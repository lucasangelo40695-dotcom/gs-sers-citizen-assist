"""Comparação das alternativas para a MESMA necessidade (água quente para o banho
da família) no MESMO período de referência (12 meses, com saldo em 10 anos).

A – Hábitos e eficiência no chuveiro elétrico (economia, sem investimento)
B – Aquecedor solar de água com apoio elétrico (renovável térmica)
C – Microgeração solar fotovoltaica (renovável elétrica, Lei 14.300/2022)
"""
from dataclasses import dataclass, replace

from energia import calculos as calc

MESES_ANO = 12


@dataclass(frozen=True)
class Entrada:
    """Situação da casa usada na comparação (cenário de referência ou do usuário)."""
    perfil: calc.PerfilBanho
    consumo_total_kwh_mes: float
    tarifa_social: bool = False
    casa_propria: bool = True
    telhado_com_sol: bool = True

    def __post_init__(self) -> None:
        if not 0 < self.consumo_total_kwh_mes <= 5000:
            raise ValueError("consumo total da conta deve estar entre 0 e 5.000 kWh/mês")


@dataclass(frozen=True)
class Cenario:
    consumo_chuveiro_kwh_mes: float
    consumo_total_kwh_mes: float
    participacao_chuveiro: float
    tarifa: float
    custo_chuveiro_ano: float
    emissao_chuveiro_kg_ano: float
    vazao_l_min: float
    energia_termica_banho_kwh: float
    energia_eletrica_banho_kwh: float


@dataclass(frozen=True)
class Alternativa:
    codigo: str
    nome: str
    renovavel: bool
    investimento: float
    manutencao_ano: float
    reducao_kwh_ano: float
    cobertura_chuveiro: float
    economia_bruta_ano: float
    economia_liquida_ano: float
    payback_anos: float | None
    saldo_horizonte: float
    co2_evitado_kg_ano: float
    viavel: bool
    viabilidade: tuple[str, ...]
    impactos: tuple[str, ...]
    limitacoes: tuple[str, ...]
    vida_util_anos: float = 0.0  # 0 = não se aplica (alternativa sem equipamento)

    @property
    def se_paga(self) -> bool:
        """True quando o investimento volta dentro da vida útil do equipamento."""
        if self.payback_anos is None:
            return False
        return self.vida_util_anos == 0 or self.payback_anos <= self.vida_util_anos


def entrada_referencia(v: dict) -> Entrada:
    """Família de 4 pessoas da análise (valores do premissas.json)."""
    perfil = calc.PerfilBanho(
        moradores=int(v["moradores"]),
        banhos_por_pessoa_dia=v["banhos_por_pessoa_dia"],
        duracao_min=v["duracao_banho_min"],
        potencia_inverno_w=v["potencia_chuveiro_inverno_w"],
        potencia_verao_w=v["potencia_chuveiro_verao_w"],
        meses_inverno=v["meses_posicao_inverno"],
        dias_por_mes=int(v["dias_por_mes"]),
    )
    return Entrada(perfil=perfil, consumo_total_kwh_mes=v["consumo_mensal_familia_kwh"])


def tarifa_estimada(v: dict) -> float:
    return calc.tarifa_final(v["tarifa_b1_vigente_sem_tributos"], 0.0, v["tributos_fracao"])


def calcular_cenario(entrada: Entrada, v: dict) -> Cenario:
    perfil = entrada.perfil
    consumo = calc.consumo_chuveiro_kwh_mes(perfil)
    tarifa = tarifa_estimada(v)
    isencao = v["tarifa_social_isencao_kwh"] if entrada.tarifa_social else 0.0
    sem_chuveiro = max(entrada.consumo_total_kwh_mes - consumo, 0.0)
    custo_mes = calc.economia_mensal_reais(entrada.consumo_total_kwh_mes, sem_chuveiro, tarifa, isencao)
    vazao = calc.vazao_l_min(calc.potencia_media_w(perfil), v["eficiencia_chuveiro"],
                             v["temperatura_agua_fria_c"], v["temperatura_banho_c"])
    litros_banho = vazao * perfil.duracao_min
    return Cenario(
        consumo_chuveiro_kwh_mes=consumo,
        consumo_total_kwh_mes=entrada.consumo_total_kwh_mes,
        participacao_chuveiro=min(consumo / entrada.consumo_total_kwh_mes, 1.0),
        tarifa=tarifa,
        custo_chuveiro_ano=custo_mes * MESES_ANO,
        emissao_chuveiro_kg_ano=calc.emissao_kg(consumo * MESES_ANO, v["fator_emissao_sin_kgco2_kwh"]),
        vazao_l_min=vazao,
        energia_termica_banho_kwh=calc.energia_termica_kwh(
            litros_banho, v["temperatura_agua_fria_c"], v["temperatura_banho_c"]),
        energia_eletrica_banho_kwh=calc.energia_kwh(calc.potencia_media_w(perfil), perfil.duracao_min / 60),
    )


