
## Protocolo

Cada entrevistado respondeu as mesmas quatro tarefas:

* **T1** – Descobrir quanto o chuveiro de casa gasta por mês (pergunta livre).
* **T2** – Simular a própria casa (menu 2) com os dados da etiqueta do chuveiro e da conta de luz.
* **T3** – Perguntar se vale a pena aquecedor solar ou placa solar.
* **T4** – Descobrir de onde vieram os números e o que **não** é garantido.

Em cada tarefa, a equipe registrou a pergunta digitada, a resposta do assistente e se ela era clara e útil para aquele perfil.

## Dados
|---|---|---|
| Entrevistado 1 | Aposentada, mora com mais 1 pessoa, recebe Tarifa Social, casa própria com telhado sombreado | 2 pessoas, banho de 6 min, chuveiro 4.400/2.100 W, inverno 3 meses, conta de 95 kWh |
| Entrevistado 2 | Inquilino, 3 pessoas, banhos longos | 3 pessoas, 15 min, 5.500/3.500 W, inverno 8 meses, conta de 210 kWh |
| Entrevistado 3 | Casa própria com sol, 5 pessoas, chuveiro potente | 5 pessoas, 10 min, 7.500/5.000 W, inverno 6 meses, conta de 260 kWh |

## Registro dos testes

| Entrevistado | Tarefa | Pergunta digitada | Resultado observado | Problema? | Depois do ajuste |
|---|---|---|---|---|---|
| Entrevistado 1 | T1 | "quanto eu gasto com o chuveiro por mes" | 72 kWh/mês (família de referência) | Não: antes de simular, a resposta é da família de referência | — |
| Entrevistado 1 | T2 | simulador | chuveiro 16 kWh/mês, R$ 171/ano; hábitos economizam R$ 30/ano; aviso da Tarifa Social | **Sim**: a tabela mostrava retorno de 115 anos (aquecedor) e 86,6 anos (placa) mesmo sem sol no telhado | B e C aparecem como "não se aplica à sua casa" |
| Entrevistado 1 | T2 | simulador | recomendação dizia "confira se tem direito à Tarifa Social" | **Sim**: ela já informou que recebe | dica não aparece para quem já recebe |
| Entrevistado 1 | T3 | "vale a pena aquecedor solar pra mim?" | "retorno de cerca de 115,0 anos" | **Sim**: número maior que a vida útil (20 anos) confunde | "não se paga dentro da vida útil (20 anos)" |
| Entrevistado 1 | T4 | "isso é certo?" | caiu na resposta genérica de ajuda | **Sim**: pergunta não reconhecida | mostra as limitações |
| Entrevistado 1 | T4 | "de onde vc tirou essas contas" | lista com nomes técnicos (`consumo_mensal_familia_kwh`) | **Sim**: ilegível para o público | nomes simples, separando dados oficiais e estimativas |
| Entrevistado 2 | T1 | "meu chuveiro come muita luz?" | consumo e custo do chuveiro | Não | — |
| Entrevistado 2 | T2 | simulador | chuveiro 109 kWh/mês, R$ 1.241/ano; hábitos economizam R$ 884/ano | **Sim**: a tabela mostrava retorno de 7,0 e 6,1 anos das opções solares para quem mora de aluguel | B e C aparecem como "não se aplica à sua casa" |
| Entrevistado 2 | T3 | "e placa solar, da pra eu colocar?" | explica, avisa "NÃO se aplica" e indica energia por assinatura | Não | — |
| Entrevistado 2 | T4 | "esses valores sao garantidos" | lista de limitações | Não | — |
| Entrevistado 3 | T1 | "qnto gasta o chuveiro" | consumo e custo do chuveiro | Não | — |
| Entrevistado 3 | T2 | simulador | chuveiro 156 kWh/mês (60% da conta); aquecedor solar se paga em 4,7 anos, placa em 6,1 | Não: com consumo alto, o aquecedor solar passa a ser a melhor opção | — |
| Entrevistado 3 | T3 | "quanto tempo pra pagar a placa" | respondeu o consumo do chuveiro | **Sim**: "placa" sozinha não era reconhecida | responde sobre a placa solar (retorno de 6,1 anos) |
| Entrevistado 3 | T4 | "fontes" | mesma lista técnica da Entrevistado 1 | **Sim** (mesmo problema) | nomes simples |

