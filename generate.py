"""
This script generates text from model trained by train.py module
Next word is generated using weighted numpy.random.choice
with frequencies of words in text
The program has console interface, implemented with argparse module.
The first word to generate could be specified by user or
it will be chosen randomly.
!Note: if word specified is not presented int the text,
ValueError will be raised.
author: Igor Kotua
version: 1.0.2
"""


import argparse as ap
import random
import sys
import numpy
import pickle


def load_model(file):  # loading model
    """
    :type file: FileIO[bytes]
    :return dict of dicts of words and frequencies
    """
    return pickle.load(file)


def get_start_word(model, seed):  # getting first word of the text
    """
    :param model: dict containing model
    :param seed: word to start generation
    """
    if seed == '':
        return random.choice(list(model.keys()))
    if seed not in model.keys():
        raise ValueError('Invalid seed')
    return seed


def get_next_word(model, current_word):
    """
    :param model: dict containing model
    :param current_word: last outputted word in text
    """
    if current_word not in model:  # there are no words after current
        return numpy.random.choice(list(model.keys()))
    d = model[current_word]
    s = sum(d.values())
    p = [d[i] / s for i in d.keys()]  # probabilities for next word
    return numpy.random.choice(list(d.keys()), p=p)


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
        if i == length - 1:
            output.write(current_word + '\n')
        else:
            output.write(current_word + ' ')
            current_word = get_next_word(model, current_word)


def main():
    parse = ap.ArgumentParser(description='Generate some text')
    parse.add_argument('-m', '--model', help='File to read model from',
                       required=True)
    parse.add_argument('-s', '--seed', help='Word to start generation',
                       default='')
    parse.add_argument('-l', '--length', type=int, help='Length of text',
                       required=True)
    parse.add_argument('-o', '--output', help='File to output text',
                       default='')
    args = parse.parse_args()
    with open(args.model, 'rb') as in_file:
        if args.output == '':
            generate(in_file, args.seed, args.length, sys.stdout)
        else:
            with open(args.output, 'w') as out_file:
                generate(in_file, args.seed, args.length, out_file)


if __name__ == '__main__':
    main()
