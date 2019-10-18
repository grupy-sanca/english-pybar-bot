import pytest

from questions_parser import parser_list


@pytest.mark.parametrize(
    "questions, expected_questions",
    [(["\n\n", " \na \n\n", "   "], ["a"]), ([" a", "a ", "a"], ["a", "a", "a"])],
)
def test_parser_list(questions, expected_questions):
    assert parser_list(questions) == expected_questions
