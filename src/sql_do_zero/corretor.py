"""Corretor automático: roda a consulta do aluno e a do gabarito no DuckDB e compara."""

from dataclasses import dataclass
from pathlib import Path

import duckdb

from .exercicios import EXERCICIOS, Exercicio

DADOS = Path(__file__).resolve().parents[2] / "dados"
PROIBIDAS = ("insert", "update", "delete", "drop", "create", "alter", "attach", "copy", "pragma")


@dataclass
class Resultado:
    ok: bool
    mensagem: str


def conectar(pasta: Path = DADOS) -> duckdb.DuckDBPyConnection:
    """Banco em memória com as tabelas `vagas` e `vaga_skill` lidas dos CSVs."""
    con = duckdb.connect()
    for tabela in ("vagas", "vaga_skill"):
        caminho = (pasta / f"{tabela}.csv").as_posix().replace("'", "''")
        con.execute(f"CREATE TABLE {tabela} AS SELECT * FROM read_csv_auto('{caminho}')")
    return con


def buscar(numero: int) -> Exercicio:
    for ex in EXERCICIOS:
        if ex.numero == numero:
            return ex
    raise KeyError(f"exercício {numero} não existe (1 a {len(EXERCICIOS)})")


def _validar(sql: str) -> str | None:
    """Só aceita um SELECT (ou WITH). Devolve a mensagem de erro ou None."""
    limpo = sql.strip().rstrip(";").strip()
    if not limpo:
        return "A consulta está vazia."
    if ";" in limpo:
        return "Envie uma única consulta (sem ponto e vírgula no meio)."
    primeira = limpo.split(None, 1)[0].lower()
    if primeira not in ("select", "with"):
        return "Só consultas SELECT (ou WITH) são aceitas."
    palavras = {p.strip("(),").lower() for p in limpo.split()}
    if palavras & set(PROIBIDAS):
        return "A consulta usa um comando que muda dados; aqui só se lê."
    return None


def _linhas(con, sql: str):
    cursor = con.execute(sql)
    colunas = [c[0] for c in cursor.description]
    return colunas, cursor.fetchall()


def _chave(linha):
    return tuple((v is None, str(v)) for v in linha)


def corrigir(con, ex: Exercicio, sql_aluno: str) -> Resultado:
    erro = _validar(sql_aluno)
    if erro:
        return Resultado(False, erro)
    try:
        _, obtido = _linhas(con, sql_aluno.strip().rstrip(";"))
    except duckdb.Error as e:
        return Resultado(False, f"Erro do DuckDB: {str(e).splitlines()[0]}")
    _, esperado = _linhas(con, ex.gabarito)
    if obtido and esperado and len(obtido[0]) != len(esperado[0]):
        return Resultado(False, f"Número de colunas diferente: esperado {len(esperado[0])}, "
                                f"veio {len(obtido[0])}.")
    if not ex.ordenado:
        obtido, esperado = sorted(obtido, key=_chave), sorted(esperado, key=_chave)
    if len(obtido) != len(esperado):
        return Resultado(False, f"Número de linhas diferente: esperado {len(esperado)}, "
                                f"veio {len(obtido)}.")
    if obtido != esperado:
        for a, b in zip(obtido, esperado, strict=True):
            if a != b:
                return Resultado(False, f"Valores diferentes: esperado {b}, veio {a}.")
    return Resultado(True, "Correto!")
