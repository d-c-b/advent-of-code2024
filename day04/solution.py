from os import path
from collections import defaultdict

HORIZONTALS = [(1, 0), (-1, 0)]
VERTICALS = [(0, 1), (0, -1)]
DIAGONALS = [(1, 1), (-1, -1), (-1, 1), (1, -1)]


ALL_DIRECTIONS = [*HORIZONTALS, *VERTICALS, *DIAGONALS]


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.x_positions = set()
        self.a_positions = set()
        self.grid = defaultdict(str)

        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                self.grid[(i, j)] = char
                if char == "X":
                    self.x_positions.add((i, j))
                elif char == "A":
                    self.a_positions.add((i, j))

    def word_search_at_position(
        self,
        coords: tuple[int, int],
        word_to_find: str,
        directions: list[tuple[int, int]],
        index_in_word: int = 0,
    ) -> int:
        x, y = coords
        return sum(
            [
                1
                for word in [
                    "".join(
                        [
                            self.grid[x + n * dx, y + n * dy]
                            for n in range(
                                -index_in_word, len(word_to_find) - index_in_word
                            )
                        ]
                    )
                    for dx, dy in directions
                ]
                if word == word_to_find
            ]
        )

    def solve_part_1(self) -> int:
        return sum(
            [
                self.word_search_at_position(
                    x_coord, word_to_find="XMAS", directions=ALL_DIRECTIONS
                )
                for x_coord in self.x_positions
            ]
        )

    def solve_part_2(self) -> int:
        return sum(
            [
                self.word_search_at_position(
                    a_coord, word_to_find="MAS", directions=DIAGONALS, index_in_word=1
                )
                == 2
                for a_coord in self.a_positions
            ]
        )


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 04:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
