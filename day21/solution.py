from os import path
from functools import cache


DIRECTIONS = {
    "<": (1, 0),
    ">": (-1, 0),
    "v": (0, -1),
    "^": (0, 1),
}


class DirectionalKeyPad:
    def __init__(self):
        self.keypad = {
            "A": (0, 0),
            "^": (1, 0),
            ">": (0, -1),
            "v": (1, -1),
            "<": (2, -1),
        }
        self.forbidden = ((2, 0),)

    def get_paths(self, from_key: str, to_key: str) -> set[str]:
        if from_key == to_key:
            return set()
        from_pos, to_pos = (
            self.keypad[from_key],
            self.keypad[to_key],
        )
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        horizontal_key = "<" if from_x < to_x else ">"
        vertical_key = "^" if from_y < to_y else "v"

        horizontals = horizontal_key * abs(from_x - to_x)
        verticals = vertical_key * abs(from_y - to_y)

        paths = []
        for possible in [f"{horizontals}{verticals}", f"{verticals}{horizontals}"]:
            allowed = True
            x, y = from_pos
            for char in possible:
                dx, dy = DIRECTIONS[char]
                x += dx
                y += dy
                if (x, y) in self.forbidden:
                    allowed = False
                    break

            if allowed:
                paths.append(possible)

        return set(paths)


class DoorKeyPad(DirectionalKeyPad):
    def __init__(self):
        self.keypad = {
            "A": (0, 0),
            "0": (1, 0),
            "1": (2, 1),
            "2": (1, 1),
            "3": (0, 1),
            "4": (2, 2),
            "5": (1, 2),
            "6": (0, 2),
            "7": (2, 3),
            "8": (1, 3),
            "9": (0, 3),
        }
        self.forbidden = ((2, 0),)


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.codes = input_file.read().strip().splitlines()
        self.door_keypad = DoorKeyPad()
        self.directional_keypad = DirectionalKeyPad()

    @cache
    def find_min_key_presses(
        self, start_key: str, target_key: str, number_of_robots: int, keypad_number: int
    ) -> int:
        keypad = self.door_keypad if keypad_number == 0 else self.directional_keypad
        sequences = keypad.get_paths(start_key, target_key)
        if not sequences:
            return 1

        if keypad_number == number_of_robots:
            return min(len(option) for option in sequences) + 1

        possible = []
        for sequence in sequences:
            count = 0
            for start, end in zip(f"A{sequence}", f"{sequence}A"):
                count += self.find_min_key_presses(
                    start, end, number_of_robots, keypad_number + 1
                )
            possible.append(count)
        return min(possible)

    def solve_for_complexity(self, number_of_robots: int) -> int:
        complexity_all_codes = 0
        for code in self.codes:
            shortest_sequence = 0
            for current_key, next_key in zip(f"A{code}", code):
                shortest_sequence += self.find_min_key_presses(
                    current_key, next_key, number_of_robots, 0
                )
            complexity_all_codes += shortest_sequence * int(code.replace("A", ""))

        return complexity_all_codes

    def solve_part_1(self) -> int:
        return self.solve_for_complexity(2)

    def solve_part_2(self) -> int:
        return self.solve_for_complexity(25)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 21:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
