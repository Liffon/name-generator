import csv
import numpy.random
import argparse

parser = argparse.ArgumentParser(description='Generate names.')
parser.add_argument('numberOfNames', metavar='N', type=int,
	nargs='?', default=1, help='Number of names to generate (defaults to 1)')
args = parser.parse_args()

numberOfNames = args.numberOfNames

class FrequencyCounter(dict):
	def __missing__(self, key):
		return 0

	# Expected file format:
	# <name> <a number of spaces> <relative frequency>
	def addEntriesFromFile(self, filename, weight=1):
		with open(filename, 'r') as f:
			reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
			for row in reader:
				if len(row) > 1:
					weight = float(row[1])
				else:
					weight = 1.0
				firstnames[row[0].lower()] += weight * float(row[1])

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

names = []
while len(names) < numberOfNames:
	name = numpy.random.choice(list(startletters.keys()), p=list(startletters.values()))
	while not name.endswith(' '):
		lastletter = name[-1]
		if not lastletter in nextletters:
			nextletters[lastletter] = FrequencyCounter()
			for digram in digrams:
				first = digram[0]
				second = digram[1]
				if first == lastletter:
					nextletters[lastletter][second] = \
						digrams[digram] / letters[first]
			nextletters[lastletter].normalize()

		name += numpy.random.choice(list(nextletters[lastletter].keys()), p=list(nextletters[lastletter].values()))

	if len(name) > 3:
		names.append(name[:-1].capitalize())

for name in names:
	print(name)
