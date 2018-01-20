from dyck import Grammar
from grammar_utils import *


all_states = [W, 'A-', 'A+', 'B-', 'B+', 'C-', 'C+']
meta3 = Grammar([
    # TOP
    (S, [W], [[x, y]]),

    # =============
    # Meta-rules
    # =============

    # Base
    all_o(W, e, [[a, b, c]]),
    all_o('A-', e, [[b, c]]),
    all_o('B-', e, [[a, c]]),
    all_o('C-', e, [[a, b]]),
    all_o('A+', e, [[a]]),
    all_o('B+', e, [[b]]),
    all_o('C+', e, [[c]]),
    [all_o(K, [K, W], [[x, y], [z, w]]) for K in all_states],

    # General 3-ins
    [all_o(K, [K], [[x, y], [a, b, c]]) for K in all_states],

    # =============
    # Meta-rule combinations
    # =============

    # A+
    all_o('C-', ['A+', 'B+'], [[x, y, z, w]]),
    all_o('B-', ['A+', 'C+'], [[x, y, z, w]]),
    all_o(W, ['A+', 'A-'], [[x, y, z, w]]),
    # B+
    all_o('A-', ['B+', 'C+'], [[x, y, z, w]]),
    # C+
    # A-
    # B-
    all_o('C+', ['B-', 'A-'], [[x, y, z, w]]),
    # C-
    all_o(W, ['C-', 'C+'], [[x, y, z, w]]),
    all_o('B+', ['C-', 'A-'], [[x, y, z, w]]),
    all_o('A+', ['C-', 'B-'], [[x, y, z, w]]),
])
