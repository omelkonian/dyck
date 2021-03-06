import importlib
import random
import os
import pickle
import time
import argparse
import re
from math import ceil
from os.path import isfile
from pprint import pformat
from itertools import permutations

from MCFParser import *
from .grammar_utils import *
from .adhoc import *

########################################################################################################################
# 2017, Dr. Michael Moortgat, Utrecht University
########################################################################################################################
#
# Dyck generation
#
def shuffle(l, r):
    if not (l and r):  # left and/or right pack are empty
        return [l + r]
    else:
        return [l[0] + w for w in shuffle(l[1:], r)] + [r[0] + w for w in shuffle(l, r[1:])]


def dshuffle(l, r):
    return [l + r] if not (l and r) else\
        [(l, r)[i][0] + w for i in range(2) if not i or r[0] < l[0] for w in dshuffle(l[(i + 1) % 2:], r[i % 2:])]


def dyck_file(n):
    return 'data/{}.dyck'.format(n)


def dyck(k, n):
    # Utilize pre-generated Dyck words
    if isfile(dyck_file(n)):
        with open(dyck_file(n), 'r') as f:
            return f.read().splitlines()
    sigma = ''.join([chr(97+i) for i in range(k)])  # a,b,c,... (k letters)
    return [sigma*n] if n < 2 else sum([dshuffle(sigma, w) for w in dyck(k, n-1)], [])

def mix(k, n):
    sigma = ''.join([chr(97+i) for i in range(k)])  # a,b,c,... (k letters)
    return (word for word in permutations(sigma * n))


########################################################################################################################
# 2017, Orestis Melkonian & Konstantinos Kogkalidis, Utrecht University
########################################################################################################################
def rand_dyck(n):
    val = {
        'a': n,
        'b': 0,
        'c': 0
    }
    ret = ""
    while True:
        choices = [k for k, v in val.items() if v > 0]
        if not choices:
            break
        choice = choices[random.randint(0, len(choices) - 1)]
        ret += choice
        val[choice] -= 1
        if choice == 'a':
            val['b'] += 1
        elif choice == 'b':
            val['c'] += 1
    return ret


#
# Global constants
#
initial_symbol = 'S'
language = 'dyck'
languages = dict(dyck=dyck, mix=mix)

#
# Grammar class
#
class Grammar(object):

    def __init__(self, rules, **kwargs):
        # Normalize rules
        rules = sum(map(lambda r: r if isinstance(r, list) else [r],
                        map(lambda r: sum(r, []) if isinstance(r, list) and (not r or not isinstance(r[0], tuple)) else r,
                    rules)), [])
        # Construct rule tuples
        self.grammar = [('{}: {} <- {} ({})'.format(i, lhs, rhs, recipe), lhs, rhs, recipe)
                        for i, (lhs, rhs, recipe) in enumerate(rules, start=1)]
        kwargs.setdefault('topdown', True)
        kwargs.setdefault('filtered', True)
        kwargs.setdefault('nonempty', True)
        self.parser = Parser(self.grammar, [initial_symbol], **kwargs)

    def test_parse(self, word):
        return self.parser.chart_parse(list(word))

    def single_parse(self, word):
        print(self.format_parse(next(self.parser.parse(list(word)))))

    def parse(self, word):
        for t in self.parser.parse(list(word)):
            print('{}\n'.format(self.format_parse(t)))

    def min_parse(self, word):
        l, min_parse = 100, None
        for t in self.parser.parse(list(word)):
            p = self.format_parse(t)
            cur_l = len(p.split('\n'))
            if cur_l < l:
                l, min_parse = cur_l, p
        print('{}\n'.format(min_parse))

    def test_n(self, n, range=(0.0, 100.0), grammar_id='', start_time=None, stats=False):
        ws = languages[language](3, n)
        l = len(ws)
        start, end = map(lambda p: int(ceil(l * (p/100))), range)
        ws = ws[start:end]
        counters = []
        if stats and not os.path.exists('stats'):
            os.makedirs('stats')

        f = open('stats/{}_{}({}-{}\%).stats'.format(grammar_id, n, range[0], range[1]), 'wb') \
            if stats else sys.stdout

        f.write('Rule size: {}\n'.format(len(self.grammar)))
        f.write('Checking {} to {}\n'.format(start, end))
        if not stats:
            f.flush()
        c = 1
        for i, w in enumerate(ws):
            sys.stdout.write("\r{0:.2f}%".format(float(i) / float(len(ws)) * 100.0))
            sys.stdout.flush()
            if not self.parser.chart_parse(list(w)):
                counters.append(w)
                c += 1
        sys.stdout.write('\n')
        f.write('Result: {0} out of {1}\n'.format(c - 1, len(ws)))
        if start_time:
            f.write('Time elapsed: {} seconds\n'.format(time.time() - start_time))
        f.write('\n-------------------- COUNTERS --------------------\n')
        for counter in counters:
            f.write('{}\n'.format(counter))
        if stats:
            f.close()


    def test_soundness(self, n_range=range(1, 10)):
        for n in n_range:
            d = dyck(3, n)
            for w in permutations('abc' * n):
                s = "".join(w)
                if s not in d and self.parser.chart_parse(w):
                    print('[{}] UNSOUND for {}'.format(n, s))
                    return
            print('[{}] SOUND!'.format(n))

    @staticmethod
    def format_parse(s):
        return re.sub(r'\(.*\: ', '',
                      pformat(s, indent=3)
                      .replace('(0, 0)', 'x').replace('(0, 1)', 'y').replace('(1, 0)', 'z')
                      .replace('(1, 1)', 'w').replace(' [] ', '').replace('"', ''))


