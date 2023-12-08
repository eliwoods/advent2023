import math
import typing as t


class Race(t.TypedDict):
    time: int
    dist: int


def get_data(file: str) -> list[Race]:
    with open(f'data/{file}', 'r') as f:
        lines = f.read().splitlines()

    times = list(map(int, lines[0].split(':')[1].split()))
    dists = list(map(int, lines[1].split(':')[1].split()))

    return [{'time': t, 'dist': d} for t, d in zip(times, dists)]


def calc_dist_traveled(sec_held: int, total_sec: int) -> int:
    speed = sec_held
    return speed * (total_sec - sec_held)


def solve_part1(file: str) -> int:
    races = get_data(file)

    res = []
    for race in races:
        num_gt = 0
        for sec_held in range(race['time']):
            dist = calc_dist_traveled(sec_held, race['time'])
            if dist > race['dist']:
                num_gt += 1
        res.append(num_gt)

    return math.prod(res)


# TODO(ew) refactor this to just check the number of ways we don't beat the record and calculate
#  total - num ways to lose. This should be faster.
def solve_part2(file: str) -> int:
    races = get_data(file)

    time = int(''.join([str(r['time']) for r in races]))
    dist = int(''.join([str(r['dist']) for r in races]))

    num_gt = 0
    for sec_held in range(time):
        dist_travel = calc_dist_traveled(sec_held, time)
        if dist_travel > dist:
            num_gt += 1

    return num_gt


def main() -> None:
    assert solve_part1('day6-test.txt') == 288
    print('Part 1: ', solve_part1('day6-actual.txt'))

    assert solve_part2('day6-test.txt') == 71503
    print('Part 2: ', solve_part2('day6-actual.txt'))


if __name__ == '__main__':
    main()
