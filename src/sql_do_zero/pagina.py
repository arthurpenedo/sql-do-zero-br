"""Página estática com os enunciados; o gabarito fica escondido num <details>."""

from html import escape

from .exercicios import EXERCICIOS, Exercicio


def _cartao(ex: Exercicio) -> str:
    return (
        f'<section id="ex{ex.numero}"><h2>{ex.numero}. {escape(ex.titulo)} '
        f'<small>[{escape(ex.nivel)}]</small></h2>'
        f"<p>{escape(ex.enunciado)}</p>"
        f"<p><em>Dica: {escape(ex.dica)}</em></p>"
        f"<details><summary>Ver gabarito</summary><pre>{escape(ex.gabarito)}</pre></details></section>"
    )


def gerar_pagina(exercicios: list[Exercicio] | None = None) -> str:
    """HTML único, sem JavaScript e sem dependências externas."""
    lista = EXERCICIOS if exercicios is None else exercicios
    indice = "".join(f'<li><a href="#ex{e.numero}">{e.numero}. {escape(e.titulo)}</a></li>' for e in lista)
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>SQL do zero</title><style>"
        "body{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem;line-height:1.5}"
        "section{border-top:1px solid #ccc;padding:.5rem 0}small{color:#666}"
        "pre{background:#f4f4f4;padding:.6rem;overflow-x:auto;white-space:pre-wrap}"
        "</style></head><body>"
        f"<h1>SQL do zero: {len(lista)} exercícios</h1>"
        "<p>Vagas reais de tecnologia, correção automática em DuckDB. Tente antes de abrir o gabarito.</p>"
        f"<ol>{indice}</ol>{''.join(_cartao(e) for e in lista)}</body></html>"
    )
