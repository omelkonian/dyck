from ..dyck import Grammar
from ..grammar_utils import *

mcfg3 = Grammar([
    r('S <- W', {(x, y, z)}),
    O('W', {(a, b, c)}, splits=2),
    O('W <- W', {(x, y, z), (a, b, c)}),
    O('W <- W, W', {(x, y, z), (l, m, n)}),
])
