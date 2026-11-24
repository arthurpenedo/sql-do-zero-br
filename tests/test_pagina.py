from sql_do_zero.cli import main
from sql_do_zero.exercicios import EXERCICIOS, Exercicio
from sql_do_zero.pagina import gerar_pagina


def test_pagina_tem_todos_os_exercicios_e_gabarito_escondido():
    html = gerar_pagina()
    assert html.count("<details>") == len(EXERCICIOS)
    assert all(f'id="ex{e.numero}"' in html for e in EXERCICIOS)
    assert "<script" not in html


def test_pagina_escapa_html():
    ex = Exercicio(1, "básico", "a <b>", "x < y & z", "d", "SELECT '<i>'")
    html = gerar_pagina([ex])
    assert "<b>" not in html and "&lt;b&gt;" in html and "&lt;i&gt;" in html


def test_cli_demo_grava_arquivo(tmp_path):
    saida = tmp_path / "s" / "index.html"
    assert main(["demo", "--saida", str(saida)]) == 0
    assert "SQL do zero" in saida.read_text(encoding="utf-8")


def test_pagina_do_demo_tem_45_exercicios_e_indice_completo():
    html = gerar_pagina()
    assert len(EXERCICIOS) == 45
    assert "SQL do zero: 45 exercícios" in html
    assert html.count('<li><a href="#ex') == 45
