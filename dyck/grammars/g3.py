from ..dyck import Grammar
from ..grammar_utils import *

all_states = ['W', 'A-', 'A+', 'B-', 'B+', 'C-', 'C+']
g3 = Grammar([
    # TOP
    ('S', ['W'], [(x, y)]),
    # Base
    O('W', {(a, b, c)}),
    O('A-', {(b, c)}),
    O('B-', {(a, c)}),
    O('C-', {(a, b)}),
    O('A+', {(a,)}),
    O('B+', {(b,)}),
    O('C+', {(c,)}),
    # Combination
    forall(all_states,
	lambda K: O('K <- K, W', {(x, y), (z, w)})),
    O('C- <- A+, B+', {(x, y, z, w)}),
    O('B- <- A+, C+', {(x, y, z, w)}),
    O('W <- A+, A-', {(x, y, z, w)}),
    O('A- <- B+, C+', {(x, y, z, w)}),
    O('C+ <- B-, A-', {(x, y, z, w)}),
    O('W <- C-, C+', {(x, y, z, w)}),
    O('B+ <- C-, A-', {(x, y, z, w)}),
    O('A+ <- C-, B-', {(x, y, z, w)}),
    # 3-ins
    forall(all_states,
	lambda K: O('K <- K', {(x, y), (a, b, c)})),
])
