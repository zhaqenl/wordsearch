Word Search
===========


Summary
-------

This is a Python implementation of the [Word Search](https://rosettacode.org/wiki/Word_search)
puzzle, but with a few modifications, namely:

- The grid doesn’t have a dimension limitation of 10 by 10.
- The word doesn’t have a length limitation of three characters.
- The word doesn’t have to contain only the alphabetic characters.
- There is no hidden word in the grid.


Usage
-----

Clone this repo:

```
$ git clone https://github.com/zhaqenl/wordsearch/ ~/python/wordsearch
```

### REPL

Run the following command in your terminal:

```
$ python
>>>
```

Once inside the interactive interpreter, type:

```
>>> import core
>>>
```

If you only want the quantity of matches of a word inside a grid, run:

```
>>> core.wordsearch('cat', """catt
... aata
... tatc""", '\n')
4
>>>
```

If you want a different character as a separator, change the separator inside the grid and the
corresponding separator argument of the function (naturally, use a unique character for the
separator):

```
>>> core.wordsearch('cat', 'catt aata tatc', ' ')
4
>>> core.wordsearch('cat', 'catt;aata;tatc', ';')
4
>>> core.wordsearch('cat', 'cattxaataxtatc', 'x')
4
```

However, if you want to display the coordinates, themselves, of the matches, run the `find_matches`
function inside `core`:

```
>>> core.find_matches('cat', """catt
aata
tatc""", '\n')
[[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (1, 1), (2, 2)], [(2, 3), (1, 3),
(0, 3)]]
```

### File input

If you prefer a file as the input of the script, you could create a file whose first line indicates
the amount of grid-to-word pairs, followed by the row quantity of the first pair, followed by its
column quantity, then the string grid itself, and finally, the hidden word. See `dummy-input.txt`
for an example structure.

After creating the `.txt` file, run the following:

```
$ python wordsearch.py dummy_input.txt
Case 1: 4
Case 2: 1
Case 3: 4
```

If you’re interested in measuring the script’s speed, append `time` at the start of the previous
command:

```
$ time python wordsearch.py dummy_input.txt
```

If you want a little more speed, use [Pypy](https://www.pypy.org/), an alternative implementation of
the Python language:

```
$ pypy wordsearch.py dummy_input.txt
Case 1: 4
Case 2: 1
Case 3: 4
```
