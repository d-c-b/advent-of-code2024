from os import path
import math
import re


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = [line.split() for line in input_file.read().strip().splitlines()]
        self.X_MAX, self.Y_MAX = 100, 102
        robots: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for line in lines:
            position, velocity = line
            px, py = [int(x) for x in re.findall(r"-?\d+", position)]
            vx, vy = [int(x) for x in re.findall(r"-?\d+", velocity)]
            robots.append(((px, py), (vx, vy)))

        self.robots = tuple(robots)
        self.seen_states: dict[
            tuple[tuple[tuple[int, int], tuple[int, int]], ...], int
        ] = dict()

    def increment_time(self, time: int) -> None:
        updated_robots = []
        for (px, py), (vx, vy) in self.robots:
            updated_px, updated_py = (px + vx * time) % (self.X_MAX + 1), (
                py + vy * time
            ) % (self.Y_MAX + 1)
            updated_robots.append(((updated_px, updated_py), (vx, vy)))

        self.robots = tuple(updated_robots)

    def get_number_or_robots_per_quadrant(self) -> list[int]:
        quadrant_x_y_ranges = [
            (range(0, self.X_MAX // 2), range(0, self.Y_MAX // 2)),
            (range(0, self.X_MAX // 2), range((self.Y_MAX // 2) + 1, self.Y_MAX + 1)),
            (range((self.X_MAX // 2) + 1, self.X_MAX + 1), range(0, self.Y_MAX // 2)),
            (
                range((self.X_MAX // 2) + 1, self.X_MAX + 1),
                range((self.Y_MAX // 2) + 1, self.Y_MAX + 1),
            ),
        ]

        return [
            len(
                [
                    position
                    for position, _ in self.robots
                    for x in x_vals
                    for y in y_vals
                    if position == (x, y)
                ]
            )
            for x_vals, y_vals in quadrant_x_y_ranges
        ]

    def solve_part_1(self) -> int:
        self.increment_time(100)
        num_per_q = self.get_number_or_robots_per_quadrant()
        return math.prod(num_per_q)

    def solve_part_2(self) -> int:
        t = 0
        while self.robots not in self.seen_states:
            self.seen_states[self.robots] = t
            self.increment_time(1)
            t += 1

        for state, time in self.seen_states.items():
            positions = set([position for position, _ in state])
            if len(positions) == len(state):
                return time

        return -1


if __name__ == "__main__":
    print(
        f"""
        Day 14:
        Part 1 Solution: {Solution().solve_part_1()}
        Part 2 Solution: {Solution().solve_part_2()}
        """
    )
