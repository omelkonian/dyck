from functools import reduce
from itertools import permutations
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

"""
(1) exists t. t `collapse` D2a /\\ t `collapse` D2c => ~(t `collapse` D3)
   witness: abacbacbc
(2) exists t. t `collapse` D3 => ~(t `collapse` D2a /\\ t `collapse` D2c)
   witness: abababccc
(3) forall w.
      exists t.
        t `collapse` D2a /\\ t `collapse` D2c => t `collapse` D3

   witness: verifiable up to n=4

(3) => (4) exists f.  f({t | t `collapse` D2a /\\ t `collapse` D2c})
                        `collapse` D3
"""

def test(m1, m2):
    (a1, b1, c1) = m1
    (a2, b2, c2) = m2
    c = collapse_matches(([a1], [b1], [c1]), ([a2], [b2], [c2]), 3)
    # print('\t{}'.format(c))
    if c:
        # print(m1, m2)
        (x, y, z) = c
        if any(map(lambda x: not x, c)):
            return True
        return (a1 in x or a2 in x) and (b1 in y or b2 in y) and (c1 in z or c2 in z)
    else:
        return False




def collapsible(dw):
    matches = cmp(dw)
    for m1, m2 in [(m1, m2) for m1 in matches for m2 in matches]:
        # print(m1, m2)
        if test(m1, m2):
            return

    raise RuntimeError('Cannot parse with (x)')



    dw_ab = dw.replace('c', '')
    dw_bc = dw.replace('a', '')

    ms = [matches, matches_ab, matches_bc] = map(cmp, [dw, dw_ab, dw_bc])

    # Numerify matches (e.g. [[4], [11], [12]] => m0==11)
    d_init = { i + 1 : k for i, k in enumerate(matches) }
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    d_abc = { tupl(k) : i for i, k in d_init.items() }
    d_ab = { tupl([x - len([y for y in dw[:x] if y == 'c']) for x in k[:2]]) : i
             for k, i in d_abc.items() }
    d_bc = { tupl([x - len([y for y in dw[:x] if y == 'a']) for x in k[1:]]) : i
             for k, i in d_abc.items() }
    print('Match ABC: {}'.format(d_abc))
    print('Match AB: {}'.format(d_ab))
    print('Match BC: {}'.format(d_bc))

    perms = [ list(permutations(sanitize_matches(x)))
              for x in ms ]
    ret = False
    trees = []
    trees_ab = []
    trees_bc = []
    for o, order in enumerate(perms[0]):
        print('^^^^^^^^^^^^^^^^^^ {} ^^^^^^^^^^^^^^^^^^^'.format(map(lambda x: d_abc[tupl(x)], order)))
        # Analyze dw, dw_ab, dw_bc
        trees0 = analyze(dw, o, order, d_abc)
        if trees0:
            ret = True
        trees.extend(trees0)
        trees_ab.extend(analyze(dw_ab, o, perms[1][o], d_ab))
        trees_bc.extend(analyze(dw_bc, o, perms[2][o], d_bc))

    # Checking equivalence
    inter = set(trees_ab).intersection(set(trees_bc))


    # rem = set(trees).difference(inter)
    # if not rem:

    # if inter.issubset(set(trees)):

    if inter.intersection(set(trees)):
        pass
        # print('YIHHAAAAAAA')
    else:
        print('NIHHHAAAAAA: {}'.format(dw))
        print('Inter: {}'.format(inter))
        print('Trees: {}'.format(trees))
        # print(rem)
        # print(inter.difference(set(trees)))

        exit(0)

    if not ret:
        raise RuntimeError('Cannot parse with (x)')

# def sort_permutations(ps):
#     return sorted(ps, key=lambda x: #int# )

def sanitize_matches(ms):
    return map(lambda m: map(lambda x: range(x, x+1), m), ms)

