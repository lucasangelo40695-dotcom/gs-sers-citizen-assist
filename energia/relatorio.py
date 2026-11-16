"""Gera docs/resultados.md e dados/resultados.json a partir do MESMO código
que responde no assistente, garantindo coerência entre análise e respostas."""
import json
import os
from dataclasses import asdict

from energia import comparacao as cmp
from energia.assistente import AssistenteEnergia, num, pct, reais
from energia.premissas import RAIZ

ARQ_MD = os.path.join(RAIZ, "docs", "resultados.md")
ARQ_JSON = os.path.join(RAIZ, "dados", "resultados.json")


def _tabela_premissas(premissas) -> list[str]:
    linhas = ["| Premissa | Valor | Unidade | Tipo | Fonte / justificativa |", "|---|---|---|---|---|"]
    for p in premissas.values():
        origem = p.fonte or p.observacao
        if p.fonte and p.observacao:
            origem = f"{p.fonte}. {p.observacao}"
        linhas.append(f"| `{p.chave}` | {num(p.valor, 4).rstrip('0').rstrip(',')} | {p.unidade} | "
                      f"{p.rotulo_tipo} | {origem} |")
    return linhas


def gerar_markdown(assistente: AssistenteEnergia) -> str:
    c, alts = assistente.analise()
    v = assistente.v
    linhas = [
        "# Resultados da análise de energia (gerado por `py main.py --relatorio`)",
        "",
        "> Arquivo gerado automaticamente pelo mesmo código que responde no assistente. "
        "Não editar à mão: altere `dados/premissas.json` e gere de novo.",
        "",
        "## 1. Situação atual (cenário de referência)",
        "",
        f"* Família de {assistente.entrada.perfil.moradores} pessoas, banho de "
        f"{num(assistente.entrada.perfil.duracao_min, 0)} min, chuveiro de "
        f"{num(v['potencia_chuveiro_inverno_w'], 0)} W (inverno) / {num(v['potencia_chuveiro_verao_w'], 0)} W (verão).",
        f"* Potência média anual: {num(cmp.calc.potencia_media_w(assistente.entrada.perfil), 0)} W.",
        f"* Consumo do chuveiro: **{num(c.consumo_chuveiro_kwh_mes)} kWh/mês** "
        f"({num(c.consumo_chuveiro_kwh_mes * 12, 0)} kWh/ano), {pct(c.participacao_chuveiro)} da conta de "
        f"{num(c.consumo_total_kwh_mes, 0)} kWh/mês.",
        f"* Tarifa estimada com tributos: **R$ {num(c.tarifa, 4)}/kWh** "
        f"= {num(v['tarifa_b1_vigente_sem_tributos'], 3)} / (1 − {num(v['tributos_fracao'], 2)}).",
        f"* Custo anual do chuveiro: **{reais(c.custo_chuveiro_ano)}**; emissão: {num(c.emissao_chuveiro_kg_ano)} kgCO2/ano.",
        f"* Verificação física (Q = m·c·ΔT): vazão aquecível {num(c.vazao_l_min, 2)} L/min, "
        f"{num(c.vazao_l_min * assistente.entrada.perfil.duracao_min, 0)} L por banho, "
        f"{num(c.energia_termica_banho_kwh, 3)} kWh de calor para {num(c.energia_eletrica_banho_kwh, 3)} kWh elétricos "
        f"(eficiência {pct(v['eficiencia_chuveiro'])}).",
        "",
        "## 2. Comparação das alternativas (mesma necessidade, 12 meses; saldo em "
        f"{num(v['horizonte_anos'], 0)} anos)",
        "",
        "| | Alternativa | Renovável | Investimento | Manutenção/ano | kWh/ano a menos na rede | "
        "Cobertura do chuveiro | Economia líquida/ano | Retorno | Saldo no horizonte | CO2 evitado/ano |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for a in alts:
        retorno = ("imediato" if a.investimento == 0 else f"{num(a.payback_anos)} anos" if a.se_paga
                   else "não se paga na vida útil")
        linhas.append(
            f"| {a.codigo} | {a.nome} | {'sim' if a.renovavel else 'não'} | {reais(a.investimento)} | "
            f"{reais(a.manutencao_ano)} | {num(a.reducao_kwh_ano, 0)} | {pct(a.cobertura_chuveiro)} | "
            f"{reais(a.economia_liquida_ano)} | {retorno} | {reais(a.saldo_horizonte)} | {num(a.co2_evitado_kg_ano)} kg |")
    linhas += ["", "## 3. Viabilidade, impactos ambientais e limitações", ""]
    for a in alts:
        linhas += [f"### {a.codigo} – {a.nome}", "", "**Viabilidade**", ""] + [f"* {t}" for t in a.viabilidade]
        linhas += ["", "**Impactos ambientais**", ""] + [f"* {t}" for t in a.impactos]
        linhas += ["", "**Limitações**", ""] + [f"* {t}" for t in a.limitacoes] + [""]
    linhas += ["## 4. Recomendação gerada pelo assistente", ""]
    linhas += [f"{i}. {p}" for i, p in enumerate(cmp.recomendar(assistente.entrada, alts), 1)]
    linhas += ["", "## 5. Premissas (origem, unidade e tipo)", ""] + _tabela_premissas(assistente.premissas)
    return "\n".join(linhas) + "\n"


def gerar_json(assistente: AssistenteEnergia) -> dict:
    c, alts = assistente.analise()
    return {"cenario": asdict(c), "alternativas": [asdict(a) for a in alts],
            "recomendacao": list(cmp.recomendar(assistente.entrada, alts))}


def salvar(assistente: AssistenteEnergia) -> tuple[str, str]:
    with open(ARQ_MD, "w", encoding="utf-8") as arquivo:
        arquivo.write(gerar_markdown(assistente))
    with open(ARQ_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(gerar_json(assistente), arquivo, ensure_ascii=False, indent=2)
    return ARQ_MD, ARQ_JSON
