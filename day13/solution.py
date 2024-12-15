from os import path
import re


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        machines = input_file.read().strip().split("\n\n")
        self.machine_configs = []
        for machine in machines:
            a, b, prize = machine.splitlines()
            ax, ay = [int(x) for x in re.findall(r"\d+", a)]
            bx, by = [int(x) for x in re.findall(r"\d+", b)]
            px, py = [int(x) for x in re.findall(r"\d+", prize)]
            self.machine_configs.append(((ax, ay), (bx, by), (px, py)))

    def solve_equation(
        self,
        a_button_movement: tuple[int, int],
        b_button_movement: tuple[int, int],
        target_vals: tuple[int, int],
    ) -> tuple[int, int] | None:
        (ax, ay), (bx, by), (target_x, target_y) = (
            a_button_movement,
            b_button_movement,
            target_vals,
        )
        determinant = ax * by - ay * bx
        if determinant == 0:
            return None

        if (by * target_x - bx * target_y) % determinant == 0 and (
            -ay * target_x + ax * target_y
        ) % determinant == 0:
            a_presses = (by * target_x - bx * target_y) // determinant
            b_presses = (-ay * target_x + ax * target_y) // determinant
            return a_presses, b_presses
        return None

    def solve(self, increase_target_by: int = 0) -> int:
        tokens_needed = 0

        for a_button_movement, b_button_movement, target_vals in self.machine_configs:
            target_x, target_y = target_vals
            target_x, target_y = (
                target_x + increase_target_by,
                target_y + increase_target_by,
            )

            a_b_button_presses = self.solve_equation(
                a_button_movement, b_button_movement, (target_x, target_y)
            )
            if a_b_button_presses:
                a_presses, b_presses = a_b_button_presses
                tokens_needed += (3 * a_presses) + b_presses

        return tokens_needed

    def solve_part_1(self) -> int:
        return self.solve()

    def solve_part_2(self) -> int:
        return self.solve(increase_target_by=10_000_000_000_000)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 13:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
