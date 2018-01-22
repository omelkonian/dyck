from ..dyck import Grammar
from ..grammar_utils import *

triple_insertion = Grammar([
    r('S <- W', [(x, y)]),
    O('W', {(a, b, c)}),
    O('W <- W', {(x, y), (a, b, c)}),
])

