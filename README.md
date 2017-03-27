# name-generator

This is a name generator that uses word lists of common names to generate new ones.

Why? Because it's pretty hilarious.

## Requirements

Numpy is needed to run.

## Usage

`namegenerator.py` takes two optional arguments:

1. The number of names to be generated (default 1)
2. The "seed" that every generated name starts with

If run without arguments, it simply prints one generated name and exits.

### Example

```
$ ./namegenerator.py 
Erinde
$ ./namegenerator.py 5
Enn
Joll
Andr
Rikandelisp
Culoa
$ ./namegenerator.py 5 Er
Erofann
Ergn
Erimicus
Ericilikal
Erisol
```

## File format

By default, the files `swedish-female-firstnames.csv` and `swedish-female-firstnames.csv` are used as input.

The files are space-separated, with names in the first column and relative frequency in the second, for example
```
Alice   2.1
Bob     1.8
```

The data included in the repository is from Statistics Sweden ([Statistiska Centralbyrån](http://www.statistikdatabasen.scb.se/pxweb/en/), some data-mangling done by me) and [The United States Census Bureau](https://www.census.gov/topics/population/genealogy/data/1990_census/1990_census_namefiles.html)
(the files are taken as-is from that link).
