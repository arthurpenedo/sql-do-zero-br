import pytest

from sql_do_zero.cli import main
from sql_do_zero.corretor import buscar, conectar, corrigir
from sql_do_zero.exercicios import EXERCICIOS


@pytest.fixture(scope="module")
def con():
    return conectar()


def test_tem_130_exercicios_numerados():
    assert [e.numero for e in EXERCICIOS] == list(range(1, 131))


@pytest.mark.parametrize("ex", EXERCICIOS, ids=lambda e: "ex" + str(e.numero))
def test_gabarito_se_corrige_como_certo(con, ex):
    assert corrigir(con, ex, ex.gabarito).ok


def test_resposta_errada_aponta_a_diferenca(con):
    r = corrigir(con, buscar(1), "SELECT COUNT(*) + 1 FROM vagas")
    assert not r.ok and "Valores diferentes" in r.mensagem


def test_ordem_nao_importa_quando_nao_ordenado(con):
    r = corrigir(con, buscar(7), "SELECT modelo, COUNT(*) AS t FROM vagas GROUP BY modelo ORDER BY modelo DESC")
    assert r.ok


def test_ordem_importa_quando_ordenado(con):
    r = corrigir(con, buscar(3), "SELECT titulo FROM vagas WHERE modelo = 'remoto' ORDER BY titulo DESC")
    assert not r.ok


def test_colunas_a_mais_sao_apontadas(con):
    r = corrigir(con, buscar(2), "SELECT titulo, empresa, id FROM vagas WHERE nivel = 'estágio'")
    assert not r.ok and "colunas" in r.mensagem


@pytest.mark.parametrize("sql", ["DROP TABLE vagas", "DELETE FROM vagas", "SELECT 1; DROP TABLE vagas", ""])
def test_comandos_que_mudam_dados_sao_barrados(con, sql):
    assert not corrigir(con, buscar(1), sql).ok
    assert con.execute("SELECT COUNT(*) FROM vagas").fetchone()[0] > 0


def test_erro_de_sintaxe_vira_mensagem(con):
    r = corrigir(con, buscar(1), "SELECT FROM WHERE")
    assert not r.ok and "DuckDB" in r.mensagem


def test_exercicio_inexistente():
    with pytest.raises(KeyError):
        buscar(131)


def test_cli_medir_e_corrigir(tmp_path, capsys):
    assert main(["medir"]) == 0
    arq = tmp_path / "r.sql"
    arq.write_text("SELECT COUNT(*) FROM vagas;", encoding="utf-8")
    assert main(["corrigir", "1", str(arq)]) == 0
    assert "Correto" in capsys.readouterr().out
    assert main(["corrigir", "1", str(tmp_path / "nao.sql")]) == 2
    assert main(["ver", "131"]) == 2
