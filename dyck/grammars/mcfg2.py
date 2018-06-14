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

    # NOTE: Insert "cba" (MIX invariant)

    ### Base cases
    forall(all_states,
           lambda K: r('S <- K', [(x, y)])),

    all_c('W', [], orders=[(a, b, c)], left=[a, b, c]),
    all_c('W', [], orders=[(a, b, c)], right=[a, b, c]),

    all_c('BC', [], orders=[(a, b, c)], left=[a, b], right=[c]),
    all_c('AB', [], orders=[(a, b, c)], left=[a], right=[b, c]),
    ###

    ### SAFETY
    O('W <- BC', {(x, y)}),
    O('W <- AB', {(x, y)}),
    ###

    # Interleaving words
    O('W <- W, W', {(x, y), (z, w)}),


    # TODO: Sanity check
    ### Insert "abc"

    # W
    O('W <- W', {(x, y), (a, b, c)}),

    # BC -> W
    all_c('W', ['BC'], orders=[(x, y), (a, b, c)]
                     , right=[x, a]),
    all_c('W', ['BC'], orders=[(x, y), (a, b, c)]
                     , left=[y], right=[a]),
    all_c('W', ['BC'], orders=[(x, y), (a, b, c)]
                     , left=[c], right=[x]),
    all_c('W', ['BC'], orders=[(x, y), (a, b, c)]
                     , left=[y, c]),

    # BC -> BC
    all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[x], right=[y, a]),
    all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[a, x], right=[y, b]),
    all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[a, b], right=[c, x]),
    all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[x, b], right=[y, c]),
    all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[y, b], right=[c]),
    all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[x, c], right=[y]),

    # BC -> AB
    all_c('AB', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[a], right=[x, b]),
    all_c('AB', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[a, x], right=[y, b]),
    all_c('AB', ['BC'], orders=[(x, y), (a, b, c)]
                      , left=[y, a], right=[b]),
    O('W <- AB', {(x, y), (a, b, c)}),

    # AB -> W
    all_c('W', ['AB'], orders=[(x, y), (a, b, c)]
                     , right=[x, a]),
    all_c('W', ['AB'], orders=[(x, y), (a, b, c)]
                     , left=[y, c]),
    all_c('W', ['AB'], orders=[(x, y), (a, b, c)]
                     , left=[y], right=[a]),
    all_c('W', ['AB'], orders=[(x, y), (a, b, c)]
                     , left=[c], right=[x]),

    # AB -> BC
    all_c('BC', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[b], right=[x, c]),
    all_c('BC', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[x, b], right=[y, c]),
    all_c('BC', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[y, b], right=[c]),

    # AB -> AB
    all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[x], right=[y, a]),
    all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[a], right=[x, b]),
    all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[x, a], right=[y, b]),
    all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[y, a], right=[b]),
    all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[x, b], right=[y, c]),
    all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
                      , left=[x, c], right=[y]),

    ### Insert "acb"

    # BC -> W
    all_c('W', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]),
    # BC -> AB
    all_c('AB', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]
                      , left=[a], right=[b]),
    # BC -> BC
    all_c('BC', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]
                      , left=[x], right=[c]),
    all_c('BC', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]
                      , left=[b], right=[y]),

    ### Insert "bac"

    # AB -> W
    all_c('W', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]),
    # AB -> AB
    all_c('AB', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]
                      , left=[x], right=[b]),
    all_c('AB', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]
                      , left=[a], right=[y]),
    # AB -> BC
    all_c('BC', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]
                      , left=[b], right=[c]),

    ### Insert "bca"

    # BC -> W
    all_c('W', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]),
    # BC -> AB
    all_c('AB', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]
                      , left=[x], right=[b]),
    all_c('AB', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]
                      , left=[a], right=[y]),
    # BC -> BC
    all_c('BC', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]
                      , left=[b], right=[c]),

    # Debugging
    ('$_W', ['W'], [[x, '$', y]]),
])
