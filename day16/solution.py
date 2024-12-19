from os import path
import heapq

NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")

        self.grid_positions = dict()
        for j, line in enumerate(input_file.read().strip().splitlines()):
            for i, c in enumerate(line):
                if c == "S":
                    self.start = (i, j)
                    self.grid_positions[(i, j)] = "."
                elif c == "E":
                    self.end = (i, j)
                    self.grid_positions[(i, j)] = "."

                elif c != "#":
                    self.grid_positions[(i, j)] = c
        self.start_direction = 1

    def find_min_distances(
        self, start: tuple[int, int], start_direction: int
    ) -> dict[tuple[tuple[int, int], int], int]:
        distances = {
            (position, d): 10_000_000_000
            for position in self.grid_positions.keys()
            for d in range(4)
        }
        distances[(start, start_direction)] = 0
        to_visit = [(0, start, start_direction)]
        visited = set()
        while to_visit:
            distance, (x, y), direction = heapq.heappop(to_visit)
            if ((x, y), direction) in visited:
                continue
            visited.add(((x, y), direction))

            distances[(x, y), direction] = min(distances[(x, y), direction], distance)

            dx, dy = DIRECTIONS[direction]
            new = x + dx, y + dy
            if new in self.grid_positions:
                heapq.heappush(to_visit, (distance + 1, new, direction))

            for i, (dx, dy) in enumerate(DIRECTIONS):
                if i == direction:
                    continue

                if abs(direction - i) == 2:
                    heapq.heappush(to_visit, (distance + 2000, (x, y), i))

                else:
                    heapq.heappush(to_visit, (distance + 1000, (x, y), i))

        return distances

    def solve_part_1(self) -> int:
        min_distances = self.find_min_distances(self.start, self.start_direction)
        return min(min_distances[(self.end, i)] for i in range(4))

    def solve_part_2(self) -> int:
        min_distances_from_start = self.find_min_distances(
            self.start, self.start_direction
        )
        target_min_to_end = min(
            [min_distances_from_start[(self.end, i)] for i in range(4)]
        )

        min_distances_from_end_for_starting_directions = [
            self.find_min_distances(self.end, d) for d in range(4)
        ]

        on_best_path = set()
        for pos in self.grid_positions.keys():
            for dir in range(4):
                if (
                    min_distances_from_start[pos, dir]
                    + min(
                        min_distances_from_end[pos, (dir + 2) % 4]
                        for min_distances_from_end in min_distances_from_end_for_starting_directions
                    )
                    == target_min_to_end
                ):
                    on_best_path.add(pos)

        return len(on_best_path)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 16:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
