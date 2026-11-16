# Análise de consumo, comparação e justificativas das recomendações

Os números deste documento vêm de [resultados.md](resultados.md), gerado pelo mesmo código que responde no assistente
(`py main.py --relatorio`). As premissas, com origem, unidade e tipo (dado real, estimativa ou hipótese), estão em
[`dados/premissas.json`](../dados/premissas.json) e na seção 5 de `resultados.md`.

## 1. Conceitos aplicados

| Conceito | Onde entra |
|---|---|
| **Potência e energia** (E = P · t) | consumo do chuveiro: 4,5 kW médios x 8 min x 120 banhos/mês = **72 kWh/mês** |
| **Calor sensível** (Q = m · c · ΔT) | verificação física: 27 L por banho, de 20 para 38 °C = 0,570 kWh de calor |
| **Eficiência** | 0,570 kWh úteis / 0,600 kWh elétricos = 95% no chuveiro; o aquecedor solar usa o sol direto, sem converter em eletricidade |
| **Fonte renovável** | solar térmica (B) e solar fotovoltaica (C) |
| **Geração FV** (kWp x HSP x PR x dias) | 1,1 x 4,65 x 0,75 x 30 = 115 kWh/mês (4,65 = SunData, São Paulo, plano inclinado) |
| **Sustentabilidade** | CO2 pelo fator do SIN (MCTI), uso de água, horário de pico, descarte de equipamentos |

## 2. Análise de consumo (situação atual)

* Chuveiro de 5.500 W (inverno) e 3.500 W (verão), com a chave em inverno 6 meses por ano: potência média de 4.500 W.
* 4 pessoas x 1 banho x 8 min x 30 dias = 16 h de chuveiro por mês, o que dá **72 kWh/mês** e 864 kWh/ano.
* Tarifa com tributos de **R$ 0,9506/kWh**: B1 Enel SP vigente desde 04/07/2026 (R$ 0,789 sem tributos, dado real),
  dividida por (1 − 0,17). ICMS de 12% é real (RICMS-SP); PIS/COFINS de cerca de 5% é estimado, porque muda todo mês.
* Custo anual do chuveiro: **R$ 821,32**, ou 40% da conta.
* Emissão: 39,8 kgCO2/ano (fator do SIN 2025: 46,1 kgCO2/MWh), baixa porque a matriz elétrica brasileira é majoritariamente renovável.

## 3. Comparação (mesma necessidade, 12 meses; saldo em 10 anos)

| | Investimento | Economia líquida/ano | Retorno | Saldo em 10 anos | CO2 evitado/ano |
|---|---|---|---|---|---|
| A – Hábitos | R$ 0 | R$ 346,02 | imediato | R$ 3.460 | 16,8 kg |
| B – Aquecedor solar | R$ 5.538 | R$ 494,92 | 11,2 anos | −R$ 589 | 27,9 kg |
| C – Fotovoltaica 1,1 kWp | R$ 6.156 | R$ 1.015,91 | 6,1 anos | R$ 4.003 | 63,7 kg |

Investimentos: B = kit de 300 L anunciado a R$ 4.405 + R$ 1.133 de mão de obra (SINAPI 103518); C = kit de 1,1 kWp
anunciado a R$ 4.656 no Pix + R$ 1.500 estimados de instalação, projeto e homologação.

## 4. Justificativas das recomendações

### Custos

* **A** não tem custo e devolve cerca de R$ 29 por mês. É a única opção que serve para todos.
* **B** custa R$ 5.538 (sistema de 300 L, porte indicado para 4 pessoas) e economiza 70% da energia do banho. Nesta
  família, que já gasta pouco (banhos de 8 min), o retorno é de cerca de 11 anos: não se paga no horizonte de 10 anos,
  mas se paga dentro da vida útil de 20 anos. Fica mais atrativo quando o banho é mais longo ou o chuveiro é mais
  potente: o simulador mostra isso para cada casa.
* **C** custa R$ 6.156 e gera mais do que o chuveiro consome (160%). O excedente abate outros aparelhos, por isso o
  retorno estimado é de 6,1 anos, o melhor entre as opções que exigem investimento.

### Viabilidade

* **A** é imediata e vale para quem mora de aluguel, mas depende de todos os moradores mudarem o hábito.
* **B** e **C** exigem casa própria (ou autorização), telhado com sol e dinheiro à vista ou financiamento, uma barreira
  real para baixa renda. A opção C também exige projeto homologado na distribuidora.
* Para quem mora de aluguel, o assistente indica A, Tarifa Social e energia solar por assinatura (sem obra).

### Impactos ambientais

* No Brasil o CO2 evitado é pequeno (fator médio do SIN em 2025 de 46,1 kgCO2/MWh, MCTI), então o argumento ambiental principal não é só carbono.
* O chuveiro concentra o consumo no **horário de pico**, quando o sistema aciona termelétricas. **A** e **B** tiram
  carga desse horário. **C** gera durante o dia e devolve o crédito à noite, por isso não alivia o pico.
* **A** também economiza **água**.
* **B** e **C** usam materiais (cobre, alumínio, vidro, silício) que precisam de reciclagem e logística reversa no fim da vida.

### Recomendação final do assistente

1. Começar por **A**, porque é imediata, gratuita e vale para todos.
2. Com casa própria e telhado com sol, avaliar **C** (melhor retorno financeiro) ou **B** (maior alívio no horário de
   pico e menor dependência das regras de compensação). A ordem é calculada pelo retorno de cada casa.
3. Famílias na Tarifa Social recebem o aviso de que só o consumo acima de 80 kWh/mês gera economia em reais.

## 5. Condições e limitações

* Todos os resultados são **estimativas** para as premissas usadas, não economia garantida.
* A tarifa sem tributos é a homologada em 2026, mas o PIS/COFINS foi estimado. Bandeiras tarifárias, juros, inflação e
  reajustes futuros não foram considerados.
* Os preços dos kits são anúncios de varejo consultados em 16/11/2026, e a instalação foi estimada. Não são orçamentos
  feitos para uma casa específica: é preciso pedir orçamentos.
* A irradiação de 4,65 kWh/m²·dia é a média anual do SunData para São Paulo no plano inclinado; telhados com outra
  orientação ou com sombra geram menos. A fração solar de 70% do aquecedor é estimativa.
* Compensação da geração FV: o fator de 85% é estimativa, e as regras do Fio B (Lei 14.300) mudam até 2029.
* As alternativas foram comparadas uma a uma com a situação atual. Combinar A com B ou C **não** soma as economias.