def _montar(codigo, nome, renovavel, entrada, cenario, v, reducao_mes, kwh_limpos_mes,
            investimento, manutencao, viavel, viabilidade, impactos, limitacoes,
            vida_util=0.0) -> Alternativa:
    isencao = v["tarifa_social_isencao_kwh"] if entrada.tarifa_social else 0.0
    total = entrada.consumo_total_kwh_mes
    depois = max(total - reducao_mes, v["custo_disponibilidade_kwh"]) if codigo == "C" else total - reducao_mes
    economia_bruta = calc.economia_mensal_reais(total, depois, cenario.tarifa, isencao) * MESES_ANO
    economia_liquida = economia_bruta - manutencao
    horizonte = v["horizonte_anos"]
    return Alternativa(
        codigo=codigo, nome=nome, renovavel=renovavel,
        investimento=investimento, manutencao_ano=manutencao,
        reducao_kwh_ano=reducao_mes * MESES_ANO,
        cobertura_chuveiro=kwh_limpos_mes / cenario.consumo_chuveiro_kwh_mes,
        economia_bruta_ano=economia_bruta,
        economia_liquida_ano=economia_liquida,
        payback_anos=calc.payback_anos(investimento, economia_liquida),
        saldo_horizonte=economia_liquida * horizonte - investimento,
        co2_evitado_kg_ano=calc.emissao_kg(kwh_limpos_mes * MESES_ANO, v["fator_emissao_sin_kgco2_kwh"]),
        viavel=viavel, viabilidade=viabilidade, impactos=impactos, limitacoes=limitacoes,
        vida_util_anos=vida_util,
    )


def alternativa_habitos(entrada: Entrada, cenario: Cenario, v: dict) -> Alternativa:
    perfil = entrada.perfil
    novo = replace(perfil,
                   duracao_min=min(perfil.duracao_min, v["habitos_duracao_alvo_min"]),
                   meses_inverno=min(perfil.meses_inverno, v["habitos_meses_posicao_inverno"]))
    reducao = cenario.consumo_chuveiro_kwh_mes - calc.consumo_chuveiro_kwh_mes(novo)
    return _montar(
        "A", "Hábitos e eficiência no chuveiro elétrico", False, entrada, cenario, v,
        reducao, reducao, 0.0, 0.0, True,
        viabilidade=("Sem custo e imediata; vale para quem mora de aluguel.",
                     "Depende de todos os moradores mudarem o hábito."),
        impactos=("Reduz energia e também água (banho mais curto).",
                  "Alivia o pico de demanda do fim da tarde, quando o chuveiro pesa mais na rede."),
        limitacoes=("Economia proporcional ao hábito real; se o banho já é curto, o ganho é pequeno.",
                    "Não muda a fonte de energia: continua 100% da rede elétrica."),
    )


