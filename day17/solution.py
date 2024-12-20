from os import path
import re
from collections import deque


class Computer:
    CODE_MAP = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]

    def __init__(self, A: int, B: int, C: int, program: list[int]) -> None:
        self.A, self.B, self.C = A, B, C
        self.program = program
        self.instruction_pointer = 0
        self.outputs: list[int] = []

    def combo(self, operand) -> int:
        combo_vals = {4: self.A, 5: self.B, 6: self.C}
        return combo_vals.get(operand, operand)

    def adv(self, operand) -> None:
        self.A = self.A // (2 ** self.combo(operand))

    def bxl(self, operand) -> None:
        self.B = self.B ^ operand

    def bst(self, operand) -> None:
        self.B = self.combo(operand) % 8

    def jnz(self, operand) -> None:
        if self.A:
            self.instruction_pointer = operand - 2

    def bxc(self, _) -> None:
        self.B = self.B ^ self.C

    def out(self, operand) -> None:
        self.outputs.append(self.combo(operand) % 8)

    def bdv(self, operand) -> None:
        self.B = self.A // (2 ** self.combo(operand))
        self.instruction_pointer += 2

    def cdv(self, operand) -> None:
        self.C = self.A // (2 ** self.combo(operand))

    def execute_instruction(self, opcode: int, operand: int) -> None:
        function_name = self.CODE_MAP[opcode]
        getattr(self, function_name)(operand)

    def run(self) -> list[int]:
        while self.instruction_pointer < len(self.program):
            opcode = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer + 1]
            self.execute_instruction(opcode, operand)
            self.instruction_pointer += 2

        return self.outputs


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        registers, program = input_file.read().strip().split("\n\n")
        register_values = []
        for r in registers.splitlines():
            value = re.search(r"-?\d+", r)
            if not value:
                raise Exception(r"No register initial value found: {r}")
            register_values.append(int(value.group()))
        self.A, self.B, self.C = register_values
        self.program = [int(x) for x in re.findall(r"-?\d+", program)]
        self.instruction_pointer = 0

    def solve_part_1(self) -> str:
        c = Computer(A=self.A, B=self.B, C=self.C, program=self.program)
        output = c.run()
        return ",".join([str(a) for a in output])

    def solve_part_2(self) -> int:
        possible = deque([[0]])
        while possible:
            octal_digits = possible.popleft()
            a = sum([8 ** (i + 1) * v for i, v in enumerate(reversed(octal_digits))])
            for i in range(8):
                new_a = a + i
                computer = Computer(A=new_a, B=self.B, C=self.C, program=self.program)
                computer.run()
                if computer.outputs == self.program:
                    return new_a

                if (
                    computer.outputs
                    == self.program[len(self.program) - len(computer.outputs) :]
                ):
                    possible.append(
                        [
                            *octal_digits,
                            i,
                        ]
                    )

        return 0


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 17:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
