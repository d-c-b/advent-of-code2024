from os import path
import re
import math


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.input_string = input_file.read().replace("\n", "")

    def sum_valid_multiplications_for_string(self, input_string: str) -> int:
        valid_multiplications = re.findall(r"mul\(\d{1,3},\d{1,3}\)", input_string)
        return sum(
            [
                math.prod([int(num) for num in re.findall(r"\d+", multiplication)])
                for multiplication in valid_multiplications
            ]
        )

    def solve_part_1(self) -> int:
        return self.sum_valid_multiplications_for_string(self.input_string)

    def solve_part_2(self) -> int:
        enabled_string = "".join(
            re.split(r"don\'t\(\).*?(do\(\)|$)", self.input_string)
        )
        return self.sum_valid_multiplications_for_string(enabled_string)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 03:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
