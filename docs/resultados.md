# Resultados da análise de energia (gerado por `py main.py --relatorio`)

> Arquivo gerado automaticamente pelo mesmo código que responde no assistente. Não editar à mão: altere `dados/premissas.json` e gere de novo.

## 1. Situação atual (cenário de referência)

* Família de 4 pessoas, banho de 8 min, chuveiro de 5.500 W (inverno) / 3.500 W (verão).
* Potência média anual: 4.500 W.
* Consumo do chuveiro: **72,0 kWh/mês** (864 kWh/ano), 40% da conta de 180 kWh/mês.
* Tarifa estimada com tributos: **R$ 0,9506/kWh** = 0,789 / (1 − 0,17).
* Custo anual do chuveiro: **R$ 821,32**; emissão: 39,8 kgCO2/ano.
* Verificação física (Q = m·c·ΔT): vazão aquecível 3,40 L/min, 27 L por banho, 0,570 kWh de calor para 0,600 kWh elétricos (eficiência 95%).

## 2. Comparação das alternativas (mesma necessidade, 12 meses; saldo em 10 anos)

| | Alternativa | Renovável | Investimento | Manutenção/ano | kWh/ano a menos na rede | Cobertura do chuveiro | Economia líquida/ano | Retorno | Saldo no horizonte | CO2 evitado/ano |
|---|---|---|---|---|---|---|---|---|---|---|
| A | Hábitos e eficiência no chuveiro elétrico | não | R$ 0,00 | R$ 0,00 | 364 | 42% | R$ 346,02 | imediato | R$ 3.460,19 | 16,8 kg |
| B | Aquecedor solar de água (renovável térmica) | sim | R$ 5.538,00 | R$ 80,00 | 605 | 70% | R$ 494,92 | 11,2 anos | −R$ 588,76 | 27,9 kg |
| C | Energia solar fotovoltaica (renovável elétrica) | sim | R$ 6.156,00 | R$ 100,00 | 1.174 | 160% | R$ 1.015,91 | 6,1 anos | R$ 4.003,05 | 63,7 kg |

## 3. Viabilidade, impactos ambientais e limitações

### A – Hábitos e eficiência no chuveiro elétrico

**Viabilidade**

* Sem custo e imediata; vale para quem mora de aluguel.
* Depende de todos os moradores mudarem o hábito.

**Impactos ambientais**

* Reduz energia e também água (banho mais curto).
* Alivia o pico de demanda do fim da tarde, quando o chuveiro pesa mais na rede.

**Limitações**

* Economia proporcional ao hábito real; se o banho já é curto, o ganho é pequeno.
* Não muda a fonte de energia: continua 100% da rede elétrica.

### B – Aquecedor solar de água (renovável térmica)

**Viabilidade**

* Exige telhado com sol (face norte, sem sombra) e estrutura para o reservatório.
* Exige casa própria ou autorização do proprietário e adaptação hidráulica.
* Investimento inicial alto para baixa renda; procurar programas habitacionais ou financiamento.

**Impactos ambientais**

* Usa o sol diretamente para aquecer a água, sem conversão em eletricidade (alta eficiência).
* Tira o chuveiro do horário de pico, o maior benefício para o sistema elétrico.
* Fabricação usa cobre, alumínio e vidro; descarte deve ser feito em reciclagem.

**Limitações**

* Em dias nublados seguidos o apoio elétrico é usado e a economia cai.
* Fração solar de 70% é estimativa; depende de instalação, orientação e consumo de água.

### C – Energia solar fotovoltaica (renovável elétrica)

**Viabilidade**

* Exige telhado com sol, casa própria e projeto homologado na distribuidora.
* Quem mora de aluguel pode avaliar energia solar por assinatura (geração compartilhada).

**Impactos ambientais**

* Gera eletricidade renovável que também abate outros aparelhos da casa.
* O banho é à noite: a energia vai para a rede de dia e volta como crédito; não alivia o pico.
* Módulos e inversor exigem logística reversa no fim da vida útil.

**Limitações**

* Regras de compensação (Fio B) mudam até 2029 e podem reduzir o valor do crédito.
* A conta nunca fica abaixo do custo de disponibilidade (30 kWh monofásico).
* Geração varia com o clima e com o endereço; confirmar no SunData/CRESESB.

## 4. Recomendação gerada pelo assistente

