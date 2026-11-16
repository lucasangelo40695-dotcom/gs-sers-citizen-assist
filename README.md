# Citizen Assist AI – Energia no banho e na conta de luz

**Contribuição da disciplina Soluções em Energias Renováveis e Sustentáveis (SERS)** ao desafio Citizen Assist AI –
Global Solution 2026.2, Ciência da Computação (1CC).

O módulo `energia/` acrescenta ao assistente orientações sobre uso consciente de energia para o **banho com chuveiro
elétrico**, baseadas em dados, cálculos e fontes verificáveis.

## Integrantes

| Nome completo | RM |
|---|---|
| Lucas Angelo | 569530 |
| Gustavo Guedes | 569779 |
| Gabriel Rodrigues | 569322 |

## Público e problema

* **Público:** famílias de baixa renda na área da Enel SP, em casas com chuveiro elétrico.
* **Necessidade energética:** água quente para o banho. Na família de referência (4 pessoas) o chuveiro gasta
  **72 kWh/mês, 40% da conta, cerca de R$ 821/ano**.
* **Alternativas comparadas** para a mesma necessidade em 12 meses (saldo em 10 anos):
  **A** hábitos e eficiência · **B** aquecedor solar de água (renovável) · **C** solar fotovoltaica (renovável).

| | Investimento | Economia líquida/ano | Retorno | CO2 evitado/ano |
|---|---|---|---|---|
| A – Hábitos | R$ 0 | R$ 346 | imediato | 17 kg |
| B – Aquecedor solar | R$ 5.538 | R$ 495 | ~11 anos | 28 kg |
| C – Fotovoltaica 1,1 kWp | R$ 6.156 | R$ 1.016 | ~6,1 anos | 64 kg |

*Estimativas para as premissas de `dados/premissas.json`, não resultados garantidos.* Detalhes em [docs/analise.md](docs/analise.md).

## Funcionalidades de energia no assistente

* **Perguntas em linguagem natural** (com ou sem acento): consumo do chuveiro, dicas de economia, aquecedor solar, painel
  fotovoltaico, comparação/recomendação, aluguel, Tarifa Social, o que é kWh, impacto ambiental, como foi calculado,
  fontes e limitações. Perguntas como "e se eu tomar banho de 10 minutos?" ou "somos 6 pessoas" são recalculadas na hora.
* **Toda resposta** traz os números da análise, as **fontes** e um bloco **"Atenção"** com as limitações.
* **Simulador da casa**: recalcula consumo, custo, retorno e recomendação com os dados do usuário, sem pedir dados pessoais.
  Considera Tarifa Social (gratuidade até 80 kWh), casa própria/aluguel e sol no telhado.
* **Relatório coerente**: `docs/resultados.md` é gerado pelo mesmo código das respostas.

## Como executar

Requer Python 3.10 ou superior, só com a biblioteca padrão (nada para instalar).

```bash
py main.py
```

```bash
py main.py --pergunta "vale a pena aquecedor solar?"
```

```bash
py main.py --relatorio
```

```bash
py -m unittest discover -s tests -t .
```

No Linux/macOS use `python3` no lugar de `py`.

## Entregáveis do enunciado → onde estão

| Exigência (PDF da GS) | Arquivo |
|---|---|
| Definição do contexto (público, necessidade, contribuição) | [docs/contexto.md](docs/contexto.md) |
| Dados utilizados, com origem, unidades, período e premissas (estimados identificados) | [dados/premissas.json](dados/premissas.json), seção 5 de [docs/resultados.md](docs/resultados.md) |
| Cálculos e comparação das alternativas | [energia/calculos.py](energia/calculos.py), [energia/comparacao.py](energia/comparacao.py), [docs/resultados.md](docs/resultados.md) |
| Justificativas (custos, viabilidade, impactos ambientais) | [docs/analise.md](docs/analise.md) |
| Integração ao assistente | [energia/assistente.py](energia/assistente.py), [main.py](main.py) |
| Referências e limitações | [docs/referencias.md](docs/referencias.md), [energia/referencias.py](energia/referencias.py), seção 5 de [docs/analise.md](docs/analise.md) |
| Testes com usuários e ajustes | [docs/testes_usuarios.md](docs/testes_usuarios.md): teste com Entrevistado 1, 2 e 3, 8 problemas encontrados e corrigidos |
| Códigos desenvolvidos e testes automatizados | `energia/`, `tests/` (41 testes) |

## Estrutura

```
main.py                  menu, simulador e linha de comando
energia/
  premissas.py           carrega dados/premissas.json (valor, unidade, tipo, fonte)
  calculos.py            E = P·t, Q = m·c·ΔT, tarifa, Tarifa Social, geração FV, CO2, payback
  comparacao.py          alternativas A, B, C + recomendação
  assistente.py          intenções, respostas com fontes e limitações
  referencias.py         referências verificáveis citadas nas respostas
  relatorio.py           gera docs/resultados.md e dados/resultados.json
dados/                   premissas.json (entrada) e resultados.json (saída)
docs/                    contexto, análise, resultados, referências, testes com usuários
tests/                   unittest
```
