from os import path
from collections import defaultdict


class Solution:
    MOD_NUMBER = 16777216

    def __init__(self, number_of_iterations: int) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.initial_secret_numbers = [
            int(num) for num in input_file.read().strip().splitlines()
        ]
        self.number_of_iterations = number_of_iterations
        self.secret_numbers = {num: [num] for num in self.initial_secret_numbers}

    def find_next_secret_number(self, current_number: int) -> int:
        secret_number = (current_number << 6 ^ current_number) % self.MOD_NUMBER
        secret_number = (secret_number >> 5 ^ secret_number) % self.MOD_NUMBER
        secret_number = (secret_number << 11 ^ secret_number) % self.MOD_NUMBER
        return secret_number

    def solve_part_1(self) -> int:
        for initial in self.initial_secret_numbers:
            secret = self.secret_numbers[initial][-1]
            while len(self.secret_numbers[initial]) < self.number_of_iterations + 1:
                secret = self.find_next_secret_number(secret)
                self.secret_numbers[initial].append(secret)

        return sum(
            [
                self.secret_numbers[initial][-1]
                for initial in self.initial_secret_numbers
            ]
        )

    def solve_part_2(self) -> int:
        scores: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
        for initial in self.initial_secret_numbers:
            secret = self.secret_numbers[initial][-1]
            while len(self.secret_numbers[initial]) < self.number_of_iterations + 1:
                secret = self.find_next_secret_number(secret)
                self.secret_numbers[initial].append(secret)

            prices = [secret_num % 10 for secret_num in self.secret_numbers[initial]]
            changes = [
                next_price - current_price
                for current_price, next_price in zip(prices, prices[1:])
            ]

            current_buyer = dict()
            for i in range(len(changes) - 4):
                change_sequence = (
                    changes[i],
                    changes[i + 1],
                    changes[i + 2],
                    changes[i + 3],
                )
                if change_sequence not in current_buyer:
                    current_buyer[change_sequence] = prices[i + 4]

            for sequence, price in current_buyer.items():
                scores[sequence] += price
        return max(s for s in scores.values())


if __name__ == "__main__":
    s = Solution(2000)
    print(
        f"""
        Day 22:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
