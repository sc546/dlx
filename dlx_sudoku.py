import argparse
from dlx import Graph

def main(args):
    board = args.board

    if len(board) != 81:
        print(f"ERROR: Invalid board length, expected 81 cells but received {len(board)}")
        return

    cells = list(board)
    for cell in cells:
        if cell not in [str(i) for i in range(0,10)]:
            print(f"ERROR: Invalid cell value, expected ones are in [0,9] but received {cell}")
            return

    universe = set() # Constraints.

    # Cell constraints.
    for row in range(1, 10):
        for col in range(1, 10):
            universe.add(f"CELL ({row},{col})")

    # Row constraints.
    for row in range(1, 10):
        for num in range(1, 10):
            universe.add(f"ROW {row} - NUM {num}")

    # Column constraints.
    for col in range(1, 10):
        for num in range(1, 10):
            universe.add(f"COL {col} - NUM {num}")

    # Box constraints.
    for box_row in range(0, 3):
        for box_col in range(0, 3):
            for num in range(1, 10):
                universe.add(f"BOX ({box_row},{box_col}) - NUM {num}")
    
    sets = [] # Assignments.
    
    # The actions are just a different representation for the assignments,
    # used when displaying the solution.
    actions = []
    
    for row in range(1, 10):
        for col in range(1, 10):
            board_num = int(board[(row-1)*9 + (col-1)])
            nums = [board_num] if board_num != 0 else range(1, 10)
            for num in nums:
                s = set()
                
                # Cell constraint.
                s.add(f"CELL ({row},{col})")

                # Row constraint.
                s.add(f"ROW {row} - NUM {num}")

                # Column constraint.
                s.add(f"COL {col} - NUM {num}")

                # Box constraint.
                box_row = (row - 1) // 3
                box_col = (col - 1) // 3
                s.add(f"BOX ({box_row},{box_col}) - NUM {num}")

                sets.append(s)
                actions.append(((row-1, col-1), num))

    graph = Graph(universe, sets)
    solution_found, solution = graph.solve()
    
    if solution_found:
        grid = [[0]*9 for _ in range(9)]
        for set_idx in solution:
            (row, col), num = actions[set_idx]
            grid[row][col] = num
        
        print("Solution found:")
        for row in grid:
            for cell in row:
                print(cell, end=" ")
            print("\n", end="")
    else:
        print("No solution found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "board",
        help="""
        The board represented as 1D string, without spaces and using 0s for
        empty cells.
        For example, the following is a valid board:
        006071030000040070000056900010004050080030000700500600068020000042900007097003500.           
        The 81 characters represent the value of each cell, read row-by-row.
        """
    )

    args = parser.parse_args()

    main(args)

