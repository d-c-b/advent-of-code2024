from os import path
from collections import deque
from typing import Callable


MULTIPLY_OPERATOR = lambda a, b: a * b
ADD_OPERATOR = lambda a, b: a + b
CONCAT_OPERATOR = lambda a, b: int(str(a) + str(b))


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.equations = []
        for line in lines:
            target, nums = line.split(":")
            equation = int(target), [int(num) for num in nums.split()]
            self.equations.append(equation)

    def solve(self, operators: list[Callable[[int, int], int]]) -> int:
        valid_lines = set()
        for i, (target, nums) in enumerate(self.equations):
            first, second, *rest = nums
            queue = deque([(operator(first, second), rest) for operator in operators])
            while queue:
                current, remaining = queue.pop()
                if current == target and len(remaining) == 0:
                    valid_lines.add(i)
                    break

                elif current <= target and len(remaining) > 0:
                    next_val, *remaining_vals = remaining
                    for operator in operators:
                        queue.append((operator(current, next_val), remaining_vals))

        return sum(
            [
                target
                for i, (target, _) in enumerate(self.equations)
                if i in valid_lines
            ]
        )

    def solve_part_1(self) -> int:
        return self.solve([MULTIPLY_OPERATOR, ADD_OPERATOR])

    def solve_part_2(self) -> int:
        return self.solve([MULTIPLY_OPERATOR, ADD_OPERATOR, CONCAT_OPERATOR])


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 07:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
