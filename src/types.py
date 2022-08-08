from types import SimpleNamespace

from collections import namedtuple


_Type = namedtuple('Type', ['name', 'regex'])

Types = SimpleNamespace(**{
    'klass': _Type('CLASS', r'^class\ .*'),
    'method': _Type('METHOD', r'^def\ .*\([self|cls].*'),
    'function': _Type('FUNCTION', r'^def\ .*\(?\)'),
    'comment': _Type('COMMENT', r'^("""\ .*|#|\'\'\')'),
    'variable': _Type('VARIABLE', r'.*\=.*'),
    'loop': _Type('LOOP', r'.*(while|for).*'),
    'conditional': _Type('CONDITIONAL', r'.*(if|else|elif).*'),
    'operation': _Type('OPERATION', ''),
})
