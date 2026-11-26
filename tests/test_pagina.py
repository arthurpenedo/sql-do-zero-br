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


def test_pagina_do_demo_tem_90_exercicios_e_indice_completo():
    html = gerar_pagina()
    assert len(EXERCICIOS) == 90
    assert "SQL do zero: 90 exercícios" in html
    assert html.count('<a href="#ex') == 90


def test_pagina_tem_filtro_por_nivel_sem_javascript():
    html = gerar_pagina()
    niveis = {e.nivel for e in EXERCICIOS}
    assert html.count('type="radio"') == len(niveis) + 1
    assert all(f'data-nivel="{n}"' in html for n in niveis)
    assert html.count(":checked~main section:not(") == len(niveis)
    assert "<script" not in html
    # os radios precisam ser irmãos de <main> para o seletor ~ funcionar
    assert html.index('id="f-todos"') < html.index("<main>")


def test_cli_demo_recusa_saida_que_e_pasta_ou_passa_por_arquivo(tmp_path, capsys):
    from sql_do_zero.cli import main

    arq = tmp_path / "arq.txt"
    arq.write_text("x")
    assert main(["demo", "--saida", str(tmp_path)]) == 2
    assert main(["demo", "--saida", str(arq / "x.html")]) == 2
    assert capsys.readouterr().err.count("--saida precisa") == 2
