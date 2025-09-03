# Dancing Links (DLX) - Exact Cover Solver

This Python script implements Donald Knuth's Dancing Links (DLX) algorithm to solve Exact Cover problems.

Given a universe of items and a collections of sets, the program finds a subset of sets whose union exactly covers the universe (no duplicates or omissions).

## Example Usage

```
python dlx.py "a, b, c" "a, c" "b"
```

- First argument is the universe (comma-separated items)
- Other argument are the sets (also comma-separated).

### Visualization 

There are two additional options:
- `visualize`: Generate a PNG visualization of the DLX graph (default is off).
- `visualize_filename`: Output filename for the visualization PNG (default is `dlx_graph`).

For example:

```
python dlx.py "a, b, c" "a, c" "b" --visualize --visualize_filename "my_graph"
```

Generates `my_graph.png` with Graphviz.

## Requirements

- Python 3.6+
- `graphviz` Python package and system binary (for visualization only)