**Resumo:** 14 situações testadas, 8 com problema; todas corrigidas. Os resultados mostram que a recomendação muda com o
perfil: para o Entrevistado 1 só os hábitos fazem sentido, para o Entrevistado 2 hábitos + energia por assinatura, e para o
Entrevistado 3 o aquecedor solar tem o melhor retorno.

## Ajustes realizados a partir dos testes

| # | Problema observado | Ajuste feito | Arquivo |
|---|---|---|---|
| 1 | Opções que não se aplicam à casa apareciam com retorno na tabela | B e C aparecem como "não se aplica à sua casa (precisa de casa própria e telhado com sol)" | `energia/assistente.py` (`_comparar`) |
| 2 | Retorno de 115 anos mostrado como número | Verificação `se_paga`: acima da vida útil aparece "não se paga dentro da vida útil" | `energia/comparacao.py`, `assistente.py`, `relatorio.py` |
| 3 | Sugeria Tarifa Social a quem já recebe | Dica só aparece para quem não recebe; motivo específico (sem casa própria ou sem sol) | `energia/comparacao.py` (`recomendar`) |
| 4 | "isso é certo?" não reconhecido | Palavras `certo` e `verdade` levam às limitações | `energia/assistente.py` |
| 5 | "a placa" e "tempo pra pagar" não reconhecidos | `placa` leva à energia fotovoltaica; `se paga`, `retorno` e `tempo pra pagar` levam à comparação | `energia/assistente.py` |
| 6 | Fontes com nomes técnicos | Nomes em linguagem simples, com percentuais, separando dados oficiais e estimativas | `energia/assistente.py` (`ROTULOS`, `_fontes`) |

Todos os casos viraram testes automáticos em `tests/test_assistente.py`, para os problemas não voltarem.

## Pré-teste de linguagem 

Antes das Entrevistados, a equipe escreveu 25 perguntas do jeito que um morador perguntaria, com gírias, sem acento e sem
termos técnicos, e verificou se o assistente entendia. Na primeira rodada, **9 de 25** caíram na resposta genérica de ajuda
ou na intenção errada.

| Pergunta | Antes | Depois do ajuste |
|---|---|---|
| "como baixar a conta?" | ajuda | dicas de economia |
| "tenho bolsa familia, pago luz?" | ajuda | Tarifa Social |
| "o que é kwh?" | consumo (não explicava a unidade) | explicação de kWh com exemplo do chuveiro |
| "e se eu tomar banho de 10 minutos?" | ajuda | **recalcula na hora**: 90 kWh/mês, R$ 205,33 a mais por ano |
| "minha casa tem 6 pessoas" | ajuda | recalcula com 6 pessoas |
| "qual opção é mais barata?" | ajuda | comparação das alternativas |
| "isso polui?" | ajuda | impacto ambiental |
| "posso confiar nesses numeros?" | ajuda | limitações |
| "qual a diferença entre aquecedor solar e painel solar?" | só aquecedor | comparação das alternativas |
| "energia solar por assinatura" | painel no telhado | orientação para quem mora de aluguel |

Segunda rodada: **24 de 25** reconhecidas. A única que vai para a ajuda é "oi", o que é o esperado.

## Ajustes feitos durante o desenvolvimento

| Situação testada | Problema encontrado | Ajuste |
|---|---|---|
| Pergunta "como você calculou?" | caía na ajuda (só reconhecia "como calcul…") | palavras-chave `calculou`, `calculo`, `calcula` em `energia/assistente.py` |
| Simulação com banho de 50 min e conta de 180 kWh | chuveiro maior que a conta inteira gerava resultado incoerente | o simulador mostra o consumo do chuveiro e não aceita conta menor que ele (`main.py`) |
| Premissas estimadas sem justificativa | 2 estimativas (vida útil) sem explicação | justificativa adicionada em `dados/premissas.json`; teste passou a exigir |
| Anos de retorno no formato `3.9` | ponto decimal confunde o público | formato brasileiro `3,9` em `energia/comparacao.py` |
