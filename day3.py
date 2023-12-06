"""
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

--- Part Two ---
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

# Consts
GENERAL_SYMBOL = '#'
GEAR_SYMBOL = '*'

DIRECTION_MAP = {
    0: (-1, -1),
    1: (-1, 0),
    2: (-1, 1),
    3: (0, -1),
    4: (0, 1),
    5: (1, -1),
    6: (1, 0),
    7: (1, 1),
}

# Types
SchematicItem = int | str | None
Schematic = list[list[SchematicItem]]
SymbolLocations = list[tuple[int, int, str]]


def handle_schematic_item(input: str) -> SchematicItem:
    if input == '.':
        return None
    elif input == '*':
        return GEAR_SYMBOL
    elif input.isnumeric():
        return int(input)
    else:
        return GENERAL_SYMBOL


def get_data(file: str) -> Schematic:
    output = []
    with open(f'data/{file}', 'r') as f:
        for line in f:
            output.append(list(map(handle_schematic_item, line.strip('\n'))))

    return output


def get_symbol_locations(schematic: Schematic) -> SymbolLocations:
    locations = []
    for i, row in enumerate(schematic):
        for j, item in enumerate(row):
            if item in (GENERAL_SYMBOL, GEAR_SYMBOL):
                locations.append((i, j, item))

    return locations


def find_part_numbers(schematic: Schematic, symbol_locations: SymbolLocations) -> tuple[
    set[int], list[tuple[int, ...]]]:
    """
    The direction encoding scheme is as follows for a given symbol
    0 1 2
    3 * 4
    5 6 7
    """
    part_numbers = set()
    gear_ratios = []
    num_schematic_rows = len(schematic)
    num_schematic_cols = len(schematic[0])
    for row, col, symbol in symbol_locations:
        # Get directions we want to search if
        allowed_directions = DIRECTION_MAP.copy()
        # If symbol in top row exclude searching above
        if row == 0:
            allowed_directions.pop(0, None)
            allowed_directions.pop(1, None)
            allowed_directions.pop(2, None)
        # If symbol in bottom row exclude searching below
        elif row == num_schematic_rows - 1:
            allowed_directions.pop(5, None)
            allowed_directions.pop(6, None)
            allowed_directions.pop(7, None)

        # If symbol on left col, only search to the right
        if col == 0:
            allowed_directions.pop(0, None)
            allowed_directions.pop(3, None)
            allowed_directions.pop(5, None)
        # If symbol on right col, only search to the left
        elif col == num_schematic_cols - 1:
            allowed_directions.pop(2, None)
            allowed_directions.pop(4, None)
            allowed_directions.pop(7, None)

        adjacent_parts = set()
        for direction in allowed_directions.values():
            part_number_id = schematic[row + direction[0]][col + direction[1]]
            if part_number_id is not None:
                adjacent_parts.add(part_number_id)

        if symbol == GEAR_SYMBOL and len(adjacent_parts) == 2:
            gear_ratios.append(tuple(adjacent_parts))

        part_numbers.update(adjacent_parts)

    return part_numbers, gear_ratios


def map_part_numbers(schematic: Schematic) -> tuple[Schematic, dict[int, int]]:
    """
    Generates unique IDs for each part number and remaps the schematic. This simplifies the search later as we just
    need to find all unique part numbers
    """
    new_schematic = []
    part_number_map = {}
    current_part_number = 0
    current_number = None
    for row in schematic:
        new_row = []
        for item in row:
            if item not in (GENERAL_SYMBOL, GEAR_SYMBOL) and item is not None:
                if current_number is None:
                    current_number = [str(item)]
                else:
                    current_number.append(str(item))
                new_row.append(current_part_number)
            else:
                if current_number is not None:
                    part_number = int(''.join(current_number))
                    part_number_map[current_part_number] = part_number
                    current_part_number += 1
                    current_number = None
                new_row.append(item)

        new_schematic.append(new_row)

    return new_schematic, part_number_map


def solve_part_1(file: str) -> int:
    schematic = get_data(file)
    symbol_locations = get_symbol_locations(schematic)
    mapped_schematic, part_number_map = map_part_numbers(schematic)
    part_numbers, _ = find_part_numbers(mapped_schematic, symbol_locations)
    return sum(map(lambda x: part_number_map[x], part_numbers))


def solve_part_2(file: str) -> int:
    schematic = get_data(file)
    symbol_locations = get_symbol_locations(schematic)
    mapped_schematic, part_number_map = map_part_numbers(schematic)
    _, gear_ratios = find_part_numbers(mapped_schematic, symbol_locations)
    return sum([part_number_map[gr[0]] * part_number_map[gr[1]] for gr in gear_ratios])


def main() -> None:
    assert solve_part_1('day3-test.txt') == 4361
    print('Part 1:', solve_part_1('day3.txt'))

    assert solve_part_2('day3-test.txt') == 467835
    print('Part 2:', solve_part_2('day3.txt'))


if __name__ == '__main__':
    main()
