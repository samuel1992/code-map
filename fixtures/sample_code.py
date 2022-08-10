code = """
import os
import sys

from collections import namedtuple

from .config import MyConfiguration


class FirstClass:
    def __init__(self, query, file):
        self._query = query
        self._file = file

    # Some comment here
    # some more comment ---> here
    @property
    def content(self):
        FourthClass() + FifthClass()
        return self._file.template.render(query=self._query)

    def method_with_conditions(self):
        if self._query:
            return 'query'
        else:
            return 'no query'

    def save(self):
        with open(self._file.path, 'w') as file:
            file.write(self.content)


variable_a = 'something'


class SecondClass:
    @staticmethod
    def generate(type, query):
        assert type in MY_TYPES

        file = MY_TYPES[type]

        return FirstClass(
            query=query, file=file
        )

    def _private_method(self):
        something = ThirdClass() + FirstClass()
        a = shomething(1)
        b = 2
        a + b
        a += b
        return a


class ThirdClass:
    def somethign(self):
        return 'bla'

    def another_method(self, param):
        if param:
            return 'bla'

        return 'another bla'

class FourthClass:
    pass

class FifthClass:
    pass


def some_function():
    a = FirstClass()
    b = SecondClass()

    return a + b

"""
