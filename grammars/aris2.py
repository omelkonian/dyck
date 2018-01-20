from functools import partial
from dyck import Grammar
from grammar_utils import *

states = {
    # 0 Symbol
    ('', ''): 'W',
    # 1 Symbol
    ("a", ''): 'lA+',
    ('', "a"): 'rA+',
    # ------------------
    ("b", ''): 'lB+',
    ('', "b"): 'rB+',
    # ------------------
    ("c", ''): 'lC+',
    ('', "c"): 'rC+',
    # 2 Symbols
    ("bc", ""): 'lA-',
    ("", "bc"): 'rA-',
    ("b", "c"): 'lrA-',
    # ------------------
    ("ac", ""): 'lB-',
    ("", "ac"): 'rB-',
    ("a", "c"): 'lrB-',
    # ------------------
    ("ab", ""): 'lC-',
    ("", "ab"): 'rC-',
    ("a", "b"): 'lrC-',
}
all_states = states.values()
_states = {states[k]: k for k in states}

# Setup
double_ins = partial(double_ins, states=states)
triple_ins = partial(triple_ins, states=states)
prog = partial(prog, states=states)
prog3 = partial(prog3, states=states)
prog4 = partial(prog4, states=states)
all_state_tuples = partial(all_state_tuples, states=states)
all_state_tuples3 = partial(all_state_tuples3, states=states)
all_state_tuples4 = partial(all_state_tuples4, states=states)

x, y, z, w, k, l, m, n = (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)
aris2 = Grammar([
    # TOP
    ('S', ['W'], [[x, y]]),

    # base
    [(v, [], [list(kk[0]), list(kk[1])]) for kk, v in states.items() if v != 'W'],

    # 2-tuples
    [list(prog(L, R)) for L, R in all_state_tuples()],

    # 3-ins
    [list(triple_ins(v[0], v[1])) for v in states],
])

