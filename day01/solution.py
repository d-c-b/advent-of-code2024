from os import path
from collections import Counter


class Solution:
    def __init__(self) -> None:
        self.left = []
        self.right = []
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        for line in input_file.read().strip().splitlines():
            left, right = [int(x) for x in line.split()]
            self.left.append(left)
            self.right.append(right)

    def solve_part_1(self) -> int:
        sorted_left = sorted(self.left)
        sorted_right = sorted(self.right)
        return sum([abs(x - y) for x, y in zip(sorted_left, sorted_right)])

    def solve_part_2(self) -> int:
        right_counts = Counter(self.right)
        return sum([val * right_counts.get(val, 0) for val in self.left])


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 01:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
