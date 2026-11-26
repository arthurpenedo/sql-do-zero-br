from sql_do_zero.cli import main
from sql_do_zero.exercicios import EXERCICIOS
from sql_do_zero.lote import sortear


def test_sortear_com_semente_repete_o_resultado():
    assert sortear(EXERCICIOS, semente=7) == sortear(EXERCICIOS, semente=7)


def test_sortear_respeita_o_nivel():
    for semente in range(20):
        assert sortear(EXERCICIOS, "case", semente).nivel == "case"


def test_sortear_nivel_inexistente_devolve_none():
    assert sortear(EXERCICIOS, "nao-existe", 1) is None


def test_cli_sortear_mostra_enunciado_sem_gabarito(capsys):
    assert main(["sortear", "--nivel", "case", "--semente", "3"]) == 0
    saida = capsys.readouterr().out
    ex = sortear(EXERCICIOS, "case", 3)
    assert saida.startswith(f"{ex.numero}. {ex.titulo}") and "Dica:" in saida
    assert "SELECT" not in saida.split("Dica:")[0]


def test_cli_sortear_nivel_inexistente_da_erro(capsys):
    assert main(["sortear", "--nivel", "xyz"]) == 2
    cap = capsys.readouterr()
    assert cap.out == "" and "Nível desconhecido: xyz" in cap.err
