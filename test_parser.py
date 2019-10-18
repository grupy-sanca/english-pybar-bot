import pytest

from questions_parser import parser_list


@pytest.fixture
def questions():
    return [" a", "a ", " a "]


def test_parser_list(questions):
    assert parser_list(questions) == ["a", "a", "a"]