1. Comece pela alternativa A (hábitos): não custa nada e reduz o consumo já no próximo mês.
2. C – Energia solar fotovoltaica (renovável elétrica): retorno estimado em 6,1 anos.
3. B – Aquecedor solar de água (renovável térmica): retorno estimado em 11,2 anos.

## 5. Premissas (origem, unidade e tipo)

| Premissa | Valor | Unidade | Tipo | Fonte / justificativa |
|---|---|---|---|---|
| `periodo_referencia` | 12 | meses | hipótese do cenário | Todas as alternativas são comparadas para a mesma necessidade (banho de 4 pessoas) em 12 meses; o saldo financeiro também é mostrado em um horizonte de 10 anos. |
| `horizonte_anos` | 10 | anos | hipótese do cenário | Horizonte menor que a vida útil dos equipamentos solares, para ser conservador. Sem correção monetária nem reajuste de tarifa. |
| `dias_por_mes` | 30 | dias | hipótese do cenário | Mês comercial. |
| `consumo_mensal_familia_kwh` | 180 | kWh/mês | ESTIMATIVA | EPE – Consumo Residencial Médio (CRM) nacional de 181,8 kWh/mês em ago/2026. Usado só para mostrar o peso do chuveiro na conta; arredondado do CRM nacional. |
| `moradores` | 4 | pessoas | hipótese do cenário |  |
| `banhos_por_pessoa_dia` | 1 | banho/dia | hipótese do cenário |  |
| `duracao_banho_min` | 8 | min | ESTIMATIVA | Duração típica relatada em campanhas de uso consciente; o usuário informa a própria duração no simulador. |
| `potencia_chuveiro_inverno_w` | 5.500 | W | hipótese do cenário | Potência nominal comum de chuveiros 127/220 V na posição inverno (dado de placa do aparelho). |
| `potencia_chuveiro_verao_w` | 3.500 | W | hipótese do cenário | Potência comum na posição verão do mesmo aparelho. |
| `meses_posicao_inverno` | 6 | meses/ano | hipótese do cenário | Cenário atual: chave em inverno metade do ano. |
| `temperatura_agua_fria_c` | 20 | °C | ESTIMATIVA | Média anual aproximada da água da rede em São Paulo; varia com a estação. |
| `temperatura_banho_c` | 38 | °C | hipótese do cenário |  |
| `eficiencia_chuveiro` | 0,95 | fração | ESTIMATIVA | Resistência elétrica converte quase toda a energia em calor; perdas pequenas para o ambiente. |
| `tarifa_b1_vigente_sem_tributos` | 0,789 | R$/kWh | dado real | ANEEL – reajuste tarifário Enel SP 2026 (vigente desde 04/07/2026): B1 residencial TE R$ 0,317 + TUSD R$ 0,472, conforme tabela publicada em calculadoraenergia.com.br. Sem tributos e sem bandeira. Conferência: B1 2025 (R$ 0,72518) x (1 + 9,02% de reajuste residencial 2026) = R$ 0,7906, coerente com R$ 0,789. |
| `tributos_fracao` | 0,17 | fração | ESTIMATIVA | RICMS-SP art. 52, V (ICMS 12% para consumo residencial de 91 a 200 kWh; Lei 12.185/2006 isenta até 90 kWh). ICMS de 12% (real, pela lei paulista) + PIS/COFINS de cerca de 5% (estimado: a alíquota efetiva muda todo mês e aparece na fatura). Aplicado 'por dentro': tarifa / (1 - tributos). |
| `fator_emissao_sin_kgco2_kwh` | 0,0461 | kgCO2/kWh | dado real | MCTI/SIRENE – planilha 'Inventários Corporativos 2026' (Inventario_2026_janset.xlsx): fator médio anual do SIN em 2025 = 0,0461 tCO2/MWh. Último ano completo. Série: 2023 = 0,0385; 2024 = 0,0545; 2025 = 0,0461 tCO2/MWh. Os meses secos (ago–nov) chegam a 0,07–0,11. |
| `solar_termico_custo_kit` | 4.405 | R$ | dado real | Anúncio Ribsol Energia Solar – kit boiler 300 L + 2 coletores 150x100 cm (consulta em 16/11/2026). Preço de varejo do equipamento, sem instalação. Outros kits de 300 L encontrados: R$ 3.690 (coletor a vácuo) a R$ 5.301 (Komeco baixa pressão). |
| `solar_termico_custo_instalacao` | 1.133 | R$ | ESTIMATIVA | SINAPI composição 103518 (aquecedor solar 300 L, fornecimento e instalação), itens de mão de obra R$ 616,90 + R$ 516,49 (ref. 09/2026). Mão de obra de referência pública; adaptações hidráulicas maiores (abrir paredes) podem custar bem mais. |
| `solar_termico_fracao_solar` | 0,7 | fração | ESTIMATIVA | Parte da energia do banho fornecida pelo sol ao longo do ano; sistemas bem dimensionados no Sudeste ficam em geral entre 60% e 80%. O restante vem do apoio elétrico. |
| `solar_termico_manutencao_ano` | 80 | R$/ano | ESTIMATIVA | Limpeza dos coletores e revisão do reservatório e das válvulas (média anual, com troca eventual de peças). |
| `solar_termico_vida_util_anos` | 20 | anos | ESTIMATIVA | Vida útil típica informada por fabricantes de coletores e reservatórios; maior que o horizonte de 10 anos usado. |
| `fv_potencia_kwp` | 1,1 | kWp | hipótese do cenário | Dois módulos de 550 Wp: menor sistema prático que cobre o consumo do chuveiro. |
| `fv_custo_kit` | 4.656 | R$ | dado real | Anúncio Rotheo Energia – kit 1,1 kWp on-grid (2 módulos 550 Wp + microinversor Deye 2 kW + estrutura), preço Pix (consulta em 16/11/2026). Só o equipamento entregue; não inclui instalação nem homologação. |
| `fv_custo_instalacao_homologacao` | 1.500 | R$ | ESTIMATIVA | Faixas de mercado: homologação/projeto de R$ 800 a R$ 3.500; referência nacional Radar Solfácil R$ 2,49/Wp para sistemas maiores. Instalação, projeto com ART e homologação na Enel para um sistema muito pequeno. Total ≈ R$ 5,59/Wp, acima da média nacional porque sistemas pequenos não ganham escala. |
| `fv_horas_sol_pleno` | 4,65 | kWh/m²·dia | dado real | CRESESB/CEPEL – SunData v3, estação São Paulo (23,5° S; 46,649° O), plano inclinado igual à latitude (24° N), média anual (consulta em 16/11/2026). Plano horizontal: 4,45. Mínimo mensal no inclinado: 4,12 (julho); máximo: 5,22 (fevereiro). |
| `fv_performance_ratio` | 0,75 | fração | ESTIMATIVA | Perdas de temperatura, sujeira, cabos e inversor. |
| `fv_fator_compensacao` | 0,85 | fração | ESTIMATIVA | Lei 14.300/2022 (marco legal da micro e minigeração distribuída). O banho é à noite, então quase toda a geração é injetada na rede e vira crédito; desde 2023 parte da TUSD Fio B deixa de ser compensada. Estimamos que 1 kWh de crédito vale 85% de 1 kWh da tarifa. |
| `fv_vida_util_anos` | 25 | anos | ESTIMATIVA | Garantia de desempenho típica dos módulos (80% da potência após 25 anos); o inversor costuma ser trocado uma vez nesse período. |
| `fv_manutencao_ano` | 100 | R$/ano | ESTIMATIVA | Limpeza dos módulos. |
| `habitos_duracao_alvo_min` | 5 | min | hipótese do cenário | Meta de banho de 5 minutos recomendada em campanhas de uso consciente de água e energia. |
| `habitos_meses_posicao_inverno` | 4 | meses/ano | hipótese do cenário | Usar a posição inverno só nos meses mais frios (jun–set). |
| `custo_disponibilidade_kwh` | 30 | kWh/mês | dado real | ANEEL – Resolução Normativa 1.000/2021 (custo de disponibilidade, ligação monofásica). Mínimo faturado em ligação monofásica; os créditos solares não reduzem a conta abaixo disso. |
| `tarifa_social_isencao_kwh` | 80 | kWh/mês | dado real | Lei 15.235/2025 (conversão da MP 1.300/2025) e regulamentação ANEEL de jul/2025. Famílias do CadÚnico com renda de até meio salário mínimo por pessoa não pagam a energia até 80 kWh/mês; o que passar de 80 kWh é cobrado. |
