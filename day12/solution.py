from os import path
from collections import deque


RIGHT, LEFT, DOWN, UP = (1, 0), (-1, 0), (0, 1), (0, -1)

DIRECTIONS = [RIGHT, LEFT, DOWN, UP]

CORNER_PAIRS = [
    ([RIGHT, UP], (1, -1)),
    ([RIGHT, DOWN], (1, 1)),
    ([LEFT, UP], (-1, -1)),
    ([LEFT, DOWN], (-1, 1)),
]


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.grid: dict[tuple[int, int], str] = dict()

        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                self.grid[(i, j)] = char

    def find_regions(self) -> list[set[tuple[int, int]]]:
        seen = set()
        regions = []
        for pos in self.grid:
            if pos in seen:
                continue
            current_region = set([pos])
            seen.add(pos)
            to_visit = deque([pos])
            while to_visit:
                x, y = to_visit.pop()
                adjacent_points = [(x + dx, y + dy) for dx, dy in DIRECTIONS]
                for adjacent in adjacent_points:
                    if adjacent in self.grid and self.grid[adjacent] == self.grid[pos]:
                        current_region.add(adjacent)
                        if adjacent not in seen:
                            to_visit.append(adjacent)
                        seen.add(adjacent)

            regions.append(current_region)

        return regions

    def calculate_perimeter(self, region: set[tuple[int, int]]) -> int:
        perimeter = 0
        for x, y in region:
            perimeter += len(
                [
                    (x + dx, y + dy)
                    for dx, dy in DIRECTIONS
                    if (x + dx, y + dy) not in region
                ]
            )
        return perimeter

    def calculate_number_of_sides(self, region: set[tuple[int, int]]) -> int:
        number_of_sides = 0
        for point in region:
            x, y = point

            for corner_directions, (diag_x, diag_y) in CORNER_PAIRS:
                if not any(
                    [(x + dx, y + dy) in region for dx, dy in corner_directions]
                ):
                    number_of_sides += 1

                elif all([(x + dx, y + dy) in region for dx, dy in corner_directions]):
                    if (x + diag_x, y + diag_y) not in region:
                        number_of_sides += 1
        return number_of_sides

    def solve_part_1(self) -> int:
        regions = self.find_regions()
        perimeters = [self.calculate_perimeter(region) for region in regions]
        return sum(
            len(region) * perimeter for region, perimeter in zip(regions, perimeters)
        )

    def solve_part_2(self) -> int:
        regions = self.find_regions()
        sides = [self.calculate_number_of_sides(region) for region in regions]
        return sum(
            len(region) * number_of_sides
            for region, number_of_sides in zip(regions, sides)
        )


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 12:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
