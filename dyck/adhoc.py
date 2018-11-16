from functools import reduce
from itertools import permutations
import numpy as np

def collapsible(dw):
    matches = cmp(dw)

    # Numerify matches (e.g. [[4], [11], [12]] => m0==11)
    d_init = { i : k for i, k in enumerate(matches) }
    # print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    d_abc = { tupl(k) : i for i, k in d_init.items() }

    ret = False
    order = pick_grandiose(list(permutations(sanitize_matches(matches))))
    # order = list(permutations(sanitize_matches(matches)))
    for o in order:
        # print('{}'.format(map(lambda x: d_abc[tupl(x)], o)))
        if analyze(dw, o, d_abc):
            ret = True
            # return True

    if ret == False:
        raise RuntimeError('Cannot parse with (x)')

def sanitize_matches(ms):
    return map(lambda m: map(lambda x: range(x, x+1), m), ms)

def analyze(dw, order, d):
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
    # trees = []
    for tree, res in nd_fold(lambda x, y: collapse_matches(x, y, dimension), order):
        if res is None:
            continue
        if concat(res) == range(n):
            # trees.append(tree) # slow
            print(pp_tree0(tree))
            return True # fast

    return False
    # return map(pp_tree0, trees)

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

def pick_grandiose(ms):

    # Calculate scores
    scores = np.zeros([len(ms[0]), len(ms[0])])
    for (i, m1), (j, m2) in pairs(list(enumerate(ms[0]))):
        w = count_touch(m1, m2)
        scores[i, j] = float(w)
        scores[j, i] = float(w)

    # Normalize columns
    scores /= scores.sum(axis=0)

    mx, best = (0, [])
    for m in ms:
        def index(xx):
            return [ i for i, ms0 in enumerate(ms[0])
                       if xx == ms0][0]

        sc = sum(map(
            lambda xy:
                max( scores[index(xy[0]), index(xy[1])]
                   , scores[index(xy[1]), index(xy[0])])
            , pairs(m)))

        # Pick most 'fitting'
        if sc == mx:
            best.append(m)
        elif sc > mx:
            best = [m]
            mx = sc

    assert best != []
    from pprint import pprint
    pprint(best)
    return best
    # return pick_grandiose0(ms)


def pick_grandiose0(ms):
    res = zip(ms, map(score, ms))
    mx = max(res, key = lambda x: x[1])

    mxs = [r[0] for r in res if r[1] == mx[1]]
    # if len(mxs) > 1:
    #     print('MULTIPLE!!!', mxs)

    return mxs


    [mx, best] = 0, None
    for m in ms:
        s = score(m)
        if s > mx:
            mx = s
            best = m
    return best

def score(m):
    return sum(map(lambda xy: count_touch(xy[0], xy[1]), pairs(m)))

def count_touch(surface_match1, surface_match2):
    ([x], [y], [z]) = surface_match1
    ([k], [l], [m]) = surface_match2
    return sum([ (1 if abs(xx-kk) == 1 else 0)
                 for xx in [x, y, z]
                 for kk in [k, l, m] ])