def all_commas(w, num_commas=1):
    if num_commas == 1:
        return [ w[:i] + '$' + w[i:] for i in range(len(w) + 1) ]
    elif num_commas == 2:
        return [ w[:i] + '$' + w[i:j] + '$' + w[j:]
                 for i in range(1, len(w))
                 for j in range(i + 1, len(w)) ]
    else:
        raise ValueError("all_commas does not support n > 3")

def main():
    parser = argparse.ArgumentParser(description='Grammar utilities for multidimensional Dyck languages.')
    parser.add_argument('-k', type=int, help='dimension', nargs='?', default=3)
    parser.add_argument('-n', type=int, help='number of "abc" occurences', nargs='?')
    parser.add_argument('-w', type=str, help='single word to check', nargs='?')
    parser.add_argument('-ws', type=str, help='file containing words to check', nargs='?')
    parser.add_argument('-p', type=str, help='single parse of a word', nargs='?')
    parser.add_argument('-minp', type=str, help='show minimal parse of a word', nargs='?')
    parser.add_argument('-ps', type=str, help='multiple parses of a word', nargs='?')
    parser.add_argument('-g', type=str, help='grammar to use', default='mcfg3')
    parser.add_argument('--lang', type=str, help='which language to check', default='dyck', nargs='?')
    parser.add_argument('-i', type=str, help='initial symbol to use', default='S', nargs='?')
    parser.add_argument('--rules', help='print all rules', action='store_true')
    parser.add_argument('--serialize', help='serialize grammar to file', action='store_true')
    parser.add_argument('--check', help='check soundness', action='store_true')
    parser.add_argument('--gen', help='generate dyck words', action='store_true')
    parser.add_argument('--range', type=str, default='0-100%', help='search in given percentage range')
    parser.add_argument('--time', help='measure execution time', action='store_true')
    parser.add_argument('--rand', help='generate random Dyck word', action='store_true')
    parser.add_argument('--stats', help='output in file', action='store_true')
    parser.add_argument('--stress', help='stress test given word', action='store_true')
    parser.add_argument('--adhoc', help='adhoc', action='store_true')
    args = parser.parse_args()

    # adhoc
    from tqdm import tqdm
    if args.adhoc:
        if args.n:
            for dw in tqdm(dyck(args.k, args.n)):
              # print('Word: {}'.format(dw))
              try:
                collapsible(dw)
              except RuntimeError:
                print('NAAAAY', dw)
                continue
                # exit(0)
            print('YAAAAAY')
        elif args.w:
            if 'a' not in args.w:
                args.w = args.w.replace('b', 'a').replace('c', 'b')
            if 'b' not in args.w:
                args.w = args.w.replace('c', 'b')
            try:
                collapsible(args.w)
            except RuntimeError:
                print('NAAAAY', args.w)
                exit(0)
            print('YAAAAAY')
        else:
            print('adhoc requires -n <int> or -w <word>')
        exit(0)

    # Comma stress testing
    if args.stress or '$' in (args.w or ''):
        args.i = '$W'

    # Set initial symbol
    global initial_symbol
    initial_symbol = args.i

    # Change language (if required)
    global language
    language = args.lang

    # Load grammar
    g = pickle.load(open('serialized_grammars/{}'.format(args.g), 'r')) \
        if '.grammar' in args.g else \
            getattr(importlib.import_module('.grammars.{}'.format(args.g), package='dyck'), args.g)

    # Start time
    start = time.time()

    if args.rules:
        if args.serialize:
            with open('serialized_grammars/{}.grammar'.format(args.g), 'wb') as f:
                pickle.dump(g, f)
        for r in map(lambda t: t[0], g.grammar):
            for k, v in tuple_to_char.items():
                r = r.replace(str(k), v)
            print(r)
        exit(0)

    # Stress-test
    if args.stress:
        for dw in tqdm(dyck(3, args.n)):
            for w in all_commas(dw, num_commas=2):
                # print('Testing: ', w)
                r = g.test_parse(w)
                # print(r)
                if r == False:
                    print('*** STRESS FAILED for n = {}!'.format(args.n))
                    # exit(0)
        print('*** STRESS COMPLETE for n = {}!'.format(args.n))


    if args.n is None and 'w' not in vars(args):
        exit(0)

    if args.rand:
        while True:
            r = rand_dyck(args.n)
            print('{}: {}'.format(r, g.test_parse(r)))
    elif args.gen:
        assert args.n
        ws = dyck(3, args.n)
        with open(dyck_file(args.n), 'w') as f:
            for w in ws:
                f.write('{}\n'.format(w))
    elif args.check:
        assert args.n
        g.test_soundness(n_range=[args.n])
    elif 'w' in vars(args) and args.w is not None:
        print(g.test_parse(args.w))
    elif 'p' in vars(args) and args.p is not None:
        g.single_parse(args.p)
    elif 'minp' in vars(args) and args.minp is not None:
        g.min_parse(args.minp)
    elif 'ps' in vars(args) and args.ps is not None:
        g.parse(args.ps)
    elif 'ws' in vars(args) and args.ws is not None:
        with open(args.ws, 'r') as f:
            for w in f.read().splitlines():
                print('{}: {}'.format(w, g.test_parse(w)))
    elif args.n:
        g.test_n(args.n, range=map(float, args.range.strip('%').split('-')),
                 grammar_id=args.g, start_time=start, stats=args.stats)
    else:
        exit(0)

    # End time
    if args.time:
        print('Time elapsed: {} seconds'.format(time.time() - start))


if __name__ == "__main__":
    main()
