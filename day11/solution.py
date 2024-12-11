from os import path
from collections import defaultdict


class Solution:
    def __init__(self) -> None:
        self.blink_count = 0
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.stone_counts: defaultdict[int, int] = defaultdict(int)
        for stone in [int(stone) for stone in input_file.read().strip().split()]:
            self.stone_counts[stone] += 1

    def blink(self) -> None:
        updated_stone_counts: defaultdict[int, int] = defaultdict(int)
        for number, occurrences in self.stone_counts.items():
            if number == 0:
                updated_stone_counts[1] += occurrences

            elif len(str(number)) % 2 == 0:
                split_point = len(str(number)) // 2
                updated_stone_counts[int(str(number)[:split_point])] += occurrences
                updated_stone_counts[int(str(number)[split_point:])] += occurrences

            else:
                updated_stone_counts[2024 * number] += occurrences

        self.stone_counts = updated_stone_counts
        self.blink_count += 1

    def solve_part_1(self) -> int:
        while self.blink_count < 25:
            self.blink()
        return sum([occurrences for occurrences in self.stone_counts.values()])

    def solve_part_2(self) -> int:
        while self.blink_count < 75:
            self.blink()
        return sum([occurrences for occurrences in self.stone_counts.values()])


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 11:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
