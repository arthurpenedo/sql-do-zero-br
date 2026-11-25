"""Linha de comando: listar, ver, corrigir, gabarito e medir."""

import argparse
import sys
from pathlib import Path

from .corretor import buscar, conectar, corrigir
from .exercicios import EXERCICIOS
from .lote import (
    agrupar_por_nivel,
    carregar,
    corrigir_pasta,
    registrar,
    resumo_progresso,
)
from .pagina import gerar_pagina


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sql-do-zero", description="60 exercícios de SQL com correção automática")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("listar", help="lista os exercícios")
    ver = sub.add_parser("ver", help="mostra o enunciado")
    ver.add_argument("numero", type=int)
    cor = sub.add_parser("corrigir", help="corrige o arquivo .sql do aluno")
    cor.add_argument("numero", type=int, nargs="?")
    cor.add_argument("arquivo", type=Path, nargs="?")
    cor.add_argument("--todos", type=Path, metavar="PASTA", help="corrige todos os NN*.sql da pasta")
    cor.add_argument("--tentativas", type=Path, metavar="JSON", help="guarda as tentativas por exercício")
    gab = sub.add_parser("gabarito", help="mostra a consulta do gabarito")
    gab.add_argument("numero", type=int)
    pro = sub.add_parser("progresso", help="resume o JSON de --tentativas: acertos, pendentes e média")
    pro.add_argument("arquivo", type=Path)
    sub.add_parser("niveis", help="mostra os níveis, quantos exercícios e quais números")
    sub.add_parser("medir", help="roda todos os gabaritos e confere que se corrigem sozinhos")
    dem = sub.add_parser("demo", help="gera a página HTML com os enunciados (gabarito escondido)")
    dem.add_argument("--saida", type=Path, default=Path("site/index.html"))
    a = p.parse_args(argv)

    if a.cmd == "listar":
        for ex in EXERCICIOS:
            print(f"{ex.numero:2d}  [{ex.nivel}]  {ex.titulo}")
        return 0
    if a.cmd == "demo" and (a.saida.is_dir() or any(q.is_file() for q in a.saida.parents)):
        print(f"--saida precisa ser um arquivo .html num caminho válido: {a.saida}", file=sys.stderr)
        return 2
    if a.cmd == "niveis":
        for nivel, numeros in agrupar_por_nivel(EXERCICIOS).items():
            print(f"{nivel:14s} {len(numeros):2d}  {', '.join(map(str, numeros))}")
        return 0
    if a.cmd == "demo":
        a.saida.parent.mkdir(parents=True, exist_ok=True)
        a.saida.write_text(gerar_pagina(), encoding="utf-8")
        print(f"Página gerada em {a.saida}")
        return 0
    if a.cmd == "progresso":
        if not a.arquivo.is_file():
            print(f"Arquivo não encontrado: {a.arquivo}", file=sys.stderr)
            return 2
        r = resumo_progresso(carregar(a.arquivo), {e.numero: e.nivel for e in EXERCICIOS})
        print(f"{len(r['acertados'])}/{len(EXERCICIOS)} exercícios resolvidos")
        for nivel, (total, ok) in r["por_nivel"].items():
            print(f"  {nivel:13s} {ok}/{total}")
        if r["media_tentativas"] is not None:
            print(f"Média de tentativas até acertar: {r['media_tentativas']}")
        if r["pendentes"]:
            print("Próximo a tentar: " + ", ".join(map(str, r["pendentes"][:5])))
        return 0
    if a.cmd == "medir":
        con = conectar()
        ok = sum(corrigir(con, ex, ex.gabarito).ok for ex in EXERCICIOS)
        print(f"{ok}/{len(EXERCICIOS)} gabaritos corrigem como corretos")
        return 0 if ok == len(EXERCICIOS) else 1
    if a.cmd == "corrigir" and a.todos:
        if not a.todos.is_dir():
            print(f"Pasta não encontrada: {a.todos}", file=sys.stderr)
            return 2
        res = corrigir_pasta(conectar(), a.todos)
        for numero, ok, msg in res:
            print(f"{numero:2d}  {'ok  ' if ok else 'erro'}  {msg}")
            if a.tentativas and any(e.numero == numero for e in EXERCICIOS):
                registrar(a.tentativas, numero, ok)
        certos = sum(ok for _, ok, _ in res)
        print(f"{certos}/{len(res)} corretos")
        return 0 if res and certos == len(res) else 1
    if a.numero is None:
        print("Informe o número do exercício (ou use --todos PASTA).", file=sys.stderr)
        return 2
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
        if a.arquivo is None or not a.arquivo.is_file():
            print(f"Arquivo não encontrado: {a.arquivo}", file=sys.stderr)
            return 2
        r = corrigir(conectar(), ex, a.arquivo.read_text(encoding="utf-8"))
        print(r.mensagem)
        if a.tentativas:
            registrar(a.tentativas, ex.numero, r.ok)
        return 0 if r.ok else 1
    return 0
