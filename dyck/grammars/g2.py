from ..dyck import Grammar
from ..grammar_utils import *

states = ['W', 'A-', 'A+', 'B-', 'B+', 'C-', 'C+']
g2 = Grammar([
    # TOP
    r('S <- W', {(x, y)}),

    # =============
    # Base cases
    # =============
    O('A-', {(b, c)}),
    O('B-', {(a, c)}),
    O('C-', {(a, b)}),
    O('A+', {(a)}),
    O('B+', {(b)}),
    O('C+', {(c)}),

    # =============
    # Combinations
    # =============
    forall(states,
	lambda K: O('K <- K, W', {(x, y), (l, m)})),
    O('C- <- A+, B+', {(x, y, l, m)}),
    O('B- <- A+, C+', {(x, y, l, m)}),
    O('W <- A+, A-', {(x, y, l, m)}),
    O('A- <- B+, C+', {(x, y, l, m)}),
    O('C+ <- B-, A-', {(x, y, l, m)}),
    O('W <- C-, C+', {(x, y, l, m)}),
    O('B+ <- C-, A-', {(x, y, l, m)}),
    O('A+ <- C-, B-', {(x, y, l, m)}),
])
