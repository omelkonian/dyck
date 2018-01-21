from ..dyck import Grammar
from ..grammar_utils import *

triple_insertion = Grammar([
    (S, [W], [[x, y]]),
    all_o(W, e, [[a, b, c]]),
    all_o(W, [W], [[x, y], [a, b, c]]),
])

