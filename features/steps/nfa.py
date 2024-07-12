"""Implementação dos testes para a simulação de DFA."""

from unittest.mock import patch, mock_open
from behave import given, when, then  # pylint: disable=no-name-in-module

import automata


@given("a descrição de um automato finito")
def _given_finite_automata_description(context):
    context.automata_description = context.text


@when("eu peço a validação das palavras")
def _when_run_automata(context):
    try:
        with patch(
            "builtins.open", mock_open(read_data=context.automata_description)
        ):
            nfa = automata.load_automata("fake_file.txt")
            dfa = automata.convert_to_dfa(nfa)
            context.result = automata.process(
                dfa, [w.strip() for w in context.text.split("\n")]
            )
    except Exception as ex:  # pylint: disable=broad-except
        context.exception = ex
        context.result = None
    else:
        context.exception = None


@then("nenhum erro ocorre na criação do automato")
def _then_no_exception(context):
    if context.exception:
        raise context.exception from None
    assert (
        context.exception is None
    ), f"Nenhuma exceção esperada mas encontrada: {str(context.exception)}"


@then("o resultado obtido é")
def _then_result_is(context):
    expected = {
        v[0].strip(): v[1].strip()
        for v in [w.split(":") for w in context.text.split("\n")]
    }
    assert (
        expected == context.result
    ), f"Expected: {expected}\nObserved: {context.result}"
