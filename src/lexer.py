import re


class Reader:
    """
    Receives a python file and normalize the lines
    """
    @staticmethod
    def _unfinished_line(line: str) -> bool:
        brackets = (
            ('{', '}'),
            ('(', ')'),
            ('[', ']')
        )

        for open_bracket, close_bracket in brackets:
            has_open_bracket = re.search(fr'.*\{open_bracket}', line)
            has_open_and_close_brackets = re.search(
                fr'.*\{open_bracket}.*\{close_bracket}', line
            )
            if has_open_bracket and not has_open_and_close_brackets:
                return True

        return False

    @classmethod
    def normalize(cls, code: list[str]) -> list[str]:
        for i, line in enumerate(code):
            next_line_i = i + 1

            while cls._unfinished_line(line) and next_line_i != len(code):
                code[i] += code.pop(next_line_i).strip()

        return code


class Tokenizer:
    """
    Get a python code and organize the lines into tokens
    """
    pass


class Lexer:
    pass
