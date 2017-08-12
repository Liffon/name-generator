#!/usr/bin/env python3

import csv
import numpy.random
import argparse

parser = argparse.ArgumentParser(description='Generate names.')
parser.add_argument('numberOfNames', metavar='n', type=int,
	nargs='?', default=1, help='Number of names to generate (defaults to 1)')
parser.add_argument('nameSeed', metavar='seed',
	nargs='?', default='', help='Seed that all generated names start with')
args = parser.parse_args()

numberOfNames = args.numberOfNames
nameSeed = args.nameSeed

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


#firstnames.addEntriesFromFile('dist.male.first.txt')
#firstnames.addEntriesFromFile('dist.female.first.txt')
firstnames.addEntriesFromFile('swedish-male-firstnames.csv')
firstnames.addEntriesFromFile('swedish-female-firstnames.csv')

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

nextletters = dict()

def nextLetter(name):
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


def generate(number_of_names=1, prefix=''):
    print(prefix)
    names = []
    while len(names) < number_of_names:
        name = prefix
        while not name.endswith(' '):
            name += nextLetter(name)

        if len(name) > 3:
            names.append(name[:-1].capitalize())
    if number_of_names == 1:
        return names[0]
    else:
        return names


def main():
    names = generate(numberOfNames, nameSeed)
    for name in names:
        print(name)


if __name__ == '__main__':
    main()
