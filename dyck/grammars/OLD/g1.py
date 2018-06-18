from ..dyck import Grammar
from ..grammar_utils import *

g1 = Grammar([
    r('S <- W', [(x, y)]),
    O('W', {(a, b, c)}),
    O('W <- W', {(x, y), (a, b, c)}),
    O('W <- W, W', {(x, y), (z, w)}),
])

