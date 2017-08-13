#!/usr/bin/env python3

import csv
import os
import numpy.random


class FrequencyCounter(dict):
    def __missing__(self, key):
        return 0

    # Expected file format:
    # <name> <at least one space> <relative frequency>
    def addEntriesFromFile(self, filename, weight=1):
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
            for row in reader:
                if len(row) > 1:
                    weight = float(row[1])
                else:
                    weight = 1.0
                self[row[0].lower()] += weight * float(row[1])

    def normalize(self):
        p = 0
        for key, val in self.items():
            p += val
        for key in self:
            self[key] = self[key] / p


startletters = FrequencyCounter()
digrams = FrequencyCounter()
letters = FrequencyCounter()

firstnames = FrequencyCounter()
nextletters = dict()


def init():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    firstnames.addEntriesFromFile(os.path.join(__location__, 'dist.male.first.txt'))
    firstnames.addEntriesFromFile(os.path.join(__location__, 'dist.female.first.txt'))

    for name, frequency in firstnames.items():
        for idx in range(len(name) - 2):
            digram = name[idx] + name[idx + 1]
            digrams[digram] += frequency
            letters[name[idx]] += frequency
        digrams[name[len(name) - 1] + ' '] += frequency
        startletters[name[0]] += frequency

    digrams.normalize()
    startletters.normalize()
    letters.normalize()


def next_letter(name):
    if name == '':
        return numpy.random.choice(list(startletters.keys()), p=list(startletters.values()))
    else:
        lastletter = name[-1:]

        if not lastletter in nextletters:
            nextletters[lastletter] = FrequencyCounter()
            for digram in digrams:
                previous = digram[0]
                current = digram[1]
                if previous == lastletter:
                    nextletters[lastletter][current] = \
                        digrams[digram] / letters[previous]
            nextletters[lastletter].normalize()

        candidates = list(nextletters[lastletter].keys())
        probabilities = list(nextletters[lastletter].values())
        return numpy.random.choice(candidates, p=probabilities)


def generate(prefix=''):
    name = prefix
    while not name.endswith(' '):
        name += next_letter(name)

    if len(name) > 3:  # length including trailing space
        return name[:-1].capitalize()
    else:
        return generate(prefix)
