from os import path
import heapq
from collections import deque


DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.grid_positions = set()
        self.wall_positions = set()
        for j, line in enumerate(input_file.read().strip().splitlines()):
            for i, c in enumerate(line):
                if c == "S":
                    self.start = (i, j)
                    self.grid_positions.add((i, j))
                elif c == "E":
                    self.end = (i, j)
                    self.grid_positions.add((i, j))

                elif c != "#":
                    self.grid_positions.add((i, j))

                else:
                    self.wall_positions.add((i, j))
        self.start_direction = 1

    def manhatten_distance(self, p1: tuple[int, int], p2: tuple[int, int]) -> int:
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def find_possible_cheat_paths(
        self, max_cheat_length: int
    ) -> set[tuple[tuple[int, int], tuple[int, int], int]]:
        possible_cheat_paths = set()
        for i, j in self.grid_positions:
            queue = deque([(i, j)])
            seen = set()
            while queue:
                x, y = queue.popleft()
                if (x, y) in seen:
                    continue
                seen.add((x, y))
                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if self.manhatten_distance((i, j), (nx, ny)) <= max_cheat_length:
                        if (nx, ny) in self.grid_positions:
                            possible_cheat_paths.add(
                                (
                                    (i, j),
                                    (nx, ny),
                                    self.manhatten_distance((i, j), (nx, ny)),
                                )
                            )
                        queue.append((nx, ny))
        return possible_cheat_paths

    def find_min_times(
        self,
    ) -> dict[tuple[int, int], int]:
        times = {position: 10_000_000_000 for position in self.grid_positions}
        times[(self.start)] = 0
        to_visit = [(0, self.start)]
        visited = set()
        while to_visit:
            time, (x, y) = heapq.heappop(to_visit)
            if (x, y) in visited:
                continue
            visited.add(((x, y)))
            times[(x, y)] = min(times[(x, y)], time)
            for dx, dy in DIRECTIONS:
                new = x + dx, y + dy
                if new in self.grid_positions:
                    heapq.heappush(to_visit, (time + 1, new))
        return times

    def solve(self, cheat_length: int, min_time_save: int) -> int:
        min_times_no_cheat = self.find_min_times()
        good_cheats = set()
        possible_cheat_positions = self.find_possible_cheat_paths(cheat_length)
        for cheat_s, cheat_e, time in possible_cheat_positions:
            time_saved = min_times_no_cheat[cheat_e] - (
                min_times_no_cheat[cheat_s] + time
            )
            if time_saved >= min_time_save:
                good_cheats.add((cheat_s, cheat_e))

        return len(good_cheats)

    def solve_part_1(self) -> int:
        return self.solve(2, 100)

    def solve_part_2(self) -> int:
        return self.solve(20, 100)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 20:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
