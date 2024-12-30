from os import path
from collections import defaultdict, deque


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.computers: set[str] = set()
        self.connections = defaultdict(set)
        lines = input_file.read().strip().splitlines()
        for line in lines:
            comp1, comp2 = line.split("-")
            self.computers.update((comp1, comp2))
            self.connections[comp1].add(comp2)
            self.connections[comp2].add(comp1)

    def solve_part_1(self) -> int:
        t_computers = [comp for comp in self.computers if comp.startswith("t")]
        connected_three_with_t_computer = set()
        for t_computer in t_computers:
            for connected in self.connections[t_computer]:
                mutual_connections = self.connections[t_computer].intersection(
                    self.connections[connected]
                )
                for mutual in mutual_connections:
                    connected_three_with_t_computer.add(
                        tuple(sorted((t_computer, connected, mutual)))
                    )
        return len(connected_three_with_t_computer)

    def solve_part_2(self) -> str:
        max_cliques_for_each_comp = []
        seen = set()
        for comp in self.computers:
            max_clique_for_comp = [comp]
            queue = deque([[comp]])
            while queue:
                clique_candidate = queue.pop()
                if tuple(sorted(clique_candidate)) in seen:
                    continue
                seen.add(tuple(sorted(clique_candidate)))
                max_clique_for_comp = max(
                    max_clique_for_comp, clique_candidate, key=len
                )
                for neighbour in self.connections[comp]:
                    if neighbour not in clique_candidate and set(
                        clique_candidate
                    ).issubset(self.connections[neighbour]):
                        queue.append([*clique_candidate, neighbour])
            max_cliques_for_each_comp.append(sorted(max_clique_for_comp))

        max_clique = max(max_cliques_for_each_comp, key=len)
        return ",".join(max_clique)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 23:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
