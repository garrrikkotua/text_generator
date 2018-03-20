import argparse as ap
import random
import sys
from collections import defaultdict


def load_model(file):  # loading model
    """
    :type file: _io.TextIOWrapper
    """
    d = defaultdict(dict)
    for line in file:
        w1, w2, count = line.split()
        d[w1][w2] = int(count)
    return d


def get_start_word(model, seed):  # getting first word of the text
    """
    :param model: dict containing model
    :param seed: word to start generation
    """
    if seed == '':
        return random.choice(list(model.keys()))
    else:
        if seed not in model.keys():
            raise ValueError('Invalid seed')
        return seed


def get_next_word(model, current_word):  # cumulative distribution to get next word
    """
    :param model: dict containing model
    :param current_word: last outputted word in text
    """
    a = list(model[current_word].keys())
    b = list(model[current_word].values())
    return random.choices(a, weights=b, k=1)[0]


def generate(file, seed, length, output):
    """
    :type file: _io.TextIOWrapper
    :param seed: word to start generation
    :param length: length of sequence to output
    :param output: file to output
    """
    model = load_model(file)
    current_word = get_start_word(model, seed)
    for i in range(length):
        output.write('{} '.format(current_word))
        current_word = get_next_word(model, current_word)


parse = ap.ArgumentParser(description='Generate some text')
parse.add_argument('-m', '--model', type=str, help='File to read model from', required=True)
parse.add_argument('-s', '--seed', type=str, help='Word to start generation', default='')
parse.add_argument('-l', '--length', type=int, help='Length of text to generate', required=True)
parse.add_argument('-o', '--output', type=str, help='File to output generated text', default='')
args = parse.parse_args()
with open(args.model, 'r') as in_file:
    if args.output == '':
        generate(in_file, args.seed, args.length, sys.stdout)
    else:
        with open(args.output, 'w') as out_file:
            generate(in_file, args.seed, args.length, out_file)
