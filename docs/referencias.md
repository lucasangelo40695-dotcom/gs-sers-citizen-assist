# Referências

As mesmas referências estão em [`energia/referencias.py`](../energia/referencias.py) e são citadas pelo assistente em cada resposta.

| Código | Referência | Uso |
|---|---|---|
| ANEEL_REAJUSTE_2026 | ANEEL – reajuste tarifário Enel SP 2026 (aprovado em 30/06/2026, residencial +9,02%, vigente desde 04/07/2026); B1 R$ 0,789/kWh sem tributos (TE 0,317 + TUSD 0,472). <https://calculadoraenergia.com.br/tarifa/enel-sp> e <https://cenarioenergia.com.br/2026/06/30/aneel-aprova-reajuste-da-enel-sao-paulo-com-efeito-medio-de-1018/> | tarifa vigente |
| ANEEL_TARIFA_2025 | ANEEL – reajuste Enel SP 2025, B1 R$ 725,18/MWh. Exame, 01/07/2025. <https://exame.com/economia/conta-de-luz-sp-aumento-enel-reajuste-tarifa-aneel-julho> | conferência da tarifa 2026 |
| ICMS_SP | RICMS-SP art. 52, V (ICMS 12% residencial até 200 kWh) e Lei 12.185/2006 (isenção até 90 kWh). <https://legislacao.fazenda.sp.gov.br/Paginas/an1art029.aspx> | tributos |
| MCTI_FATOR_SIN | MCTI/SIRENE – planilha "Inventários Corporativos 2026": fator médio anual do SIN 2025 = 0,0461 tCO2/MWh. <https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao> | CO2 evitado |
| CRESESB_SUNDATA | CRESESB/CEPEL – SunData v3, estação São Paulo: 4,65 kWh/m²·dia no plano inclinado (24° N), 4,45 no horizontal. <https://cresesb.cepel.br/index.php?section=sundata> | geração FV |
| CUSTO_SOLAR_TERMICO | Ribsol Energia Solar – kit boiler 300 L + 2 coletores, R$ 4.405. <https://www.ribsolenergiasolar.com.br/kit-solar-boiler-300-litros-2-coletores-150x100cm-inox-ribsol-energia-solar> | custo do aquecedor |
| SINAPI_103518 | SINAPI composição 103518 – aquecedor solar 300 L, fornecimento e instalação (mão de obra R$ 616,90 + R$ 516,49, ref. 09/2026). <https://orcamentor.com/composicao/103518/> | instalação do aquecedor |
| CUSTO_FV_KIT | Rotheo Energia – kit FV 1,1 kWp on-grid (2 x 550 Wp + microinversor Deye 2 kW), R$ 4.656 no Pix. <https://www.rotheo.com.br/kit-gerador-de-energia-solar-fotovoltaico-11-kwp-on-grid-2-paineis-550kw-microinversor-deye-2kw-estrutura-cabo-30m-conector-mc6-string-box-cc-e-ca> | custo da FV |
| SOLFACIL_RADAR | Radar Solfácil – preço médio residencial de sistemas FV (R$ 2,49/Wp no 3º tri 2025). <https://cenarioenergia.com.br/2025/12/02/acre-rondonia-e-alagoas-lideram-ranking-dos-estados-mais-baratos-para-instalar-energia-solar-aponta-solfacil/> | comparação de custo por Wp |
| EPE_CONSUMO | EPE – Resenha Mensal do Mercado de Energia Elétrica. <https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/resenha-mensal-do-mercado-de-energia-eletrica> | consumo médio residencial |
| PROCEL_PPH | Eletrobras/Procel – Pesquisa de Posse e Hábitos de Uso de Equipamentos Elétricos. <https://q.eletrobras.com/pt/AreasdeAtuacao/BRASIL.pdf> | peso do chuveiro no consumo e no pico |
| LEI_15235 | Lei 15.235/2025 (conversão da MP 1.300/2025) – Tarifa Social, gratuidade até 80 kWh/mês. <https://cenarioenergia.com.br/2025/06/10/gratuidade-de-80-kwh-mensais-na-tarifa-social-e-regulamentada-pela-aneel-e-beneficia-mais-de-17-milhoes-de-familias/> | Tarifa Social |
| LEI_14300 | Lei 14.300/2022 – Marco legal da micro e minigeração distribuída. <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm> | compensação da geração FV |
| ANEEL_REN1000 | ANEEL – Resolução Normativa 1.000/2021. <https://www2.aneel.gov.br/cedoc/ren20211000.html> | custo de disponibilidade |

## Verificações feitas (16/11/2026)

| Item | Antes | Verificado | Fonte |
|---|---|---|---|
| Tarifa B1 Enel SP vigente | R$ 0,72518 (2025) + reajuste médio de 10,18% (estimativa) | **R$ 0,789/kWh** sem tributos, vigente desde 04/07/2026. Confere com 0,72518 x 1,0902 (reajuste residencial) = 0,7906 | ANEEL_REAJUSTE_2026 |
| ICMS / PIS / COFINS | 17% estimado | ICMS **12%** confirmado na lei paulista para 91–200 kWh; PIS/COFINS de cerca de 5% continua **estimado** (muda todo mês) | ICMS_SP |
| Irradiação em São Paulo | 4,5 (estimado) | **4,65 kWh/m²·dia** no plano inclinado igual à latitude | CRESESB_SUNDATA |
| Fator de emissão do SIN | 0,0385 (2023) | **0,0461 tCO2/MWh** (média de 2025, último ano completo, lida na planilha oficial do MCTI) | MCTI_FATOR_SIN |
| Aquecedor solar 300 L | R$ 5.000 (faixa de mercado) | kit **R$ 4.405** (anúncio) + mão de obra **R$ 1.133** (SINAPI) = **R$ 5.538** | CUSTO_SOLAR_TERMICO, SINAPI_103518 |
| FV 1,1 kWp | R$ 3,50/Wp = R$ 3.850 | kit **R$ 4.656** (anúncio) + R$ 1.500 de instalação e homologação (estimado) = **R$ 6.156** | CUSTO_FV_KIT |
