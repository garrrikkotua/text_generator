"""
This script is a simple text generator, which uses bigram models.
Bigrams frequencies are counted using Counter module.
Model saves in byte format, using pickle module.
The program has console interface, implemented with argparse module.
For detailed information about usage please type -help in console.
author: Igor Kotua
version: 1.0.2
"""


import argparse as ap
import sys
import re
from collections import Counter
import os
import pickle
from collections import defaultdict


def gen_files(input_dir):  # yields file from input-dir
    """
    :param input_dir: directory of input files
    """
    if input_dir == '':
        yield sys.stdin
    else:
        if os.path.isfile(input_dir):  # lone file
            file = open(input_dir, 'r')
            yield file
            file.close()
        else:
            for dirpath, _, files in os.walk(input_dir):
                for filename in files:
                    file = open(os.path.join(dirpath, filename), 'r')
                    yield file
                    file.close()


def gen_lines(files, lowercase):  # yields line from file
    """
    :param files: iterable object containing files
    :param lowercase: bool saying whether to cast to lower or not
    """
    for file in files:
        for line in file:
            if lowercase:
                yield line.lower()
            else:
                yield line


def gen_words(lines):  # yields word from lines
    """
    :param lines: iterable of strings to evaluate
    """
    alphabet = re.compile(u'[а-яА-Яa-zA-Z]+')
    for line in lines:
        for word in alphabet.findall(line):
            yield word


def gen_bigrams(words, model):  # yields bigrams using words
    """
    :param words: iterable of strings, considered to be words
    """
    b1 = next(words)
    for b2 in words:
        yield (b1, b2)
        b1 = b2


def count_freq(bigrams, model):
    # counting frequencies of bigrams and writing to file
    """
    :param bigrams: iterable of tuples, containing two words
    :param model: str path to save model
    """
    c = Counter(bigrams)
    d = defaultdict(dict)
    for a, b in c.keys():  # dict of dicts of words and frequencies
        d[a][b] = c[(a, b)]
    with open(model, 'wb') as file:   # writing model to file
        pickle.dump(d, file)


def train(input_dir, model, lowercase):
    """
    :param input_dir: directory of input files
    :param model: str path to save model
    :param lowercase: bool saying whether to cast to lower or not
    """
    files = gen_files(input_dir)
    lines = gen_lines(files, lowercase)
    words = gen_words(lines)
    bigrams = gen_bigrams(words, model)
    count_freq(bigrams, model)


def main():
    parse = ap.ArgumentParser(description='Train on  some text')
    parse.add_argument('-i', '--input-dir', help='Input directory',
                       default='', required=True)
    parse.add_argument('-m', '--model',
                       help='Path to the file where model will be saved',
                       required=True)
    parse.add_argument('--lc', action='store_true', help='Make text lowercase')
    args = parse.parse_args()
    train(args.input_dir, args.model, args.lc)


if __name__ == '__main__':
    main()
