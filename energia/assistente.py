"""Respostas de energia do Citizen Assist AI.

O assistente reconhece a intenção da pergunta por palavras-chave e responde
com os números calculados em energia.comparacao, sempre indicando fontes e
limitações. Nenhum número é escrito à mão no texto: tudo vem da análise.
"""
import re
import unicodedata
from dataclasses import dataclass, replace

from energia import comparacao as cmp
from energia.premissas import carregar_premissas, valores
from energia.referencias import REFERENCIAS, Referencia, citar

AVISO_PADRAO = ("Valores são ESTIMATIVAS para o cenário informado, não resultados garantidos. "
                "Tarifa, clima, preços e hábitos reais mudam o resultado.")

# Ordem importa: intenções mais específicas primeiro ("aquecedor solar" antes de "solar").
INTENCOES = (
    ("comparar", ("diferenca entre",)),
    ("tarifa_social", ("tarifa social", "baixa renda", "cadunico", "cad unico", "gratuidade", "isencao",
                       "bolsa familia", "beneficio")),
    ("aluguel", ("aluguel", "alugad", "inquilino", "nao tenho casa", "apartamento", "assinatura")),
    ("solar_termico", ("aquecedor solar", "aquecimento solar", "agua quente solar", "boiler", "coletor solar")),
    ("fotovoltaica", ("painel", "placa", "fotovolt", "energia solar", "gerar energia")),
    ("comparar", ("compar", "melhor", "vale a pena", "qual escolher", "recomend", "o que fazer", "mais barat",
                  "tempo pra pagar", "tempo para pagar", "se paga", "retorno")),
    ("kwh", ("o que e kwh", "o que e um kwh", "o que significa kwh", "kwh significa", "o que e quilowatt")),
    ("habitos", ("dica", "economiz", "reduzir", "diminuir", "baixar", "banho curto", "posicao verao", "habito")),
    ("ambiental", ("co2", "carbono", "ambient", "polui", "sustentav", "planeta")),
    ("calculo", ("calculou", "calculo", "calcula", "formula", "como chegou", "de onde vem o numero", "conta feita")),
    ("fontes", ("fonte", "referencia", "de onde", "dados usados")),
    ("limitacoes", ("limitac", "garant", "certeza", "certo", "verdade", "confiavel", "confiar", "precisao")),
    ("consumo", ("chuveiro", "gasta", "consumo", "quanto", "conta de luz", "kwh")),
)
# Nomes em linguagem simples para a resposta "fontes" (o público não lê chaves técnicas).
ROTULOS = {
    "tarifa_b1_vigente_sem_tributos": "Preço do kWh na Enel SP, sem impostos (ANEEL 2026)",
    "tributos_fracao": "Impostos na conta (ICMS 12% + PIS/COFINS)",
    "fator_emissao_sin_kgco2_kwh": "CO2 por kWh da rede elétrica (MCTI 2025)",
    "fv_horas_sol_pleno": "Sol médio em São Paulo (SunData)",
    "solar_termico_custo_kit": "Kit de aquecedor solar de 300 L",
    "solar_termico_custo_instalacao": "Instalação do aquecedor solar",
    "solar_termico_fracao_solar": "Parte do banho aquecida pelo sol",
    "fv_custo_kit": "Kit de placa solar de 1,1 kWp",
    "fv_custo_instalacao_homologacao": "Instalação e homologação da placa solar",
    "fv_fator_compensacao": "Quanto vale o crédito de energia solar",
    "tarifa_social_isencao_kwh": "Faixa gratuita da Tarifa Social",
    "eficiencia_chuveiro": "Eficiência do chuveiro elétrico",
}
# "banho de 10 minutos", "somos 6 pessoas": recalcula na hora com o número informado.
PADRAO_MINUTOS = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:min|minuto)")
PADRAO_PESSOAS = re.compile(r"(\d+)\s*(?:pessoa|morador)")


@dataclass(frozen=True)
class Resposta:
    intencao: str
    texto: str
    fontes: tuple[Referencia, ...]
    limitacoes: tuple[str, ...]

    def formatar(self) -> str:
        linhas = [self.texto, "", "Atenção:"]
        linhas += [f"  • {item}" for item in self.limitacoes + (AVISO_PADRAO,)]
        if self.fontes:
            linhas += ["", "Fontes:"]
            linhas += [f"  [{r.codigo}] {r.descricao} – {r.url}" for r in self.fontes]
        return "\n".join(linhas)


def normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return " ".join(sem_acento.lower().split())


def identificar_intencao(pergunta: str) -> str:
    texto = normalizar(pergunta)
    if PADRAO_MINUTOS.search(texto) or PADRAO_PESSOAS.search(texto):
        return "simular"
    for intencao, palavras in INTENCOES:
        if any(p in texto for p in palavras):
            return intencao
    return "ajuda"


def reais(valor: float) -> str:
    texto = f"R$ {abs(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"−{texto}" if valor < -0.005 else texto


def num(valor: float, casas: int = 1) -> str:
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(fracao: float) -> str:
    return f"{fracao * 100:.0f}%"


class AssistenteEnergia:
    """Guarda a situação da casa (imutável) e responde perguntas sobre energia."""

    def __init__(self, premissas=None, entrada: cmp.Entrada | None = None) -> None:
        self.premissas = premissas or carregar_premissas()
        self.v = valores(self.premissas)
        self.entrada = entrada or cmp.entrada_referencia(self.v)

    def com_entrada(self, entrada: cmp.Entrada) -> "AssistenteEnergia":
        """Devolve um NOVO assistente para outra casa (não altera o atual)."""
        return AssistenteEnergia(self.premissas, entrada)

    def com_situacao(self, **campos) -> "AssistenteEnergia":
        return self.com_entrada(replace(self.entrada, **campos))

    # ------------------------------------------------------------------ análise
    def analise(self):
        return cmp.comparar(self.entrada, self.v)

    def responder(self, pergunta: str) -> Resposta:
        if not pergunta or not pergunta.strip():
            return self._ajuda()
        intencao = identificar_intencao(pergunta)
        if intencao == "simular":
            return self._simular(normalizar(pergunta))
        return getattr(self, f"_{intencao}")()

    def _simular(self, texto: str) -> Resposta:
        """Recalcula o consumo com minutos e/ou pessoas citados na pergunta."""
        perfil = self.entrada.perfil
        minutos = PADRAO_MINUTOS.search(texto)
        pessoas = PADRAO_PESSOAS.search(texto)
        try:
            novo = replace(
                perfil,
                duracao_min=float(minutos.group(1).replace(",", ".")) if minutos else perfil.duracao_min,
                moradores=int(pessoas.group(1)) if pessoas else perfil.moradores,
            )
        except ValueError as erro:
            return Resposta("simular", f"Não consegui simular: {erro}.", (), ())
        antes, _ = self.analise()
        outro = self.com_entrada(replace(self.entrada, perfil=novo,
                                         consumo_total_kwh_mes=max(self.entrada.consumo_total_kwh_mes,
                                                                   cmp.calc.consumo_chuveiro_kwh_mes(novo))))
        depois, _ = outro.analise()
        diferenca = depois.custo_chuveiro_ano - antes.custo_chuveiro_ano
        sentido = "a mais" if diferenca > 0 else "a menos"
        texto_resp = (
            f"Com {novo.moradores} pessoa(s) e banho de {num(novo.duracao_min, 0)} min, o chuveiro gastaria cerca de "
            f"{num(depois.consumo_chuveiro_kwh_mes)} kWh por mês ({reais(depois.custo_chuveiro_ano)} por ano).\n"
            f"Comparado ao cenário atual ({num(antes.consumo_chuveiro_kwh_mes)} kWh/mês), são "
            f"{reais(abs(diferenca))} {sentido} por ano.\n"
            "Para ver as opções solares com esses dados, use o menu 2 (Simular a minha casa)."
        )
        return Resposta("simular", texto_resp, citar("ANEEL_REAJUSTE_2026", "ICMS_SP"),
                        ("Mantivemos a potência do chuveiro e os meses na posição inverno do cenário atual.",))

    def _kwh(self) -> Resposta:
        c, _ = self.analise()
        texto = (
            "kWh (quilowatt-hora) é a unidade de energia que aparece na conta de luz.\n"
            "1 kWh é a energia de um aparelho de 1.000 W ligado por 1 hora.\n"
            f"Exemplo: um chuveiro de {num(self.v['potencia_chuveiro_inverno_w'], 0)} W ligado 1 hora gasta "
            f"{num(self.v['potencia_chuveiro_inverno_w'] / 1000)} kWh, cerca de "
            f"{reais(self.v['potencia_chuveiro_inverno_w'] / 1000 * c.tarifa)} com a tarifa estimada."
        )
        return Resposta("kwh", texto, citar("ANEEL_REAJUSTE_2026"), ())

    # --------------------------------------------------------------- respostas
    def _consumo(self) -> Resposta:
        c, _ = self.analise()
        p = self.entrada.perfil
        texto = (
            f"Seu chuveiro gasta cerca de {num(c.consumo_chuveiro_kwh_mes)} kWh por mês "
            f"({pct(c.participacao_chuveiro)} de uma conta de {num(c.consumo_total_kwh_mes, 0)} kWh).\n"
            f"Conta: {p.moradores} pessoa(s) x {num(p.banhos_por_pessoa_dia, 0)} banho(s) x "
            f"{num(p.duracao_min, 0)} min x {p.dias_por_mes} dias, com potência média de "
            f"{num(cmp.calc.potencia_media_w(p), 0)} W (E = P x t).\n"
            f"Isso custa cerca de {reais(c.custo_chuveiro_ano)} por ano, com tarifa estimada de "
            f"{reais(c.tarifa)}/kWh com impostos."
        )
        return Resposta("consumo", texto, citar("ANEEL_REAJUSTE_2026", "ICMS_SP", "PROCEL_PPH"),
                        ("A potência real está na etiqueta do chuveiro; a duração do banho é informada por você.",
                         "Bandeiras tarifárias (amarela/vermelha) não foram incluídas e podem aumentar o custo."))

    def _habitos(self) -> Resposta:
        c, alts = self.analise()
        a = alts[0]
        texto = (
            f"Dicas que não custam nada (alternativa A):\n"
            f"  1. Banho de até {num(self.v['habitos_duracao_alvo_min'], 0)} minutos.\n"
            f"  2. Chave na posição VERÃO, exceto nos {num(self.v['habitos_meses_posicao_inverno'], 0)} meses mais frios.\n"
            f"  3. Desligar o chuveiro ao se ensaboar.\n"
            f"Na sua situação, isso reduz cerca de {num(a.reducao_kwh_ano, 0)} kWh por ano "
            f"({pct(a.cobertura_chuveiro)} do chuveiro), economia de cerca de {reais(a.economia_liquida_ano)} por ano "
            f"e {num(a.co2_evitado_kg_ano)} kg de CO2 a menos."
        )
        return Resposta("habitos", texto, citar("ANEEL_REAJUSTE_2026", "MCTI_FATOR_SIN"), a.limitacoes)

    def _texto_alternativa(self, alt: cmp.Alternativa) -> str:
        if alt.se_paga:
            retorno = f"cerca de {num(alt.payback_anos)} anos"
        else:
            retorno = f"não se paga dentro da vida útil ({num(alt.vida_util_anos, 0)} anos) com estes dados"
        situacao = "" if alt.viavel else "\nPara a sua casa (aluguel ou sem telhado com sol) esta opção NÃO se aplica agora."
        return (
            f"{alt.codigo} – {alt.nome}\n"
            f"  Investimento estimado: {reais(alt.investimento)} | manutenção: {reais(alt.manutencao_ano)}/ano\n"
            f"  Cobre {pct(alt.cobertura_chuveiro)} da energia do chuveiro | "
            f"economia líquida: {reais(alt.economia_liquida_ano)}/ano\n"
            f"  Retorno do investimento: {retorno} | saldo em {num(self.v['horizonte_anos'], 0)} anos: "
            f"{reais(alt.saldo_horizonte)}\n"
            f"  CO2 evitado: {num(alt.co2_evitado_kg_ano)} kg/ano\n"
            f"  Viabilidade: " + " ".join(alt.viabilidade) + "\n"
            f"  Ambiente: " + " ".join(alt.impactos) + situacao
        )

    def _solar_termico(self) -> Resposta:
        _, alts = self.analise()
        return Resposta("solar_termico", self._texto_alternativa(alts[1]),
                        citar("CUSTO_SOLAR_TERMICO", "SINAPI_103518", "ANEEL_REAJUSTE_2026", "MCTI_FATOR_SIN"), alts[1].limitacoes)

    def _fotovoltaica(self) -> Resposta:
        _, alts = self.analise()
        return Resposta("fotovoltaica", self._texto_alternativa(alts[2]),
                        citar("CUSTO_FV_KIT", "SOLFACIL_RADAR", "CRESESB_SUNDATA", "LEI_14300", "ANEEL_REN1000"), alts[2].limitacoes)

    def _comparar(self) -> Resposta:
        c, alts = self.analise()
        cab = f"{'Opção':<6}{'Investe':>14}{'Economia/ano':>16}{'Retorno':>10}{'Saldo 10a':>14}{'CO2 kg/ano':>12}"
        linhas = [f"Comparação para a mesma necessidade (banho da família, 12 meses). "
                  f"Hoje o chuveiro custa {reais(c.custo_chuveiro_ano)}/ano.", "", cab]
        for a in alts:
            if not a.viavel:
                linhas.append(f"{a.codigo:<6}  não se aplica à sua casa (precisa de casa própria e telhado com sol)")
                continue
            if a.investimento == 0:
                retorno = "imediato"
            else:
                retorno = f"{num(a.payback_anos)} a" if a.se_paga else "não paga"
            linhas.append(f"{a.codigo:<6}{reais(a.investimento):>14}{reais(a.economia_liquida_ano):>16}"
                          f"{retorno:>10}{reais(a.saldo_horizonte):>14}{num(a.co2_evitado_kg_ano):>12}")
        linhas += ["", "Recomendação:"] + [f"  {i}. {p}" for i, p in enumerate(cmp.recomendar(self.entrada, alts), 1)]
        return Resposta("comparar", "\n".join(linhas),
                        citar("ANEEL_REAJUSTE_2026", "CUSTO_SOLAR_TERMICO", "SOLFACIL_RADAR", "MCTI_FATOR_SIN"),
                        ("Cada alternativa foi comparada com a situação atual; somar A com B ou C não soma as economias, "
                         "porque com banhos mais curtos sobra menos energia para o solar economizar.",
                         "Retorno simples, sem juros nem reajuste de tarifa."))

    def _tarifa_social(self) -> Resposta:
        isencao = self.v["tarifa_social_isencao_kwh"]
        texto = (
            f"Famílias inscritas no CadÚnico com renda de até meio salário mínimo por pessoa têm gratuidade "
            f"até {num(isencao, 0)} kWh por mês na conta de luz. O que passar de {num(isencao, 0)} kWh é cobrado.\n"
            f"Para manter o benefício: conta no nome de alguém da família e cadastro atualizado no CRAS.\n"
            f"Se a casa gasta menos de {num(isencao, 0)} kWh, economizar energia ajuda o ambiente, mas quase não muda a conta."
        )
        return Resposta("tarifa_social", texto, citar("LEI_15235"),
                        ("Regras e faixas de renda podem mudar; confirme na distribuidora ou no CRAS.",))

    def _aluguel(self) -> Resposta:
        alugada = self.com_situacao(casa_propria=False)
        _, alts = alugada.analise()
        texto = (
            "Quem mora de aluguel normalmente não pode instalar aquecedor solar ou placas no telhado sem autorização.\n"
            f"O que funciona já: alternativa A, com economia estimada de {reais(alts[0].economia_liquida_ano)} por ano.\n"
            "Também vale conhecer a energia solar por assinatura (geração compartilhada), que não exige obra, "
            "e verificar se a família tem direito à Tarifa Social."
        )
        return Resposta("aluguel", texto, citar("LEI_14300", "LEI_15235"),
                        ("Ofertas de assinatura têm contrato, fidelidade e desconto variáveis; leia antes de assinar.",))

    def _ambiental(self) -> Resposta:
        c, alts = self.analise()
        texto = (
            f"O chuveiro da casa emite cerca de {num(c.emissao_chuveiro_kg_ano)} kg de CO2 por ano. É pouco porque a "
            f"eletricidade brasileira é majoritariamente renovável (fator de {num(self.v['fator_emissao_sin_kgco2_kwh'] * 1000)} "
            f"kgCO2/MWh).\n"
            f"CO2 evitado por ano: A {num(alts[0].co2_evitado_kg_ano)} kg | B {num(alts[1].co2_evitado_kg_ano)} kg | "
            f"C {num(alts[2].co2_evitado_kg_ano)} kg.\n"
            "O maior ganho ambiental do chuveiro está no HORÁRIO DE PICO (fim da tarde), quando o sistema liga "
            "termelétricas: as opções A e B reduzem o consumo nesse horário; a C gera de dia."
        )
        return Resposta("ambiental", texto, citar("MCTI_FATOR_SIN", "PROCEL_PPH"),
                        ("Fator anual médio; no horário de pico a emissão real por kWh é maior.",
                         "Não inclui emissões de fabricação e transporte dos equipamentos."))

    def _calculo(self) -> Resposta:
        c, _ = self.analise()
        texto = (
            "Como os números são calculados:\n"
            "  • Energia: E (kWh) = Potência (kW) x tempo (h).\n"
            "  • Água do banho: Q = m · c · ΔT, com c = 4,186 kJ/kg°C. "
            f"Um banho usa cerca de {num(c.vazao_l_min * self.entrada.perfil.duracao_min, 0)} L, "
            f"aquecidos de {num(self.v['temperatura_agua_fria_c'], 0)} para {num(self.v['temperatura_banho_c'], 0)} °C: "
            f"{num(c.energia_termica_banho_kwh, 2)} kWh de calor contra {num(c.energia_eletrica_banho_kwh, 2)} kWh de "
            f"eletricidade (eficiência de {pct(self.v['eficiencia_chuveiro'])}).\n"
            "  • Custo: kWh x tarifa com impostos. Retorno = investimento / economia líquida anual.\n"
            "  • Solar FV: kWp x horas de sol pleno x performance x 30 dias.\n"
            "  • CO2: kWh x fator de emissão do SIN."
        )
        return Resposta("calculo", texto, citar("MCTI_FATOR_SIN", "CRESESB_SUNDATA"), ())

    def _fontes(self) -> Resposta:
        def linha(chave: str) -> str:
            p = self.premissas[chave]
            if p.unidade == "fração":
                return f"  • {ROTULOS[chave]}: {pct(p.valor)}"
            casas = 4 if p.valor < 0.1 else 3 if p.valor < 1 else 2 if p.valor < 10 else 0
            return f"  • {ROTULOS[chave]}: {num(p.valor, casas)} {p.unidade}"

        oficiais = [linha(c) for c in ROTULOS if self.premissas[c].tipo == "real"]
        estimados = [linha(c) for c in ROTULOS if self.premissas[c].tipo == "estimado"]
        texto = ("Dados OFICIAIS ou de preço publicado (fontes no fim desta resposta):\n" + "\n".join(oficiais)
                 + "\n\nESTIMATIVAS da equipe (explicadas em dados/premissas.json):\n" + "\n".join(estimados)
                 + "\n\nOs dados da sua casa (pessoas, minutos, potência, conta) vêm do que você informa no simulador.")
        return Resposta("fontes", texto, tuple(REFERENCIAS.values()), ())

    def _limitacoes(self) -> Resposta:
        texto = (
            "As orientações são estimativas para ajudar a decidir, não promessas de economia:\n"
            "  • A tarifa 2026 sem impostos é a homologada pela ANEEL; o PIS/COFINS muda todo mês, confira na sua conta.\n"
            "  • Preços dos kits são anúncios de varejo e a instalação foi estimada; peça ao menos 3 orçamentos.\n"
            "  • Geração solar depende do clima, sombra e orientação do telhado.\n"
            "  • Regras de compensação de energia solar (Lei 14.300) mudam ao longo dos anos.\n"
            "  • Não consideramos juros, inflação nem bandeiras tarifárias."
        )
        return Resposta("limitacoes", texto, citar("LEI_14300", "ANEEL_REAJUSTE_2026", "ICMS_SP"), ())

    def _ajuda(self) -> Resposta:
        texto = (
            "Posso ajudar com energia do banho e da conta de luz. Exemplos de perguntas:\n"
            "  • Quanto meu chuveiro gasta?\n"
            "  • Dicas para economizar\n"
            "  • Vale a pena aquecedor solar?\n"
            "  • E painel solar fotovoltaico?\n"
            "  • Qual a melhor opção para mim?\n"
            "  • Moro de aluguel, o que posso fazer?\n"
            "  • Tenho direito à Tarifa Social?\n"
            "  • Qual o impacto ambiental?  • Como você calculou?  • Quais as fontes?  • Isso é garantido?"
        )
        return Resposta("ajuda", texto, (), ())
