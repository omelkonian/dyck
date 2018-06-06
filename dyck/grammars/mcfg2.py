from ..dyck import Grammar
from ..grammar_utils import *

"""
ababaacbcbcc

W
 - [W] null
 - [BC] b -> c
 - [AB] a -> b


BC(|ab|,|c|)

BC(ab |ab|, |c| c)

AB(abab |a|, |cb| cc)

W(ababa |acb|, cbcc)



# extra

W(abc, abc)

#

BC(|ab|, |c|)

AB(ab|a|, |cb|c)

BC(|ab|aba, cbc|c|)

AB(ababa|a|, |cb|cbcc)

"""

all_states = ['W', 'BC', 'AB']

mcfg2 = Grammar([

    ### Base cases
    forall(all_states,
           lambda K: r('S <- K', [(x, y)])),

    all_c('W', [], orders=[(a, b, c)], left=[a, b, c]),
    all_c('W', [], orders=[(a, b, c)], right=[a, b, c]),

    all_c('BC', [], orders=[(a, b, c)], left=[a, b], right=[c]),
    all_c('AB', [], orders=[(a, b, c)], left=[a], right=[b, c]),
    ###

    # Insert "abc"
    O('W <- W', {(x, y), (a, b, c)}),
    all_c('BC', ['BC'], orders=[(x, y), (a, b, c)], left=[a,b], right=[c]),
    all_c('BC', ['BC'], orders=[(x, y), (a, b, c)], left=[x], right=[y]),

    all_c('AB', ['AB'], orders=[(x, y), (a, b, c)], left=[a], right=[b, c]),
    all_c('AB', ['AB'], orders=[(x, y), (a, b, c)], left=[x], right=[y]),

    forall(all_states,
           lambda K: all_c('BC', [K], orders=[(x, y), (a, b, c)],
                                      left=[a, b], right=[c])),

    forall(all_states,
           lambda K: all_c('AB', [K], orders=[(x, y), (a, b, c)],
                                      left=[a], right=[b, c])),

    ### Insert "acb"

    # BC -> W
    all_c('W', ['BC'], orders=[(x, y), (a, c, b), (x, c), (a, b, y)],
                     left=[y, c]),
    all_c('W', ['BC'], orders=[(x, y), (a, c, b), (x, c), (a, b, y)],
                     right=[x, a]),

    # BC -> AB
    all_c('AB', ['BC'], orders=[(x, y), (a, c, b), (x, c), (a, b, y)],
                        left=[a], right=[b]),

    # BC -> BC
    all_c('BC', ['BC'], orders=[(x, y), (a, c, b), (x, c), (a, b, y)],
                        left=[b], right=[y]),

    ### Insert "bac"

    # AB -> W
    all_c('W', ['AB'], orders=[(x, y), (b, a, c), (x, b), (a, y)],
                     left=[y, c]),
    all_c('W', ['AB'], orders=[(x, y), (b, a, c), (x, b), (a, y)],
                     right=[x]),

    # AB -> BC
    all_c('BC', ['AB'], orders=[(x, y), (b, a, c), (x, b), (a, y)],
                        left=[b], right=[c]),

    # AB -> AB
    all_c('AB', ['AB'], orders=[(x, y), (b, a, c), (x, b), (a, y)],
                      left=[x], right=[b]),

    ### Insert "bca"

    # AB -> W

    all_c('W', ['AB'], orders=[(x, y), (b, c, a), (x, b), (a, y)],
                     left=[b, c], right=[a]),
    all_c('W', ['AB'], orders=[(x, y), (b, c, a), (x, b), (a, y)],
                     left=[y]),
    all_c('W', ['AB'], orders=[(x, y), (b, c, a), (x, b), (a, y)],
                     right=[x]),

    # AB -> BC
    all_c('BC', ['AB'], orders=[(x, y), (b, c, a), (x, b), (a, y)],
                      left=[b], right=[c]),

    # AB -> AB
    all_c('AB', ['AB'], orders=[(x, y), (b, c, a), (x, b), (a, y)],
                      left=[x], right=[b]),
    all_c('AB', ['AB'], orders=[(x, y), (b, c, a), (x, b), (a, y)],
                      left=[a], right=[y]),


    # # Debugging
    ('$_W', ['W'], [[x, '$', y]]),
])
