from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = [line.split() for line in input_file.read().strip().splitlines()]
        self.reports = [[int(x) for x in levels] for levels in lines]

    def diffs_for_report(self, report: list[int]) -> list[int]:
        return [x - y for x, y in zip(report, report[1:])]

    def report_is_valid(self, report: list[int]) -> bool:
        diffs = self.diffs_for_report(report)
        if (
            all([diff == abs(diff) for diff in diffs])
            or all([diff == abs(diff) * -1 for diff in diffs])
        ) and all([1 <= abs(diff) <= 3 for diff in diffs]):
            return True
        return False

    def check_valid_with_removed_level(
        self, report: list[int], indices_to_remove: list[int]
    ):
        for i in indices_to_remove:
            dampened_report = [*report[:i], *report[i + 1 :]]
            if self.report_is_valid(dampened_report):
                return True
        return False

    def solve_part_1(self) -> int:
        total = 0
        for report in self.reports:
            if self.report_is_valid(report):
                total += 1
        return total

    def solve_part_2(self) -> int:
        total = 0
        for report in self.reports:
            if self.report_is_valid(report):
                total += 1

            else:
                if self.check_valid_with_removed_level(
                    report, list(range(len(report)))
                ):
                    total += 1
        return total


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 02:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
