from os import path
from collections import defaultdict


class Grid:
    DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, new_obstruction_position: tuple[int, int] | None = None) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.positions = defaultdict(str)
        self.direction = 0
        self.visited = set()
        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                if char == "^":
                    self.current_position = (i, j)
                    self.visited.add(((i, j), self.direction))
                    char = "."
                self.positions[i, j] = (
                    "#" if (i, j) == new_obstruction_position else char
                )

    def get_next_position(self) -> tuple[int, int]:
        x, y, dx, dy = *self.current_position, *self.DIRECTIONS[self.direction]
        return (x + dx, y + dy)

    def move(self) -> None:
        new_position = self.get_next_position()
        if self.positions[new_position] == "#":
            self.direction = (self.direction + 1) % len(self.DIRECTIONS)

        else:
            if self.positions[new_position] == ".":
                self.visited.add((new_position, self.direction))
            self.current_position = new_position

    def has_cycle(self) -> bool:
        while self.positions[self.current_position]:
            self.move()
            new_position = self.get_next_position()
            if (new_position, self.direction) in self.visited:
                return True
        return False

    def find_visited_positions(self) -> set[tuple[int, int]]:
        while self.positions[self.current_position]:
            self.move()
        return set([position for position, _ in self.visited])


if __name__ == "__main__":
    grid = Grid()
    visited_positions = grid.find_visited_positions()

    print(
        f"""
        Day 06:
        Part 1 Solution: {len(visited_positions)}
        Part 2 Solution: {len([pos for pos in visited_positions if Grid(new_obstruction_position=pos).has_cycle()])}
        """
    )
