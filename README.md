# name-generator

This is a name generator that uses word lists of common names to generate new ones.

Why? Because it's pretty hilarious.

## Expected file format

The file format is a space-separated file, with names in the first column and relative frequency in the second, for example
```
Alice   2.1
Bob     1.8
```

The data included in the repository is from [The United States Census Bureau](https://www.census.gov/topics/population/genealogy/data/1990_census/1990_census_namefiles.html)
(the files are taken as-is from that link) and Statistics Sweden ([Statistiska Centralbyrån](http://www.statistikdatabasen.scb.se/pxweb/en/)).
