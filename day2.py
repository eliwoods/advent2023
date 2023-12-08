"""
As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?

--- Part Two ---

As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?

"""

COLORS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

RoundData = dict[str, int]
GameData = list[RoundData]


def parse_game_id(game_id: str) -> int:
    return int(game_id.split(' ')[1])


def parse_game_data(game_data: str) -> GameData:
    output = []
    game_rounds = game_data.split('; ')
    for game_round in game_rounds:
        game_output = {}
        round_values = game_round.split(', ')
        for round_value in round_values:
            num, color = round_value.split(' ')
            game_output[color] = int(num)

        output.append(game_output)

    return output


def load_data(file: str) -> dict[int, GameData]:
    with open(f'data/{file}', 'r') as f:
        lines = f.read().splitlines()

    output = {}
    for line in lines:
        game_id_str, game_data_str = line.split(': ')
        game_id = parse_game_id(game_id_str)
        game_data = parse_game_data(game_data_str)
        output[game_id] = game_data

    return output


def _round_is_feasible(round_data: RoundData) -> bool:
    return all(COLORS[color] >= val for color, val in round_data.items())


def solve_part_1(file: str) -> int:
    games = load_data(file)
    feasible_games = []
    for game_id, game_data in games.items():
        if all(_round_is_feasible(round_data) for round_data in game_data):
            feasible_games.append(game_id)

    return sum(feasible_games)


def solve_part_2(file: str) -> int:
    games = load_data(file)
    game_powers = []
    for game_data in games.values():
        game_max = {
            'red': 0,
            'green': 0,
            'blue': 0
        }

        for round_ in game_data:
            for color, num in round_.items():
                if num > game_max[color]:
                    game_max[color] = num

        game_powers.append(game_max['red'] * game_max['green'] * game_max['blue'])

    return sum(game_powers)


def main():
    assert solve_part_1('day2-part1-test.txt') == 8
    # 2795
    print('Part 1:', solve_part_1('day2-actual.txt'))

    assert solve_part_2('day2-part2-test.txt') == 2286
    print('Part 2:', solve_part_2('day2-actual.txt'))


if __name__ == '__main__':
    main()
