from pathlib import Path

from sql_do_zero.cli import main
from sql_do_zero.exercicios import EXERCICIOS
from sql_do_zero.lote import agrupar_por_nivel


def test_agrupar_por_nivel_cobre_todos_os_exercicios():
    r = agrupar_por_nivel(EXERCICIOS)
    assert sorted(n for nums in r.values() for n in nums) == [e.numero for e in EXERCICIOS]
    assert r["básico"][0] == 1


def test_cli_niveis_lista_cada_nivel_com_contagem(capsys):
    assert main(["niveis"]) == 0
    linhas = capsys.readouterr().out.splitlines()
    assert len(linhas) == len(agrupar_por_nivel(EXERCICIOS))
    assert linhas[0].startswith("básico")


def test_cli_dica_mostra_so_a_dica(capsys):
    assert main(["dica", "6"]) == 0
    assert capsys.readouterr().out.strip() == "GROUP BY e ORDER BY ... DESC"


def test_cli_dica_de_exercicio_inexistente_da_erro(capsys):
    assert main(["dica", "999"]) == 2
    assert capsys.readouterr().out == ""


def test_readme_tem_tabela_de_niveis_atualizada():
    readme = (Path(__file__).parent.parent / "README.md").read_text(encoding="utf-8")
    for nivel, nums in agrupar_por_nivel(EXERCICIOS).items():
        assert f"| {nivel} | {len(nums)} |" in readme
