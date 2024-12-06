from os import path
from functools import cmp_to_key


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        rules, updates = input_file.read().strip().split("\n\n")
        self.rules = [
            tuple(int(x) for x in rule.split("|")) for rule in rules.splitlines()
        ]
        self.updates = [
            [int(x) for x in update.split(",")] for update in updates.splitlines()
        ]

    def all_rules_followed(self, update: list[int]) -> bool:
        update_dict = {update: i for i, update in enumerate(update)}
        for lt, gt in self.rules:
            if lt in update_dict and gt in update_dict:
                if update_dict[lt] > update_dict[gt]:
                    return False
        return True

    def get_middle_value_of_list(self, int_list: list[int]) -> int:
        return int_list[(len(int_list) - 1) // 2]

    def valid_ordering_comparator(self, a: int, b: int) -> int:
        if (b, a) in self.rules:
            return -1
        return 1

    def solve_part_1(self) -> int:
        correctly_ordered = [
            update for update in self.updates if self.all_rules_followed(update)
        ]
        return sum(
            [self.get_middle_value_of_list(update) for update in correctly_ordered]
        )

    def solve_part_2(self) -> int:
        incorrectly_ordered = [
            update for update in self.updates if not self.all_rules_followed(update)
        ]
        fixed_orders = [
            sorted(update, key=cmp_to_key(self.valid_ordering_comparator))
            for update in incorrectly_ordered
        ]
        return sum([self.get_middle_value_of_list(update) for update in fixed_orders])


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 05:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
