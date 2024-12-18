from os import path
from collections import deque

DIRECTION_MAP = {
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, 1),
    "^": (0, -1),
}


class Grid:
    def __init__(self, double_size: bool = False) -> None:
        self.double_size = double_size
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        grid, directions = input_file.read().strip().split("\n\n")
        self.directions = "".join([line for line in directions.splitlines()])
        self.grid_positions = dict()
        for j, line in enumerate(grid.splitlines()):
            for i, c in enumerate(line):
                if c == "#":
                    if double_size:
                        self.grid_positions[(i * 2, j)] = c
                        self.grid_positions[(i * 2 + 1, j)] = c
                    else:
                        self.grid_positions[(i, j)] = c

                elif c == "@":
                    if double_size:
                        self.robot_position = (i * 2, j)
                        self.grid_positions[(i * 2, j)] = "."
                        self.grid_positions[(i * 2 + 1, j)] = "."
                    else:
                        self.robot_position = (i, j)
                        self.grid_positions[(i, j)] = "."
                elif c == "O":
                    if double_size:
                        self.grid_positions[(i * 2, j)] = "["
                        self.grid_positions[(i * 2 + 1, j)] = "]"

                    else:
                        self.grid_positions[(i, j)] = c
                else:
                    if double_size:
                        self.grid_positions[(i * 2, j)] = c
                        self.grid_positions[(i * 2 + 1, j)] = c

                    else:
                        self.grid_positions[(i, j)] = c

    def move(self, direction: str) -> None:
        dx, dy = DIRECTION_MAP[direction]
        px, py = self.robot_position
        to_move = []
        positions_to_check = deque([(px, py)])

        while positions_to_check:
            px, py = positions_to_check.popleft()
            next_x, next_y = px + dx, py + dy

            if self.grid_positions[(next_x, next_y)] == "#":
                return None

            elif self.grid_positions[(next_x, next_y)] == ".":
                to_move.append((px, py))

            else:
                if not self.double_size or direction in "<>":
                    to_move.append((px, py))
                    positions_to_check.append((next_x, next_y))

                else:
                    if self.grid_positions[(next_x, next_y)] == "[":
                        positions_to_check.extend(
                            ((next_x, next_y), (next_x + 1, next_y))
                        )
                        to_move.extend(((next_x, next_y), (next_x + 1, next_y)))

                    elif self.grid_positions[(next_x, next_y)] == "]":
                        positions_to_check.extend(
                            ((next_x, next_y), (next_x - 1, next_y))
                        )
                        to_move.extend(((next_x, next_y), (next_x - 1, next_y)))

        moved = set()

        for x, y in reversed(to_move):
            if (x, y) in moved:
                continue
            self.grid_positions[(x + dx, y + dy)] = self.grid_positions[(x, y)]
            self.grid_positions[(x, y)] = "."
            moved.add((x, y))

        cur_x, cur_y = self.robot_position
        self.robot_position = cur_x + dx, cur_y + dy


def solve_part_1() -> int:
    grid = Grid()
    for direction in grid.directions:
        grid.move(direction)

    return sum(
        [
            (100 * y) + x
            for x, y in grid.grid_positions
            if grid.grid_positions[(x, y)] == "O"
        ]
    )


def solve_part_2() -> int:
    grid = Grid(double_size=True)
    for direction in grid.directions:
        grid.move(direction)

    return sum(
        [
            (100 * y) + x
            for x, y in grid.grid_positions
            if grid.grid_positions[(x, y)] == "["
        ]
    )


if __name__ == "__main__":
    print(
        f"""
        Day 15:
        Part 1 Solution: {solve_part_1()}
        Part 2 Solution: {solve_part_2()}
        """
    )
