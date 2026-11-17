"""Linha de comando: listar, ver, corrigir, gabarito e medir."""

import argparse
import sys
from pathlib import Path

from .corretor import buscar, conectar, corrigir
from .exercicios import EXERCICIOS


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sql-do-zero", description="20 exercícios de SQL com correção automática")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("listar", help="lista os exercícios")
    ver = sub.add_parser("ver", help="mostra o enunciado")
    ver.add_argument("numero", type=int)
    cor = sub.add_parser("corrigir", help="corrige o arquivo .sql do aluno")
    cor.add_argument("numero", type=int)
    cor.add_argument("arquivo", type=Path)
    gab = sub.add_parser("gabarito", help="mostra a consulta do gabarito")
    gab.add_argument("numero", type=int)
    sub.add_parser("medir", help="roda todos os gabaritos e confere que se corrigem sozinhos")
    a = p.parse_args(argv)

    if a.cmd == "listar":
        for ex in EXERCICIOS:
            print(f"{ex.numero:2d}  [{ex.nivel}]  {ex.titulo}")
        return 0
    if a.cmd == "medir":
        con = conectar()
        ok = sum(corrigir(con, ex, ex.gabarito).ok for ex in EXERCICIOS)
        print(f"{ok}/{len(EXERCICIOS)} gabaritos corrigem como corretos")
        return 0 if ok == len(EXERCICIOS) else 1
    try:
        ex = buscar(a.numero)
    except KeyError as e:
        print(e.args[0], file=sys.stderr)
        return 2
    if a.cmd == "ver":
        print(f"{ex.numero}. {ex.titulo} [{ex.nivel}]\n\n{ex.enunciado}\n\nDica: {ex.dica}")
    elif a.cmd == "gabarito":
        print(ex.gabarito)
    else:
        if not a.arquivo.is_file():
            print(f"Arquivo não encontrado: {a.arquivo}", file=sys.stderr)
            return 2
        r = corrigir(conectar(), ex, a.arquivo.read_text(encoding="utf-8"))
        print(r.mensagem)
        return 0 if r.ok else 1
    return 0
