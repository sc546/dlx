# Dancing Links (DLX) - Exact Cover Solver

This repository contains an implementation of
[Donald Knuth's Dancing Links (DLX) algorithm](https://en.wikipedia.org/wiki/Dancing_Links)
to solve [Exact Cover](https://en.wikipedia.org/wiki/Exact_cover) problems.

Given a universe of items and a collections of sets, the program finds a subset
of sets whose union exactly covers the universe.

As an example, a Sudoku solver which makes use of this implementation is also
included.

## Example Usage

### Stand-alone program

[`dlx.py`](https://github.com/sc546/dlx/blob/main/dlx.py) can be used as a
stand-alone program, like:

```
python dlx.py "a, b, c" "a, c" "b"
```

- First argument is the universe (comma-separated items).
- Other argument are the sets (also comma-separated).

There are two optional arguments, useful for visualization:
- `visualize`: Generate a PNG visualization of the DLX graph (default is off).
- `visualize_filename`: Output filename for the visualization PNG (default is
`dlx_graph`).

For example:

```
python dlx.py "a, b, c" "a, c" "b" --visualize --visualize_filename "my_graph"
```

Generates `my_graph.png` with Graphviz.


### Library

[`dlx.py`](https://github.com/sc546/dlx/blob/main/dlx.py) can also be used as a
library, like in [`dlx_sudoku.py`](https://github.com/sc546/dlx/blob/main/dlx_sudoku.py).
This program receives an incomplete Sudoku board as an argument, extracts the
equivalent Exact Cover problem and searches for a solution.

The board has to be be passed as 1D string, without spaces and using 0s to
represent empty cells.

For example:

```
python dlx_sudoku.py 006071030000040070000056900010004050080030000700500600068020000042900007097003500
```

Returns a valid solution to the given Sudoku board.

## Requirements

- Python 3.6+.
- `graphviz` [Python package](https://pypi.org/project/graphviz/) and
[system binary](https://graphviz.org/) (for visualization only).

