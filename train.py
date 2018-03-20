import argparse as ap
import sys
import re
from collections import Counter
import os
from collections import defaultdict


def previous_bigrams(model):  # loads current mode if file is not empty
    """
    :type model: str
    """
    d = defaultdict(lambda: 0)
    with open(model, 'r') as file:
        for line in file:
            w1, w2, count = line.rstrip().split()
            d[(w1, w2)] = int(count)
    return d


def gen_files(input_dir):  # yields file from input-dir
    """
    :param input_dir: directory of input files
    """
    directory = os.listdir(path=input_dir)
    for path in directory:
        file = open(os.path.join(input_dir, path), 'r')
        yield file
        file.close()


def gen_lines(files, lowercase):  # yields line from file
    """
    :param files: iterable object containing files
    :param lowercase: bool saying whether to cast to lower or not
    """
    if lowercase:
        for file in files:
            for line in file:
                yield line.lower()
    else:
        for file in files:
            for line in file:
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
    b1 = '*start*'
    for b2 in words:
        yield (b1, b2)
        b1 = b2


def count_freq(bigrams, model):  # counting frequencies of bigrams and writing to file
    """
    :param bigrams: iterable of tuples, containing two words
    :param model: str path to save model
    """
    c = Counter(bigrams)
    d = previous_bigrams(model)
    for bigram, count in c.items():  # updating model
        d[bigram] += count
    with open(model, 'w') as file:   # writing model to file
        for bigram in d:
            w1, w2 = bigram
            file.write('{} {} {}\n'.format(w1, w2, d[bigram]))


def train(input_dir, model, lowercase):
    """
    :param input_dir: directory of input files
    :param model: str path to save model
    :param lowercase: bool saying whether to cast to lower or not
    """
    if input_dir != '':
        files = gen_files(input_dir)
        lines = gen_lines(files, lowercase)
        words = gen_words(lines)
        bigrams = gen_bigrams(words, model)
        count_freq(bigrams, model)
    else:   # input-dir is not specified, writing to sys.stdin
        lines = gen_lines([sys.stdin], lowercase)
        words = gen_words(lines)
        bigrams = gen_bigrams(words, model)
        count_freq(bigrams, model)


parse = ap.ArgumentParser(description='Train on  some text')
parse.add_argument('-i', '--input-dir', type=str, help='Input directory', default='', required=True)
parse.add_argument('-m', '--model', type=str, help='Path to the file where model will be saved', required=True)
parse.add_argument('--lc', action='store_true', help='Make text lowercase')
args = parse.parse_args()
train(args.input_dir, args.model, args.lc)
