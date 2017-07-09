assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    boxes = cross(rows, cols)
    i = 0
    sudoku_dict = {}
    while i < 81:
        for b in boxes:
            if grid[i] == '.':
                sudoku_dict[b] = '123456789'
            else:
                sudoku_dict[b] = grid[i]
            i += 1

    return sudoku_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    boxes = cross(rows, cols)
    # This finds the max number of characters in each box and adds one.
    # the max will be '123456789' so 9 + 1 = 10
    width = 1+max(len(values[s])for s in boxes)

    # This will create 30 dashes separated with a "+" 3x
    line = '+' .join(['-'*(width*3)]*3)

    # This builds the board.  It iterates through [A1, A2, etc.] and then
    # uses the .center method to center whatever value is in that cell.
    # It adds a | in-between columns 3 & 6 otherwise an empty string.
    # It prints a line if the row is C or F
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    boxes = cross(rows, cols)

    # Creates an array with arrays of the row keys
    # [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['B1', 'B2', ...], [..], ..]
    row_units = [cross(r, cols) for r in rows]

    # Creates an array with arrays of the column keys
    # [['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['A2', 'B2', ...], [..], ..]
    column_units = [cross(rows, c) for c in cols]

    # Creates an array with arrays of the square units
    # [['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], ['A4', 'A5', ...], [..], ..]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

    unitlist = row_units + column_units + square_units

    # Iterates through each key (i.e.: 'A1', 'A2', 'A3', ...) and then loops through all of the arrays in
    # unitlist and adds the array to the dictionary value IF the key is included.  Basically creates a
    # dictionary with each key as the key & then the values are the arrays that include that key.
    # Ex: {'A1': [['A1', ...], ['A1', ...], ['A1', ...], [...]], 'A2': [['A2', ...], ['A2', ...], [...]], etc.}
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

    # This creates a dictionary.  It loops through each key (i.e. 'A1', 'A2', 'A3', etc.) and then sets the value
    # to the peers.  It does this by using the sum method to create one array of all of the units for that key.  It
    # then uses the set function to create a set (i.e. {} vs. []) of those values, and then subtracts out the key
    # from that set i.e. if it's on 'A1', the end set of values will not include 'A1'
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

    # Iterate through each box & check the length of the value.  If it's one,
    # keep it in the array.
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        # Get value of the solved box
        digit = values[box]
        # Iterate through all of the peers for the box
        for peer in peers[box]:
            # Remove the digit from the possible answer for all of the peers
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    # Creates an array with arrays of the row keys
    # [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['B1', 'B2', ...], [..], ..]
    row_units = [cross(r, cols) for r in rows]

    # Creates an array with arrays of the column keys
    # [['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['A2', 'B2', ...], [..], ..]
    column_units = [cross(rows, c) for c in cols]

    # Creates an array with arrays of the square units
    # [['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], ['A4', 'A5', ...], [..], ..]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

    unitlist = row_units + column_units + square_units

    # unit is an array ['A1', 'A3', 'A4', ...]
    for unit in unitlist:
        for digit in '123456789':
            # Iterates through each key in the unit array and checks if the digit is in the value for that
            # key from the original values dictionary.  If yes, it will include that box in the new array.
            digit_places = [box for box in unit if digit in values[box]]

            # If there is only one box which would allow a certain digit (i.e. the length is 1) then update the
            # values dictionary with that digit
            if len(digit_places) == 1:
                values[digit_places[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        eliminate(values)

        # Use the Only Choice Strategy
        only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):

    "Using depth-first search and propagation, try all possible values."
    boxes = cross(rows, cols)

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    length, square = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[square]:
        new_sudoku = values.copy()
        new_sudoku[square] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    search(values)

    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
