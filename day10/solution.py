from os import path
from collections import deque


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.grid: dict[tuple[int, int], int] = dict()
        self.TRAIL_LENGTH = 10
        self.end_positions: list[tuple[int, int]] = []
        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                self.grid[(i, j)] = int(char)
                if int(char) == 9:
                    self.end_positions.append((i, j))

    def find_valid_trails(self) -> set[tuple[tuple[int, int], ...]]:
        valid_trails = set()
        possible_trails: deque[tuple[tuple[int, int], ...]] = deque(
            [(end_pos,) for end_pos in self.end_positions]
        )
        while possible_trails:
            lowest_trail_point, *rest = possible_trails.popleft()
            x, y = lowest_trail_point
            for dx, dy in DIRECTIONS:
                new_coords = x + dx, y + dy
                if (
                    new_coords in self.grid
                    and self.grid[lowest_trail_point] - self.grid[new_coords] == 1
                ):
                    updated_possible_trail = (new_coords, lowest_trail_point, *rest)
                    if len(updated_possible_trail) == self.TRAIL_LENGTH:
                        valid_trails.add(updated_possible_trail)

                    else:
                        possible_trails.append(updated_possible_trail)

        return valid_trails

    def solve_part_1(self) -> int:
        valid_trails = self.find_valid_trails()
        return len(set([(start, end) for start, *_, end in valid_trails]))

    def solve_part_2(self) -> int:
        valid_trails = self.find_valid_trails()
        return len(valid_trails)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 10:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
