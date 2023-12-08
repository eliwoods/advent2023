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


def merge_ranges(ranges: list[list[int]]) -> list[list[int]]:
    if len(ranges) < 2:
        return ranges

    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    merged_ranges = []
    prev_interval = sorted_ranges[0]
    for interval in sorted_ranges[1:]:
        if prev_interval[1] >= interval[0]:
            prev_interval[1] = max(interval[1], prev_interval[1])
        else:
            merged_ranges.append(prev_interval)
            prev_interval = interval
    merged_ranges.append(prev_interval)

    return merged_ranges


# TODO(ew) need to handle partial ranges for mapping
def apply_range_mapping(seed_ranges: list[list[int]], map_rows: list[MapRow]) -> list[list[int]]:
    output = []

    for seed_range in seed_ranges:
        seed_range_min = seed_range[0]
        seed_range_max = seed_range[1]
        mapped = False

        range_output = []
        # TODO Need to consider the fact that overlaps could split range into >2 parts; don't think we have to merge tho
        for map_row in map_rows:
            if map_row['source'] <= seed_range_min <= map_row['source'] + map_row['range'] and map_row['source'] <= seed_range_max <= map_row['source'] + map_row['range']:
                print(f'Seed range {seed_range=} maps to row {map_row=}')
                mapped_range = [seed_range_min + map_row['diff'], seed_range_max + map_row['diff']]
                range_output.append(mapped_range)
                mapped = True
                break
            if map_row['source'] <= seed_range_min <= map_row['source'] + map_row['range'] and not(map_row['source'] <= seed_range_max <= map_row['source'] + map_row['range']):
                mapped_range = [seed_range_min + map_row['diff'], map_row['source'] + map_row['range'] + map_row['diff'] - 1]
                unmapped_range = [map_row['source'] + map_row['range'], seed_range_max]
                range_output.extend([mapped_range, unmapped_range])
                print(f'Seed range {seed_range=} partially maps to row {map_row=}, upper bound out of map range.')
                print(f'Mapped range {mapped_range=}')
                print(f'Unmapped range {unmapped_range=}')
                mapped = True
                continue
            if not(map_row['source'] <= seed_range_min <= map_row['source'] + map_row['range']) and map_row['source'] <= seed_range_max <= map_row['source'] + map_row['range']:
                mapped_range = [map_row['source'] + map_row['diff'], seed_range_max + map_row['diff']]
                # unmapped_range = [seed_range_min, seed_range_max - map_row['source']]
                unmapped_range = [seed_range_min, map_row['dest'] - map_row['diff'] - 1]
                range_output.extend([mapped_range, unmapped_range])
                print(f'Seed range {seed_range=} partially maps to row {map_row=}, lower bound out of map range.')
                print(f'Mapped range {mapped_range=}')
                print(f'Unmapped range {unmapped_range=}')
                mapped = True
                continue

        if not mapped:
            print(f'Seed range {seed_range=} does not map to any rows')
            unmapped_range = [seed_range_min, seed_range_max]
            range_output.append(unmapped_range)

        # TODO(ew) I don't think we have to do this
        # output += merge_ranges(range_output)
        output += range_output

    return output


def solve_part1(file: str) -> int:
    maps, seeds = get_data(file)
    next_seeds = seeds
    for name, map_rows in maps.items():
        print(f'### Checking mapping for {name} ###')
        next_seeds = apply_mapping(next_seeds, map_rows)
        print()

    return min(next_seeds)


def solve_part2(file: str) -> int:
    maps, seeds = get_data(file)
    seed_ranges = [[seeds[2*i], seeds[2*i] + seeds[2*i+1]] for i in range(len(seeds)//2)]

    next_seed_ranges = seed_ranges
    for name, map_rows in maps.items():
        print(f'### Checking mapping for {name} ###')
        next_seed_ranges = apply_range_mapping(next_seed_ranges, map_rows)
        print()

    print(sorted(next_seed_ranges))
    seeds = []
    for seed_range in next_seed_ranges:
        seeds.extend(seed_range)

    return min(seeds)


def main() -> None:
    # assert solve_part1('day5-test.txt') == 35
    # # 107430936
    # print('Part 1:', solve_part1('day5-actual.txt'))

    # supposed expected output without merging
    # [[46, 56], [56, 60], [60, 61], [82, 85], [86, 90], [94, 97], [97, 99]]
    assert solve_part2('day5-test.txt') == 46
    # print('Part 2:', solve_part2('day5-actual.txt'))


if __name__ == '__main__':
    main()
