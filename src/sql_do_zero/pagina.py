"""Página estática com os enunciados; o gabarito fica escondido num <details>."""

from html import escape

from .exercicios import EXERCICIOS, Exercicio


def _cartao(ex: Exercicio) -> str:
    return (
        f'<section id="ex{ex.numero}" data-nivel="{escape(ex.nivel, quote=True)}"><h2>{ex.numero}. {escape(ex.titulo)} '
        f'<small>[{escape(ex.nivel)}]</small></h2>'
        f"<p>{escape(ex.enunciado)}</p>"
        f"<p><em>Dica: {escape(ex.dica)}</em></p>"
        f"<details><summary>Ver gabarito</summary><pre>{escape(ex.gabarito)}</pre></details></section>"
    )


def _filtro(niveis: list[str]) -> tuple[str, str]:
    """Filtro por nível só com CSS (radio + :checked), sem JavaScript."""
    radios = '<input type="radio" name="f" id="f-todos" checked><label for="f-todos">todos</label>'
    regras = ""
    for i, n in enumerate(niveis):
        radios += f'<input type="radio" name="f" id="f{i}"><label for="f{i}">{escape(n)}</label>'
        alvo = escape(n, quote=True).replace("\\", "\\\\")
        regras += f'#f{i}:checked~main section:not([data-nivel="{alvo}"]),#f{i}:checked~ol li:not([data-nivel="{alvo}"]){{display:none}}'
    regras += "input[type=radio]{margin-left:.6rem}"
    return radios, regras


def gerar_pagina(exercicios: list[Exercicio] | None = None) -> str:
    """HTML único, sem JavaScript e sem dependências externas."""
    lista = EXERCICIOS if exercicios is None else exercicios
    indice = "".join(f'<li data-nivel="{escape(e.nivel, quote=True)}"><a href="#ex{e.numero}">{e.numero}. {escape(e.titulo)}</a></li>' for e in lista)
    niveis = list(dict.fromkeys(e.nivel for e in lista))
    radios, regras = _filtro(niveis)
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>SQL do zero</title><style>"
        "body{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem;line-height:1.5}"
        "section{border-top:1px solid #ccc;padding:.5rem 0}small{color:#666}"
        "pre{background:#f4f4f4;padding:.6rem;overflow-x:auto;white-space:pre-wrap}"
        f"{regras}</style></head><body>"
        f"<h1>SQL do zero: {len(lista)} exercícios</h1>"
        "<p>Vagas reais de tecnologia, correção automática em DuckDB. Tente antes de abrir o gabarito.</p>"
        f"<span>Filtrar por nível:</span>{radios}"
        f"<ol>{indice}</ol><main>{''.join(_cartao(e) for e in lista)}</main></body></html>"
    )
