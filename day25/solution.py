from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.keys = []
        self.locks = []
        keys_and_locks = input_file.read().strip().split("\n\n")
        for key_lock in keys_and_locks:
            lines = key_lock.splitlines()
            code = [
                len([lines[i][j] for i in range(len(lines)) if lines[i][j] == "#"]) - 1
                for j in range(len(lines[0]))
            ]

            if all(c == "#" for c in lines[0]):
                self.locks.append(tuple(code))

            else:
                self.keys.append(tuple(code))

    def solve_part_1(self) -> int:
        no_overlaps = set(
            [
                (lock, key)
                for key in self.keys
                for lock in self.locks
                if all(l + k <= 5 for l, k in zip(lock, key))
            ]
        )
        return len(no_overlaps)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 25:
        Part 1 Solution: {s.solve_part_1()}
        """
    )
