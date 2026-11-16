"""Referências verificáveis usadas na análise e citadas pelo assistente."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Referencia:
    codigo: str
    descricao: str
    url: str


REFERENCIAS = {
    "ANEEL_TARIFA_2025": Referencia(
        "ANEEL_TARIFA_2025",
        "ANEEL – reajuste tarifário Enel SP 2025 (B1 residencial R$ 725,18/MWh), via Exame, 01/07/2025",
        "https://exame.com/economia/conta-de-luz-sp-aumento-enel-reajuste-tarifa-aneel-julho"),
    "ANEEL_REAJUSTE_2026": Referencia(
        "ANEEL_REAJUSTE_2026",
        "ANEEL – reajuste Enel SP 2026 (30/06/2026; residencial +9,02%; vigente desde 04/07/2026); "
        "B1 R$ 0,789/kWh sem tributos (TE 0,317 + TUSD 0,472)",
        "https://calculadoraenergia.com.br/tarifa/enel-sp"),
    "ICMS_SP": Referencia(
        "ICMS_SP",
        "RICMS-SP art. 52, V – ICMS de 12% para consumo residencial até 200 kWh; Lei 12.185/2006 – isenção até 90 kWh",
        "https://legislacao.fazenda.sp.gov.br/Paginas/an1art029.aspx"),
    "MCTI_FATOR_SIN": Referencia(
        "MCTI_FATOR_SIN",
        "MCTI/SIRENE – fator médio anual de emissão do SIN 2025: 0,0461 tCO2/MWh (planilha Inventários Corporativos 2026)",
        "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao"),
    "EPE_CONSUMO": Referencia(
        "EPE_CONSUMO",
        "EPE – Resenha Mensal do Mercado de Energia Elétrica (consumo residencial médio)",
        "https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/resenha-mensal-do-mercado-de-energia-eletrica"),
    "PROCEL_PPH": Referencia(
        "PROCEL_PPH",
        "Eletrobras/Procel – Pesquisa de Posse e Hábitos de Uso de Equipamentos (chuveiro ≈ 24% do consumo residencial)",
        "https://q.eletrobras.com/pt/AreasdeAtuacao/BRASIL.pdf"),
    "LEI_15235": Referencia(
        "LEI_15235",
        "Lei 15.235/2025 – Tarifa Social: gratuidade até 80 kWh/mês para famílias do CadÚnico",
        "https://cenarioenergia.com.br/2025/06/10/gratuidade-de-80-kwh-mensais-na-tarifa-social-e-regulamentada-pela-aneel-e-beneficia-mais-de-17-milhoes-de-familias/"),
    "LEI_14300": Referencia(
        "LEI_14300",
        "Lei 14.300/2022 – Marco legal da micro e minigeração distribuída",
        "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm"),
    "ANEEL_REN1000": Referencia(
        "ANEEL_REN1000",
        "ANEEL – Resolução Normativa 1.000/2021 (custo de disponibilidade)",
        "https://www2.aneel.gov.br/cedoc/ren20211000.html"),
    "SOLFACIL_RADAR": Referencia(
        "SOLFACIL_RADAR",
        "Radar Solfácil – preço médio residencial de sistemas FV, R$ 2,49/Wp no 3º tri 2025 (Cenário Energia)",
        "https://cenarioenergia.com.br/2025/12/02/acre-rondonia-e-alagoas-lideram-ranking-dos-estados-mais-baratos-para-instalar-energia-solar-aponta-solfacil/"),
    "CRESESB_SUNDATA": Referencia(
        "CRESESB_SUNDATA",
        "CRESESB/CEPEL – SunData v3: São Paulo, 4,65 kWh/m²·dia no plano inclinado igual à latitude (24° N)",
        "https://cresesb.cepel.br/sundata/index.php"),
    "CUSTO_SOLAR_TERMICO": Referencia(
        "CUSTO_SOLAR_TERMICO",
        "Ribsol Energia Solar – kit boiler 300 L + 2 coletores (R$ 4.405); SINAPI 103518 – mão de obra de instalação",
        "https://www.ribsolenergiasolar.com.br/kit-solar-boiler-300-litros-2-coletores-150x100cm-inox-ribsol-energia-solar"),
    "SINAPI_103518": Referencia(
        "SINAPI_103518",
        "SINAPI composição 103518 – aquecedor solar 300 L, fornecimento e instalação (mão de obra R$ 616,90 + R$ 516,49)",
        "https://orcamentor.com/composicao/103518/"),
    "CUSTO_FV_KIT": Referencia(
        "CUSTO_FV_KIT",
        "Rotheo Energia – kit FV 1,1 kWp on-grid (2 x 550 Wp + microinversor Deye 2 kW), R$ 4.656 no Pix",
        "https://www.rotheo.com.br/kit-gerador-de-energia-solar-fotovoltaico-11-kwp-on-grid-2-paineis-550kw-microinversor-deye-2kw-estrutura-cabo-30m-conector-mc6-string-box-cc-e-ca"),
}


def citar(*codigos: str) -> tuple[Referencia, ...]:
    return tuple(REFERENCIAS[c] for c in codigos)
