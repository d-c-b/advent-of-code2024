from os import path
import heapq


DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.byte_positions = [
            tuple([int(x) for x in line.split(",")]) for line in lines
        ]
        self.X_MAX, self.Y_MAX = 70, 70
        self.start = (0, 0)

    def find_min_distance(self, bytes_fallen: int) -> int:
        distances = {
            position: 10_000_000_000
            for position in (
                (x, y) for y in range(self.Y_MAX + 1) for x in range(self.X_MAX + 1)
            )
        }
        distances[self.start] = 0
        corrupted_positions = set(self.byte_positions[:bytes_fallen])
        visited = set()
        to_visit = [(0, self.start)]
        while to_visit:
            distance, (x, y) = heapq.heappop(to_visit)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            distances[(x, y)] = min(distances[(x, y)], distance)

            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (
                    (0 <= nx <= self.X_MAX)
                    and (0 <= ny <= self.Y_MAX)
                    and (nx, ny) not in corrupted_positions
                ):
                    heapq.heappush(to_visit, (distance + 1, (nx, ny)))

        return distances[(self.X_MAX, self.Y_MAX)]

    def solve_part_1(self) -> int:
        return self.find_min_distance(1024)

    def solve_part_2(self) -> str:
        left_index, right_index = 0, len(self.byte_positions) - 1

        while right_index - left_index > 1:
            midpoint = left_index + (right_index - left_index) // 2
            if self.find_min_distance(midpoint) < 10_000_000_000:
                left_index = midpoint
            else:
                right_index = midpoint

        return ",".join(str(x) for x in self.byte_positions[right_index - 1])


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 18:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
