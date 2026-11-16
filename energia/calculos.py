"""Cálculos de energia, custo e emissões (funções puras, sem efeitos colaterais).

Conceitos usados:
* Energia elétrica: E [kWh] = P [kW] x t [h]
* Calor sensível da água: Q = m · c · ΔT, com c = 4,186 kJ/(kg·°C) e 1 L ≈ 1 kg
* Eficiência: energia útil / energia consumida
* Geração fotovoltaica: E = P_pico x HSP x PR x dias
"""
from dataclasses import dataclass

CALOR_ESPECIFICO_AGUA_KJ = 4.186   # kJ/(kg·°C)
KJ_POR_KWH = 3600.0
MESES_ANO = 12


@dataclass(frozen=True)
class PerfilBanho:
    """Hábitos de banho de uma casa (entrada do simulador)."""
    moradores: int
    banhos_por_pessoa_dia: float
    duracao_min: float
    potencia_inverno_w: float
    potencia_verao_w: float
    meses_inverno: float
    dias_por_mes: int = 30

    def __post_init__(self) -> None:
        if not 1 <= self.moradores <= 20:
            raise ValueError("moradores deve estar entre 1 e 20")
        if not 0 < self.banhos_por_pessoa_dia <= 5:
            raise ValueError("banhos por pessoa por dia deve estar entre 0 e 5")
        if not 0 < self.duracao_min <= 60:
            raise ValueError("duração do banho deve estar entre 0 e 60 minutos")
        if not 0 < self.potencia_verao_w <= self.potencia_inverno_w <= 10000:
            raise ValueError("potências devem ser positivas, até 10.000 W, e verão <= inverno")
        if not 0 <= self.meses_inverno <= MESES_ANO:
            raise ValueError("meses na posição inverno deve estar entre 0 e 12")


def energia_kwh(potencia_w: float, horas: float) -> float:
    """E = P · t (P em W convertida para kW)."""
    return potencia_w / 1000.0 * horas


def potencia_media_w(perfil: PerfilBanho) -> float:
    """Média anual ponderada pelos meses em cada posição da chave."""
    meses_verao = MESES_ANO - perfil.meses_inverno
    return (perfil.meses_inverno * perfil.potencia_inverno_w
            + meses_verao * perfil.potencia_verao_w) / MESES_ANO


def banhos_por_mes(perfil: PerfilBanho) -> float:
    return perfil.moradores * perfil.banhos_por_pessoa_dia * perfil.dias_por_mes


def consumo_chuveiro_kwh_mes(perfil: PerfilBanho) -> float:
    horas_mes = perfil.duracao_min / 60.0 * banhos_por_mes(perfil)
    return energia_kwh(potencia_media_w(perfil), horas_mes)


def energia_termica_kwh(litros: float, t_fria_c: float, t_quente_c: float) -> float:
    """Q = m · c · ΔT, convertido de kJ para kWh."""
    delta_t = t_quente_c - t_fria_c
    if litros < 0 or delta_t < 0:
        raise ValueError("litros e ΔT devem ser não negativos")
    return litros * CALOR_ESPECIFICO_AGUA_KJ * delta_t / KJ_POR_KWH


def vazao_l_min(potencia_w: float, eficiencia: float, t_fria_c: float, t_quente_c: float) -> float:
    """Vazão que o chuveiro consegue aquecer: P·η = ṁ · c · ΔT."""
    delta_t = t_quente_c - t_fria_c
    if delta_t <= 0 or not 0 < eficiencia <= 1:
        raise ValueError("ΔT deve ser positivo e eficiência entre 0 e 1")
    kg_por_s = potencia_w * eficiencia / (CALOR_ESPECIFICO_AGUA_KJ * 1000.0 * delta_t)
    return kg_por_s * 60.0


def tarifa_final(tarifa_sem_tributos: float, reajuste: float, tributos: float) -> float:
    """Aplica o reajuste e os tributos 'por dentro' (ICMS/PIS/COFINS)."""
    if not 0 <= tributos < 1:
        raise ValueError("fração de tributos deve estar entre 0 e 1")
    return tarifa_sem_tributos * (1 + reajuste) / (1 - tributos)


def kwh_faturado(consumo_kwh: float, isencao_kwh: float = 0.0) -> float:
    """kWh cobrados no mês; com a Tarifa Social só se paga o que passa da faixa isenta."""
    return max(consumo_kwh - isencao_kwh, 0.0)


def economia_mensal_reais(consumo_antes: float, consumo_depois: float,
                          tarifa: float, isencao_kwh: float = 0.0) -> float:
    """Diferença na conta, considerando a faixa isenta da Tarifa Social."""
    return (kwh_faturado(consumo_antes, isencao_kwh)
            - kwh_faturado(consumo_depois, isencao_kwh)) * tarifa


def emissao_kg(kwh: float, fator_kg_por_kwh: float) -> float:
    return kwh * fator_kg_por_kwh


def geracao_fv_kwh_mes(potencia_kwp: float, horas_sol_pleno: float,
                       performance_ratio: float, dias: int = 30) -> float:
    return potencia_kwp * horas_sol_pleno * performance_ratio * dias


def payback_anos(investimento: float, economia_liquida_anual: float) -> float | None:
    """Retorno simples (sem juros). None quando a economia não paga o investimento."""
    if investimento <= 0:
        return 0.0
    if economia_liquida_anual <= 0:
        return None
    return investimento / economia_liquida_anual
