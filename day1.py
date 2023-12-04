import re

NUMS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

INT_MATCH = re.compile('[1-9]')


def get_data(file: str) -> list[str]:
    with open(f'data/{file}', 'r') as f:
        return f.read().splitlines()


def process_line_regex(line: str) -> int:
    matches = INT_MATCH.findall(line)
    nums = list(map(lambda x: NUMS[x] if x in NUMS else x, matches))
    return int(f'{nums[0]}{nums[-1]}')


def solve_part_1(file: str) -> int:
    data = get_data(file)
    vals = map(process_line_regex, data)
    return sum(vals)


def process_line_literals(line: str) -> int:
    nums = []
    for i in range(len(line)):
        for literal, num in NUMS.items():
            if ''.join(line[i:i + len(literal)]) == literal or line[i] == str(num):
                nums.append(num)
                break
    return int(f'{nums[0]}{nums[-1]}')


def solve_part_2(file: str) -> int:
    data = get_data(file)
    vals = map(process_line_literals, data)
    ans = sum(vals)
    return ans


def main():
    assert solve_part_1('day1-part1-test.txt') == 142
    # 55712
    print('Part 1:', solve_part_1('day1.txt'))

    assert solve_part_2('day1-part2-test.txt') == 281
    # 55413
    print('Part 2:', solve_part_2('day1.txt'))


if __name__ == '__main__':
    main()
