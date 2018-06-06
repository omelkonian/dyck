from ..dyck import Grammar
from ..grammar_utils import *

mcfg3 = Grammar([
    r('S <- W', [(x, y, o)]),
    O('W', {(a, b, c)}, splits=2),
    O('W <- W', {(x, y, o), (a, b, c)}, splits=2),

    # Debugging
    ('$_W', ['W'], [[x, '$', y, '$', o]]),
])
