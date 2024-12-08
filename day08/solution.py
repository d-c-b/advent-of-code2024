from os import path
from collections import defaultdict
from itertools import count
import math


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.X_MAX = len(lines[0])
        self.Y_MAX = len(lines)
        self.frequencies = defaultdict(list)
        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                if char != ".":
                    self.frequencies[char].append((i, j))

    def is_in_bounds(self, coords: tuple[int, int]) -> bool:
        new_x, new_y = coords
        return 0 <= new_x < self.X_MAX and 0 <= new_y < self.Y_MAX

    def solve_part_1(self) -> int:
        antinodes = set()
        for frequency in self.frequencies:
            for x1, y1 in self.frequencies[frequency]:
                for x2, y2 in [
                    antenna_position
                    for antenna_position in self.frequencies[frequency]
                    if antenna_position != (x1, y1)
                ]:
                    dx, dy = (x2 - x1), (y2 - y1)
                    new_x, new_y = (x1 + 2 * dx, y1 + 2 * dy)
                    if self.is_in_bounds((new_x, new_y)):
                        antinodes.add((new_x, new_y))
        return len(antinodes)

    def solve_part_2(self) -> int:
        antinodes = set()
        for frequency in self.frequencies:
            for x1, y1 in self.frequencies[frequency]:
                for x2, y2 in [
                    antenna_position
                    for antenna_position in self.frequencies[frequency]
                    if antenna_position != (x1, y1)
                ]:
                    div = math.gcd(x2 - x1, y2 - y1)
                    dx, dy = (x2 - x1) // div, (y2 - y1) // div
                    for i in count():
                        new_x, new_y = (x1 + (i * dx), y1 + (i * dy))
                        if self.is_in_bounds((new_x, new_y)):
                            antinodes.add((new_x, new_y))
                        else:
                            break

        return len(antinodes)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 08:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
