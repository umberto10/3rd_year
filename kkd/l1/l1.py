#!/usr/bin/env python

import numpy as np
import math, sys, getopt
import collections as coll

chars = []

def read_file(fn):
    with open(fn, 'rb') as f:
        while byte := f.read(1):
            chars.append(byte)
    return chars

'''
BABABACACA
0 = {'B': 1}
A = {'B': 2, 'C':2}
B = {'A': 3}
'''

def count_chars(chars):
    single = coll.Counter(chars)
    pairs = coll.Counter(zip([b'\x00'] + chars, chars))

    # {A, B}: 2 -> A = {B: 2}
    return (dict(single), dict(pairs), len(chars), len(list(zip([b'\x00'] + chars, chars))))


def entr(counts):
    single, pairs, f_len, _ = counts
    entr = 0
    for k, v in single.items():
        p = v / f_len
        entr -= p * math.log2(p)

    return entr


def cnd_entr(counts):
    single, pairs, f_len, _ = counts
    cnd_entr = 0
    for k, v in single.items():
        cnd_entr += (v / f_len) * H(counts, (k, v))
        # fn(counts, (k, v)) #(v / f_len) * H(counts, (k, v))

    return cnd_entr


def fn(counts, pi):
    single, pairs, f_len, p_len = counts
    s = 0
    for k, val in pairs.items():
        if k[0] == pi[0]:
            s += val * (log2(single[k]) - log2(val))

    return s


def H(counts, pi):
    single, pairs, f_len, p_len = counts
    px = pi[1] / f_len
    s = 0

    for k, val in pairs.items():
        if k[0] == pi[0]:
            s += (math.log2((val / p_len) / px) * (val / p_len) / px)

    return -1 * s


def main():

    human = False
    options, args = getopt.gnu_getopt(sys.argv[1:], 'h', ['human',])
    for opt, arg in options:
        if opt in ('-h', '--human'):
            human = True

    for f in args:
        cnts = count_chars(read_file(f))
        ent = entr(cnts)
        cnd_ent = cnd_entr(cnts)
        diff = abs(ent - cnd_ent)
        if human:
            print(f)
            print('Entropy: ', ent)
            print('Condition Entropy: ', cnd_ent)
            print('Diff: ', diff)
            print()
        else:
            print(f"{ent} {cnd_ent} {diff}")

if __name__ == '__main__':
    main()
