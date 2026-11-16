"""Carrega as premissas de dados/premissas.json.

Cada premissa guarda valor, unidade, tipo (real, estimado ou hipotese),
fonte e observação, para que o assistente possa citar de onde veio cada número.
"""
import json
import os
from dataclasses import dataclass
from types import MappingProxyType

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_PREMISSAS = os.path.join(RAIZ, "dados", "premissas.json")
TIPOS_VALIDOS = ("real", "estimado", "hipotese")


@dataclass(frozen=True)
class Premissa:
    chave: str
    valor: float
    unidade: str
    tipo: str
    fonte: str = ""
    observacao: str = ""

    def __post_init__(self):
        if self.tipo not in TIPOS_VALIDOS:
            raise ValueError(f"Premissa '{self.chave}': tipo inválido '{self.tipo}'")
        if not isinstance(self.valor, (int, float)) or self.valor < 0:
            raise ValueError(f"Premissa '{self.chave}': valor deve ser número não negativo")

    @property
    def rotulo_tipo(self):
        return {"real": "dado real", "estimado": "ESTIMATIVA", "hipotese": "hipótese do cenário"}[self.tipo]


def carregar_premissas(caminho=ARQUIVO_PREMISSAS):
    """Lê o JSON e devolve um mapeamento somente leitura chave -> Premissa."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            bruto = json.load(arquivo)
    except FileNotFoundError as erro:
        raise FileNotFoundError(f"Arquivo de premissas não encontrado: {caminho}") from erro
    except json.JSONDecodeError as erro:
        raise ValueError(f"Arquivo de premissas inválido ({caminho}): {erro}") from erro

    premissas = {}
    for chave, dados in bruto.items():
        if chave.startswith("_"):
            continue
        premissas[chave] = Premissa(
            chave=chave,
            valor=dados["valor"],
            unidade=dados["unidade"],
            tipo=dados["tipo"],
            fonte=dados.get("fonte", ""),
            observacao=dados.get("observacao", ""),
        )
    return MappingProxyType(premissas)


def valores(premissas):
    """Atalho: dicionário chave -> valor numérico."""
    return {chave: p.valor for chave, p in premissas.items()}
