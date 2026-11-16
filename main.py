"""Citizen Assist AI – módulo de Energia (GS 2026.2, Soluções em Energias Renováveis e Sustentáveis).

Uso:
    py main.py                          # menu interativo
    py main.py --pergunta "quanto meu chuveiro gasta?"
    py main.py --relatorio              # gera docs/resultados.md e dados/resultados.json
"""
import argparse
import sys

from energia import calculos as calc
from energia import comparacao as cmp
from energia.assistente import AssistenteEnergia
from energia.relatorio import salvar

MENU = """
==== Citizen Assist AI – Energia no banho e na conta de luz ====
1. Fazer uma pergunta ao assistente
2. Simular a minha casa
3. Ver comparação das alternativas
4. Fontes e limitações
0. Sair
"""


def ler_numero(rotulo: str, minimo: float, maximo: float, padrao: float, entrada=input) -> float:
    """Lê um número validado; Enter usa o valor padrão."""
    while True:
        bruto = entrada(f"{rotulo} [{padrao:g}]: ").strip().replace(",", ".")
        if not bruto:
            return padrao
        try:
            valor = float(bruto)
        except ValueError:
            print("  Digite um número (ex.: 8 ou 7,5).")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"  Valor deve estar entre {minimo:g} e {maximo:g}.")


def ler_sim_nao(rotulo: str, padrao: bool, entrada=input) -> bool:
    while True:
        bruto = entrada(f"{rotulo} (s/n) [{'s' if padrao else 'n'}]: ").strip().lower()
        if not bruto:
            return padrao
        if bruto in ("s", "sim"):
            return True
        if bruto in ("n", "nao", "não"):
            return False
        print("  Responda s ou n.")


def simular(assistente: AssistenteEnergia, entrada=input) -> AssistenteEnergia:
    """Coleta os dados da casa e devolve um novo assistente para essa situação."""
    atual = assistente.entrada
    p = atual.perfil
    print("\nResponda com os dados da sua casa (Enter mantém o valor do cenário de referência).")
    print("Não pedimos nome, endereço nem documento.")
    moradores = int(ler_numero("Quantas pessoas tomam banho em casa", 1, 20, p.moradores, entrada))
    duracao = ler_numero("Duração média do banho (min)", 1, 60, p.duracao_min, entrada)
    inverno = ler_numero("Potência do chuveiro na posição inverno (W, veja a etiqueta)", 1000, 10000,
                         p.potencia_inverno_w, entrada)
    verao = ler_numero("Potência na posição verão (W)", 500, inverno, min(p.potencia_verao_w, inverno), entrada)
    meses = ler_numero("Quantos meses por ano usa a posição inverno", 0, 12, p.meses_inverno, entrada)
    perfil = calc.PerfilBanho(moradores, p.banhos_por_pessoa_dia, duracao, inverno, verao, meses, p.dias_por_mes)
    chuveiro = calc.consumo_chuveiro_kwh_mes(perfil)
    print(f"  O chuveiro sozinho gasta cerca de {chuveiro:.0f} kWh/mês; a conta não pode ser menor que isso.")
    total = ler_numero("Consumo total da conta (kWh/mês, está na fatura)", round(chuveiro, 1), 5000,
                       max(atual.consumo_total_kwh_mes, round(chuveiro, 1)), entrada)
    social = ler_sim_nao("Recebe Tarifa Social de energia", atual.tarifa_social, entrada)
    propria = ler_sim_nao("A casa é própria", atual.casa_propria, entrada)
    telhado = ler_sim_nao("O telhado recebe sol a maior parte do dia", atual.telhado_com_sol, entrada)
    novo = assistente.com_entrada(cmp.Entrada(perfil, total, social, propria, telhado))
    print("\n" + novo.responder("qual a melhor opção para mim?").formatar())
    return novo


def conversar(assistente: AssistenteEnergia, entrada=input) -> None:
    print("\nDigite sua pergunta (ou 'voltar').")
    print(assistente.responder("ajuda").formatar())
    while True:
        pergunta = entrada("\nVocê: ").strip()
        if pergunta.lower() in ("voltar", "sair", "0"):
            return
        print("\nAssistente:\n" + assistente.responder(pergunta).formatar())


def menu(assistente: AssistenteEnergia, entrada=input) -> None:
    while True:
        print(MENU)
        opcao = entrada("Opção: ").strip()
        if opcao == "1":
            conversar(assistente, entrada)
        elif opcao == "2":
            assistente = simular(assistente, entrada)
        elif opcao == "3":
            print(assistente.responder("comparar alternativas").formatar())
        elif opcao == "4":
            print(assistente.responder("quais as fontes?").formatar())
            print(assistente.responder("isso é garantido?").formatar())
        elif opcao == "0":
            print("Até logo!")
            return
        else:
            print("Opção inválida. Escolha 0 a 4.")


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Citizen Assist AI – módulo de energia")
    parser.add_argument("--pergunta", help="responde uma pergunta e sai")
    parser.add_argument("--relatorio", action="store_true", help="gera docs/resultados.md e dados/resultados.json")
    args = parser.parse_args(argv)

    try:
        assistente = AssistenteEnergia()
    except (FileNotFoundError, ValueError, KeyError) as erro:
        print(f"Erro ao carregar as premissas: {erro}", file=sys.stderr)
        return 1

    if args.relatorio:
        for caminho in salvar(assistente):
            print(f"Gerado: {caminho}")
        return 0
    if args.pergunta:
        print(assistente.responder(args.pergunta).formatar())
        return 0
    try:
        menu(assistente)
    except (EOFError, KeyboardInterrupt):
        print("\nEncerrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
