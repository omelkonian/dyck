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

all_states = ['W', 'BC', 'AB'] #, 'ABC']

mcfg2 = Grammar([
    r('S <- W', {(x, y)}),
    O('W', {(a, b, c)}),
    O('W <- W', {(x, y), (a, b, c)}),
    # O('W <- W, W', {(x, y), (l, m)}),
])

# mcfg2 = Grammar([
#     r('S <- W', {(x, y)}),
#     O('A', {(a)}),
#     O('B', {(b)}),
#     O('C', {(c)}),
#     O('W', {(a, b, c)}),
#     O('W <- W, A, B, C', {(x, y), (l, m, q, w, r, t), (a, b, c)}),
# ])

mcfg22 = Grammar([

    ### Base cases
    # r('S <- W', {(x, y)}),

    # # all_c('W', [], orders=[(a, b, c)], left=[a, b, c]),
    # all_c('W', [], orders=[(a, b, c)], right=[a, b, c]),

    # all_c('BC', [], orders=[(a, b, c)], left=[a, b], right=[c]),
    # all_c('AB', [], orders=[(a, b, c)], left=[a], right=[b, c]),
    # # ###

    # # ### SAFETY
    # O('W <- BC', {(x, y)}),
    # O('W <- AB', {(x, y)}),
    # # O('W <- ABC', {(x, y)}),
    # # ###

    # # Interleaving words
    # O('W <- W, W', {(x, y), (z, w)}),

    # # all_c('W', ['AB', 'BC'], orders=[(x, y), (z, w)]
    # all_c('AB', ['AB', 'BC'], orders=[(x, y), (z, w)], left=[x], right=[y]),
    # all_c('BC', ['AB', 'BC'], orders=[(x, y), (z, w)], left=[z], right=[w]),
    # # all_c('ABC', ['AB', 'BC'], orders=[(x, y), (z, w)]
    # #                          , left=[x, z], right=[y, w]),


    # all_c('W', ['AB', 'AB'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                        , left=[y, w]),
    # all_c('W', ['AB', 'AB'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                        , right=[x, z]),
    # all_c('AB', ['AB', 'AB'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[x], right=[z, y, w]),
    # all_c('AB', ['AB', 'AB'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[z], right=[x, y, w]),
    # all_c('AB', ['AB', 'AB'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[x, z], right=[y, w]),
    # all_c('AB', ['AB', 'AB'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[x, z, w], right=[y]),
    # all_c('AB', ['AB', 'AB'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[x, z, y], right=[w]),

    # all_c('W', ['BC', 'BC'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                        , left=[y, w]),
    # all_c('W', ['BC', 'BC'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                        , right=[x, z]),
    # all_c('BC', ['BC', 'BC'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[x], right=[z, y, w]),
    # all_c('BC', ['BC', 'BC'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[z], right=[x, y, w]),
    # all_c('BC', ['BC', 'BC'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[x, z], right=[y, w]),
    # all_c('BC', ['BC', 'BC'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[x, z, w], right=[y]),
    # all_c('BC', ['BC', 'BC'], orders=[(x, y), (z, w), (x, w), (z, y)]
    #                         , left=[x, z, y], right=[w]),


    # # ABC
    # # all_c('ABC', ['BC'], orders=[(x, y), (a, b, c)]
    # #                    , left=[a, x], right=[y, b]),
    # # all_c('ABC', ['AB'], orders=[(x, y), (a, b, c)]
    # #                    , left=[x, b], right=[y, c]),
    # # all_c('ABC', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]
    # #                    , left=[a, x], right=[b, c]),
    # # all_c('ABC', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]
    # #                    , left=[a, b], right=[y, c]),
    # # all_c('ABC', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]
    # #                    , left=[a, b], right=[y, c]),

    # # ABC -> W
    # all_c('W', ['ABC'], orders=[(x, y), (c, b, a), (x, b, y), (x, c), (a, y)]
    #                   , left=[y, a]),
    # all_c('W', ['ABC'], orders=[(x, y), (c, b, a), (x, b, y), (x, c), (a, y)]
    #                   , right=[x, c]),
    # # ABC -> AB
    # all_c('AB', ['ABC'], orders=[(x, y), (c, b, a), (x, b, y), (x, c), (a, y)]
    #                    , left=[c], right=[b]),
    # # ABC -> BC
    # all_c('BC', ['ABC'], orders=[(x, y), (c, b, a), (x, b, y), (x, c), (a, y)]
    #                    , left=[b], right=[a]),
    # # ABC -> ABC
    # all_c('ABC', ['ABC'], orders=[(x, y), (c, b, a), (x, b, y), (x, c), (a, y)]
    #                     , left=[x], right=[c]),
    # all_c('ABC', ['ABC'], orders=[(x, y), (c, b, a), (x, b, y), (x, c), (a, y)]
    #                     , left=[a], right=[y]),

    # ### Insert "abc"

    # # W
    # O('W <- W', {(x, y), (a, b, c)}),

    # # BC -> W
    # all_c('W', ['BC'], orders=[(x, y), (a, b, c)]
    #                  , right=[x, a]),
    # all_c('W', ['BC'], orders=[(x, y), (a, b, c)]
    #                  , left=[y], right=[a]),
    # all_c('W', ['BC'], orders=[(x, y), (a, b, c)]
    #                  , left=[c], right=[x]),
    # all_c('W', ['BC'], orders=[(x, y), (a, b, c)]
    #                  , left=[y, c]),

    # # BC -> BC
    # all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[x], right=[y, a]),
    # all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[a, x], right=[y, b]),
    # all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[a, b], right=[c, x]),
    # all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[x, b], right=[y, c]), # ^2
    # all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[y, b], right=[c]),
    # all_c('BC', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[x, c], right=[y]),

    # # BC -> AB
    # all_c('AB', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[a], right=[x, b]),
    # all_c('AB', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[a, x], right=[y, b]),
    # all_c('AB', ['BC'], orders=[(x, y), (a, b, c)]
    #                   , left=[y, a], right=[b]),


    # O('W <- AB', {(x, y), (a, b, c)}),

    # # AB -> W
    # all_c('W', ['AB'], orders=[(x, y), (a, b, c)]
    #                  , right=[x, a]),
    # all_c('W', ['AB'], orders=[(x, y), (a, b, c)]
    #                  , left=[y, c]),
    # all_c('W', ['AB'], orders=[(x, y), (a, b, c)]
    #                  , left=[y], right=[a]),
    # all_c('W', ['AB'], orders=[(x, y), (a, b, c)]
    #                  , left=[c], right=[x]),

    # # AB -> BC
    # all_c('BC', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[b], right=[x, c]),
    # all_c('BC', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[x, b], right=[y, c]),
    # all_c('BC', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[y, b], right=[c]),

    # # AB -> AB
    # all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[x], right=[y, a]),
    # all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[a], right=[x, b]),
    # all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[x, a], right=[y, b]), # ^2
    # all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[y, a], right=[b]),
    # all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[x, b], right=[y, c]),
    # all_c('AB', ['AB'], orders=[(x, y), (a, b, c)]
    #                   , left=[x, c], right=[y]),

    # ### Insert "acb"

    # # BC -> W
    # all_c('W', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]),
    # # BC -> AB
    # all_c('AB', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]
    #                   , left=[a], right=[b]),
    # # BC -> BC
    # all_c('BC', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]
    #                   , left=[x], right=[c]),
    # all_c('BC', ['BC'], orders=[(x, y), (a, c, b), (x, c), (b, y)]
    #                   , left=[b], right=[y]),

    # ### Insert "bac"

    # # AB -> W
    # all_c('W', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]),
    # # AB -> AB
    # all_c('AB', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]
    #                   , left=[x], right=[b]),
    # all_c('AB', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]
    #                   , left=[a], right=[y]),
    # # AB -> BC
    # all_c('BC', ['AB'], orders=[(x, y), (b, a, c), (a, y), (x, b)]
    #                   , left=[b], right=[c]),

    # ### Insert "bca"

    # # BC -> W
    # all_c('W', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]),
    # # BC -> AB
    # all_c('AB', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]
    #                   , left=[x], right=[b]),
    # all_c('AB', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]
    #                   , left=[a], right=[y]),
    # # BC -> BC
    # all_c('BC', ['AB'], orders=[(x, y), (b, c, a), (a, y), (x, b)]
    #                   , left=[b], right=[c]),

    # # # Debugging
    # ('$_W', ['W'], [[x, '$', y]]),
])