def analyze(dw, o, order, d):
    def pp_order(order):
        return map(pp_match, order)
    def pp_match(ms):
        return d[tupl(ms)]
    def pp_tree0(t):
        if isinstance(t, tuple) and len(t) == 2: # Node
            (l, r) = t
            [pt1, pt2] = sorted([pp_tree0(l), pp_tree0(r)])
            return '({} <> {})'.format(pt1, pt2)
        else: # Leaf
            return pp_match(t)
    def pp_tree(t, gr, acc):
        if isinstance(t, tuple) and len(t) == 2: # Node
            (l, r) = t
            (ln, rn) = (acc + "L", acc + "R")
            pp_tree(l, gr, ln)
            pp_tree(r, gr, rn)
            gr.add_node(acc, label="*")
            gr.add_edge(acc, ln)
            gr.add_edge(acc, rn)
        else: # Leaf
            gr.add_node(acc, label=pp_match(t))

    dimension = len(set(dw))
    n = len(dw)
    trees = []
    for tree, res in nd_fold(lambda x, y: collapse_matches(x, y, dimension), order):
        if res is None:
            continue
        if concat(res) == range(n):
            trees.append(tree) # slow
            # return True # fast

    # Render in DOT
    # g = nx.DiGraph()
    # for i, t in enumerate(trees):
    #     print('\t{}'.format(pp_tree0(t)))
    #     pp_tree(t, g, str(i + 1))
    # write_dot(g, '{}{}.dot'.format(dw, str(o)))

    return map(pp_tree0, trees)

def tupl(xs):
    if isinstance(xs, list) and len(xs) == 1:
        return xs[0]
    if isinstance(xs, tuple) or isinstance(xs, list):
        return tuple(map(tupl, xs))
    else:
        return xs

def cmp(dw):
    dimension = len(set(dw))
    alphabet = 'abcdefghijklmnopqrstuvwxyz'[(0 if 'a' in set(dw) else 1):]
    symbols = alphabet[:dimension]
    stacks = [[] for _ in range(dimension)]
    for i, c in enumerate(dw):
        j = symbols.index(c)
        if j == 0:
            stacks[j].append([i])
        else:
            cc = stacks[j-1].pop()
            stacks[j].append(cc + [i])
    return stacks[-1]


def collapse_matches(match1, match2, dimension):
    if (match1 is None) or (match2 is None):
        return None
    try:
        s = sorted(concat(match1) + concat(match2))
        b = [[] for _ in range(dimension)]
        cur = 0
        last = s[0] - 1
        for x in s:
            if x - last != 1:
                cur += 1
            b[cur].append(x)
            last = x
        # print('{} ~ {} = {}'.format(match1, match2, b))
        return b
    except IndexError:
        # print('{} ~ {} = X'.format(match1, match2, b))
        return None

def concat(xss):
    return reduce(lambda x, y: x + y, xss)

def all_trees0(xs):
    return all_trees(len(xs), xs)

def all_trees(n, xs):
    if n == 2: #nodes = 1
        return [tuple(xs)]
    else: #nodes >= 2
        return concat([ insert_at_end(t, xs[-1])
                        for t in all_trees(n - 1, xs[:-1])])

def insert_at_end(t, x):
    if isinstance(t, tuple): # Node
        (l, r) = t
        # A. create new root
        ta = (t, x)
        # B. go down in the right tree
        tb = insert_at_end(r, x)

        return [ta] + map(lambda y: (l, y), tb)
    else: # Leaf
        return [(t, x)]

def nd_fold(f, xs):
    # all bracketings
    ts = all_trees0(xs)
    # fold f (in all inner bracketing)
    return map(lambda t: (t, fold(f, t)), ts)

# Fold over a Tree = tuple of tuples
def fold(f, t):
    if isinstance(t, tuple): # Node
        (l, r) = t
        return f(fold(f, l), fold(f, r))
    else: # Leaf
        return t


def pairs(xs):
    return zip(xs, xs[1:])


# for order in pick_grandiose(matches):
        # if invalid(order):
        #     continue
        # if incompatible(order):
            # print('INCOMPAT')
            # continue

# def pick_grandiose(matches):
#     xs = sorted(permutations(matches), key = continuous, reverse = True)
#     ma = continuous(xs[0])
#     return [ x for x in xs if continuous(x) == ma]

# def continuous(match):
#     xs = map(lambda x: collapse_matches(x[0], x[1]) is None, pairs(match))
#     try:
#         i = xs.index(None)
#         return len(xs[:i])
#     except  :
#         return len(xs)

# def incompatible(order):
#     # bs = map(lambda x: collapse_matches(x[0], x[1]) is None, pairs(order))
#     # return any(bs)
#     return collapse_matches(order[0], order[1]) is None


# def invalid(order):
#     return False
    # aa = map(lambda x: x[0], order)
    # cc = map(lambda x: -x[2], order)
    # return (sorted(aa) != aa) and (sorted(cc) != cc)
