from itertools import permutations, combinations
import numpy as np


#
# Universal constants
#
tuple_to_char = {
    # 1-MCFG
    (0, 0): 'x',
    (1, 0): 'z',
    (2, 0): 'k',
    (3, 0): 'm',
    # 2-MCFG
    (0, 1): 'y',
    (1, 1): 'w',
    (2, 1): 'l',
    (3, 1): 'n',
    # 3-MCFG
    (0, 2): 'o',
    (1, 2): 'p',
    (2, 2): 'q',
    (3, 2): 'r',
    # 4-MCFG
    (0, 3): 's',
    (1, 3): 't',
    (2, 3): 'u',
    (3, 3): 'v',
}
for key, value in tuple_to_char.items():
    globals().update({value: key})

a, b, c, S, W = 'abcSW'
e = []
A, A_, B, B_, C, C_ = 'A', 'A-', 'B', 'B-', 'C', 'C-'
AB, AC, BA, CA, BC, CB, AA, BB, CC = 'AB', 'AC', 'BA', 'CA', 'BC', 'CB', 'AA', 'BB', 'CC'
A_B_, A_C_, B_A_, C_A_, B_C_, C_B_, A_A_, B_B_, C_C_ = 'A-B-', 'A-C-', 'B-A-', 'C-A-', 'B-C-', 'C-B-', 'A-A-', 'B-B-', 'C-C-'
AC_, C_A, A_A, AA_, CC_, CA_, A_C, BA_, C_B, B_C, AB_, BB_, BC_ = 'AC-', 'C-A', 'A-A', 'AA-', 'CC-', 'CA-', 'A-C', 'BA-', 'C-B', 'B-C', 'AB-', 'BB_', 'BC_'
all_singles = [A, A_, B, B_, C, C_]
all_doubles = [AA, AA_, AB, AB_, AC, AC_, BA_, BB, BB_, BC, BC_, CC, CC_, A_A_, A_B_, A_C_, B_B_, B_C_, C_C_]


########################################################################################################################
# Meta-grammar utilities
########################################################################################################################
def flatten(l):
    return sum(l, [])


def rule(lhs, rhs):
    assert len(rhs) == 1
    return lhs, rhs, [[x], [y]]


def symbols_from_orders(orders):
    return ''.join(list(set(''.join(orders))))


def is_ordered(symbols, orders):
    return all([is_ordered_single(symbols, order) for order in orders])


def is_ordered_single(symbols, order):
    for i, o in enumerate(order):
        for j, symbol in enumerate(symbols):
            if symbol == o:
                return is_ordered_single(symbols[j+1:], order[i+1:])
            if symbol != o and symbol in order:
                return False
    return True


def ordered_permutations(orders, **symmetries):
    return remove_symmetries([
            ''.join(s)
            for s in permutations(symbols_from_orders(orders))
            if is_ordered(s, orders)], **symmetries)


def ordered_pairs(orders, splits=1, **symmetries):
    return [tuple([np_arr.tolist() for np_arr in np.split(list(perm), indices)])
            for indices in combinations(range(len(symbols_from_orders(orders)) + 1), splits)
            for perm in ordered_permutations(orders, **symmetries)]


def post_process(orders, splits=1, **symmetries):
    return [map(post_process_single, tuple) for tuple in ordered_pairs(orders, splits=splits, **symmetries)]


def post_process_single(order):
    return [globals()[ch] for ch in order]


def pre_process(symbols):
    return [pre_process_single(s) for s in symbols]


def pre_process_single(symbols):
    return ''.join([tuple_to_char.get(s, 'e' if s == [] else s) for s in symbols])


def all_ordered(orders, splits=1, **symmetries):
    return post_process(pre_process(orders), splits=splits, **symmetries)


def all_o(lhs, rhs, orders, splits=1, **symmetries):
    return [(lhs, rhs, order) for order in all_ordered(orders, splits=splits, **symmetries)]


def all_c(lhs, rhs, left=[], right=[], orders=[], **symmetries):
    return [(lhs, rhs, order) for order in all_ordered(orders, **symmetries)
            if all(map(lambda l: l in order[0], left))
            if all(map(lambda r: r in order[1], right))]


def all_nc(lhs, rhs, left=[], right=[], orders=[], **symmetries):
    allOrd = all_ordered(orders, **symmetries)
    allCon = [o for o in allOrd
              if all(map(lambda l: l in o[0], left))
              if all(map(lambda r: r in o[1], right))]
    return [(lhs, rhs, o) for o in allOrd if o not in allCon]


def remove_symmetries(words, **symmetries):
    ret = []
    for w in words:
        if [translate(w, **symmetries)] not in ret:
            ret += [[w]]
    return flatten(ret)


def translate(word, **symmetries):
    symmetries = {k: (tuple_to_char[v] if isinstance(v, tuple) else v) for k, v in symmetries.items()}
    symmetries = dict(symmetries, **{v: k for k, v in symmetries.items()})  # add inverse translations
    return ''.join([symmetries.get(c, c) for c in word])


########################################################################################################################
# ARIS: Automatic Rule Inference System
########################################################################################################################
def all_state_tuples(states):
    cur = []
    for L in states:
        for R in states:
            if (R, L) not in cur:
                cur.append((L, R))
                yield (L, R)


