from collections import defaultdict
from typing import TypedDict


class MapRow(TypedDict):
    source: int
    dest: int
    range: int
    diff: int


def get_data(file: str) -> tuple[dict[str, list[MapRow]], list[int]]:
    with open(f'data/{file}', 'r') as f:
        lines = f.read().splitlines()

    seeds = list(map(int, lines[0].split(': ')[-1].split(' ')))

    maps = defaultdict(list)
    map_key = None
    for line in lines[1:]:
        if 'map' in line:
            map_key = line.split(' ')[0]
            continue

        if line == '':
            continue

        dest_start, source_start, map_range = list(map(int, line.split(' ')))
        maps[map_key].append({
            'source': source_start,
            'dest': dest_start,
            'range': map_range,
            'diff': dest_start - source_start,
        })

    return maps, seeds


def apply_mapping(seeds: list[int], map_rows: list[MapRow]) -> list[int]:
    output = []
    for seed in seeds:
        seed_mapped = False
        for map_row in map_rows:
            if map_row['source'] <= seed <= map_row['source'] + map_row['range']:
                print(f'Seed {seed} maps to row {map_row=}')
                output.append(seed + map_row['diff'])
                seed_mapped = True
                break

        if not seed_mapped:
            print(f'Seed {seed} does not map to any rows')
            output.append(seed)

    return output


def solve_part1(file: str) -> int:
    maps, seeds = get_data(file)
    next_seeds = seeds
    for name, map_rows in maps.items():
        print(f'### Checking mapping for {name} ###')
        next_seeds = apply_mapping(next_seeds, map_rows)
        print()

    return min(next_seeds)


# TODO(ew) actually solve this. Want to avoid brute forcing, I feel like there is a more clever approach.
def solve_part2(file: str) -> int:
    maps, seeds = get_data(file)
    next_seeds = seeds
    for name, map_rows in maps.items():
        print(f'### Checking mapping for {name} ###')
        next_seeds = apply_mapping(next_seeds, map_rows)
        print()

    return min(next_seeds)


def main() -> None:
    assert solve_part1('day5-test.txt') == 35
    # 107430936
    print('Part 1:', solve_part1('day5.txt'))

    assert solve_part2('day5-test.txt') == 46


if __name__ == '__main__':
    main()
