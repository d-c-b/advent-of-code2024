from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        towels, patterns = input_file.read().strip().split("\n\n")
        self.towels = towels.split(", ")
        self.patterns = patterns.splitlines()
        self.arrangements_cache: dict[str, int] = dict()

    def arrangements(self, pattern: str) -> int:
        if pattern == "":
            return 1
        if pattern in self.arrangements_cache:
            return self.arrangements_cache[pattern]

        possible = 0
        for towel in self.towels:
            if pattern.startswith(towel):
                arrangement_count = self.arrangements(pattern[len(towel) :])
                self.arrangements_cache[pattern[len(towel) :]] = arrangement_count
                possible += arrangement_count

        return possible

    def solve_part_1(self) -> int:
        return sum([1 for pattern in self.patterns if self.arrangements(pattern)])

    def solve_part_2(self) -> int:
        return sum([self.arrangements(pattern) for pattern in self.patterns])


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 19:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