def all_state_tuples3(states):
    cur = []
    for A in states:
        for B in states:
            for C in states:
                if all([(X, Y, Z) not in cur for X, Y, Z in [
                    (A, C, B),
                    (B, A, C), (B, C, A),
                    (C, A, B), (C, B, A)
                ]]):
                    yield (A, B, C)


def all_state_tuples4(states):
    cur = []
    for A in states:
        for B in states:
            for C in states:
                for D in states:
                    if all([(X, Y, Z, W) not in cur for X, Y, Z, W in [
                        (A, B, D, C), (A, D, B, C), (A, D, C, B), (A, C, B, D), (A, C, D, B),
                        (B, A, C, D), (B, A, D, C), (B, C, A, D), (B, C, D, A), (B, D, A, C), (B, D, C, A),
                        (C, A, B, D), (C, A, D, B), (C, B, A, D), (C, B, D, A), (C, D, A, B), (C, D, B, A),
                        (D, A, B, C), (D, A, C, B), (D, B, A, C), (D, B, C, A), (D, C, A, B), (D, C, B, A),
                    ]]):
                        yield (A, B, C, D)


# def all_state_pairs3():
#     cur = []
#     for L in states:
#         for R in states:
#             for C in states:
#                 # Exclude X-
#                 if any(map(lambda t: '-' in states[t], [L, R, C])):
#                     continue
#                 if all(map(lambda t: t not in cur, [(L, R, C), (R, L, C), (R, C, L), (C, L, R), (C, R, L)])):
#                     cur.append((L, C, R))
#                     yield (L, C, R)


def eliminate((l, r)):
    lr = l + '%' + r
    a_choices = [i for i, ch in enumerate(lr) if ch == 'a']
    b_choices = [i for i, ch in enumerate(lr) if ch == 'b']
    c_choices = [i for i, ch in enumerate(lr) if ch == 'c']

    choices = [(a_i, b_i, c_i) for a_i in a_choices for b_i in b_choices for c_i in c_choices]
    valid_choices = filter(lambda (k, l, m): k < l < m, choices)
    if not valid_choices:
        yield tuple(lr.split('%'))
    for (a_i, b_i, c_i) in valid_choices:
        temp = list(lr)
        temp[a_i] = '$'
        temp[b_i] = '$'
        temp[c_i] = '$'
        lr2 = "".join(temp)
        eliminated = "".join([ch for ch in lr2 if ch != '$'])
        rule = tuple(eliminated.split('%'))
        yield rule # W <- ....
        if rule == (e, e):
            yield (l, r)


def double_ins(_x, _y, states):
    d = {x: _x, y: _y}
    rhs = states[(_x, _y)]
    perms = flatten([
        all_ordered([[x, y], [k], [l]])
        for k in [a, b, c]
        for l in [a, b, c]])

    def transform(l):
        return ''.join(map(lambda elem: d[elem] if isinstance(elem, tuple) else elem, l))

    perms2 = map(lambda (l1, l2): (transform(l1), transform(l2)), perms)
    for perm, _perm in zip(perms2, perms):
        eliminated = list(eliminate(perm))[0]
        try:
            state = states[eliminated]
            rule = (state, [rhs], [_perm[0], _perm[1]])
            yield rule
        except KeyError:
            continue


def triple_ins(_x, _y, states):
    d = {x: _x, y: _y}
    rhs = states[(_x, _y)]
    perms = all_ordered([[x, y], [a], [b], [c]])

    def transform(l):
        return ''.join(map(lambda elem: d[elem] if isinstance(elem, tuple) else elem, l))

    perms2 = map(lambda (l1, l2): (transform(l1), transform(l2)), perms)
    for perm, _perm in zip(perms2, perms):
        for eliminated in eliminate(perm):
            try:
                state = states[eliminated]
                rule = (state, [rhs], [_perm[0], _perm[1]])
                yield rule
            except KeyError:
                continue


# TODO progN
def prog((_x, _y), (_z, _w), states):
    L = states[(_x, _y)]
    R = states[(_z, _w)]
    d = {x: _x, y: _y, z: _z, w: _w}
    for element1, element2 in all_ordered([[x, y], [z, w]]):
        desc1, desc2 = "", ""
        for elem in element1:
            desc1 += d[elem]
        for elem in element2:
            desc2 += d[elem]
        descriptor = (desc1, desc2)
        for eliminated in eliminate(descriptor):
            try:
                eliminated_state = states[eliminated]
            except KeyError:
                continue
            yield (eliminated_state, [L, R], [element1, element2])


def prog3((_x, _y), (_z, _w), (_k, _l), states):
    A = states[(_x, _y)]
    B = states[(_z, _w)]
    C = states[(_k, _l)]
    d = {x:_x, y:_y, z:_z, w:_w, k: _k, l: _l}
    for element1, element2 in all_ordered([[x, y], [z, w], [k, l]]):
        desc1, desc2 = "", ""
        for elem in element1:
            desc1 += d[elem]
        for elem in element2:
            desc2 += d[elem]
        descriptor = (desc1, desc2)
        eliminated_list = eliminate(descriptor)
        for eliminated in eliminated_list:
            try:
                eliminated_state = states[eliminated]
            except KeyError:
                continue
            yield (eliminated_state, [A, B, C], [element1, element2])