def alternativa_solar_termico(entrada: Entrada, cenario: Cenario, v: dict) -> Alternativa:
    reducao = cenario.consumo_chuveiro_kwh_mes * v["solar_termico_fracao_solar"]
    viavel = entrada.casa_propria and entrada.telhado_com_sol
    return _montar(
        "B", "Aquecedor solar de água (renovável térmica)", True, entrada, cenario, v,
        reducao, reducao, v["solar_termico_custo_kit"] + v["solar_termico_custo_instalacao"],
        v["solar_termico_manutencao_ano"], viavel,
        viabilidade=("Exige telhado com sol (face norte, sem sombra) e estrutura para o reservatório.",
                     "Exige casa própria ou autorização do proprietário e adaptação hidráulica.",
                     "Investimento inicial alto para baixa renda; procurar programas habitacionais ou financiamento."),
        impactos=("Usa o sol diretamente para aquecer a água, sem conversão em eletricidade (alta eficiência).",
                  "Tira o chuveiro do horário de pico, o maior benefício para o sistema elétrico.",
                  "Fabricação usa cobre, alumínio e vidro; descarte deve ser feito em reciclagem."),
        limitacoes=("Em dias nublados seguidos o apoio elétrico é usado e a economia cai.",
                    "Fração solar de 70% é estimativa; depende de instalação, orientação e consumo de água."),
        vida_util=v["solar_termico_vida_util_anos"],
    )


def alternativa_fotovoltaica(entrada: Entrada, cenario: Cenario, v: dict) -> Alternativa:
    geracao = calc.geracao_fv_kwh_mes(v["fv_potencia_kwp"], v["fv_horas_sol_pleno"],
                                      v["fv_performance_ratio"], entrada.perfil.dias_por_mes)
    credito_equivalente = geracao * v["fv_fator_compensacao"]
    viavel = entrada.casa_propria and entrada.telhado_com_sol
    return _montar(
        "C", "Energia solar fotovoltaica (renovável elétrica)", True, entrada, cenario, v,
        credito_equivalente, geracao, v["fv_custo_kit"] + v["fv_custo_instalacao_homologacao"],
        v["fv_manutencao_ano"], viavel,
        viabilidade=("Exige telhado com sol, casa própria e projeto homologado na distribuidora.",
                     "Quem mora de aluguel pode avaliar energia solar por assinatura (geração compartilhada)."),
        impactos=("Gera eletricidade renovável que também abate outros aparelhos da casa.",
                  "O banho é à noite: a energia vai para a rede de dia e volta como crédito; não alivia o pico.",
                  "Módulos e inversor exigem logística reversa no fim da vida útil."),
        limitacoes=("Regras de compensação (Fio B) mudam até 2029 e podem reduzir o valor do crédito.",
                    "A conta nunca fica abaixo do custo de disponibilidade (30 kWh monofásico).",
                    "Geração varia com o clima e com o endereço; confirmar no SunData/CRESESB."),
        vida_util=v["fv_vida_util_anos"],
    )


def comparar(entrada: Entrada, v: dict) -> tuple[Cenario, tuple[Alternativa, ...]]:
    cenario = calcular_cenario(entrada, v)
    alternativas = (
        alternativa_habitos(entrada, cenario, v),
        alternativa_solar_termico(entrada, cenario, v),
        alternativa_fotovoltaica(entrada, cenario, v),
    )
    return cenario, alternativas


def recomendar(entrada: Entrada, alternativas: tuple[Alternativa, ...]) -> tuple[str, ...]:
    """Ordem de recomendação coerente com a análise (não é promessa de resultado)."""
    passos = ["Comece pela alternativa A (hábitos): não custa nada e reduz o consumo já no próximo mês."]
    renovaveis = sorted((a for a in alternativas if a.renovavel and a.viavel),
                        key=lambda a: a.payback_anos if a.payback_anos is not None else float("inf"))
    if not renovaveis:
        motivo = "Sem casa própria" if not entrada.casa_propria else "Sem telhado com sol"
        dica = "" if entrada.tarifa_social else " e confira se tem direito à Tarifa Social"
        passos.append(f"{motivo}, as opções solares no telhado não se aplicam agora; "
                      f"avalie energia solar por assinatura{dica}.")
    for alt in renovaveis:
        if not alt.se_paga:
            passos.append(f"{alt.codigo} – {alt.nome}: com estes dados a economia não paga o investimento "
                          "dentro da vida útil do equipamento.")
        else:
            anos = f"{alt.payback_anos:.1f}".replace(".", ",")
            passos.append(f"{alt.codigo} – {alt.nome}: retorno estimado em {anos} anos.")
    if entrada.tarifa_social:
        passos.append("Com a Tarifa Social, os primeiros 80 kWh do mês já são gratuitos: a economia em reais "
                      "vem só do consumo acima disso.")
    return tuple(passos)
