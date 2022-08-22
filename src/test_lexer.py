from .lexer import Reader, Tokenizer


class TestLexer:
    def test_normalize_multiple_lines_code(self):
        code = """variable = some_function(
                    param1,
                    param2,
                    param3
            )""".split('\n')

        normalized_code = Reader.normalize(code)

        assert (
            ['variable = some_function(param1,param2,param3)'] == normalized_code
        )

    def test_normalize_code_multiple_brackets(self):
        code = """variable = some_function(another_function(
                        param1,
                        param2
                    ),
                    param3
                )""".split('\n')

        normalized_code = Reader.normalize(code)

        assert (
            ['variable = some_function(another_function(param1,param2),param3)']
            == normalized_code
        )

    def test_normalize_code_with_different_kind_of_brackets(self):
        code = """variable = some_function(another_function(
                        param1,
                        param2,
                        [
                            item1,
                            item2,
                            item3
                        ],
                        {
                            "a": 123
                        }
                    ),
                    param3
                )""".split('\n')

        normalized_code = Reader.normalize(code)

        assert (
            ['variable = some_function(another_function(param1,param2,[item1,item2,item3],{"a": 123}),param3)']
            == normalized_code
        )
