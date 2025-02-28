from os import path
import re
from collections import deque
from dataclasses import dataclass


@dataclass
class Gate:
    operator: str
    input_wires: list[str]


class Circuit:

    OPERATORS = {
        "XOR": lambda a, b: a ^ b,
        "OR": lambda a, b: a | b,
        "AND": lambda a, b: a & b,
    }

    def __init__(
        self,
        x_vals: dict[str, int],
        y_vals: dict[str, int],
        gates: dict[str, Gate],
    ) -> None:
        self.wire_outputs = dict(**x_vals, **y_vals)
        self.gates = gates
        self.gate_reference = dict()
        self.NUMBER_OF_BITS = len(x_vals)

        for wire, gate in self.gates.items():
            if set(inp[0] for inp in gate.input_wires) == set(["x", "y"]):
                string_bit_num = gate.input_wires[0][1:]
                self.gate_reference[wire] = f"{gate.operator}{string_bit_num}"

    def swap_gates(self, g1: str, g2: str) -> None:
        self.gates[g1], self.gates[g2] = (
            self.gates[g2],
            self.gates[g1],
        )

    def find_gate_swaps(self) -> set[str]:
        broken = set()
        i = 0
        while i < self.NUMBER_OF_BITS:
            current_xor = self.find_gate("XOR", (f"x{i:02}", f"y{i:02}"))
            current_and = self.find_gate("AND", (f"x{i:02}", f"y{i:02}"))
            assert current_xor and current_and
            if i == 0:
                self.gate_reference["z00"] = current_xor
                self.gate_reference["c00"] = current_and
                i += 1

            else:
                carry_in = self.gate_reference[f"c{i-1:02}"]
                prev_carry = self.find_gate("AND", (current_xor, carry_in))
                if prev_carry:
                    self.gate_reference[f"pc{i:02}"] = prev_carry

                carry_out = self.find_gate(
                    "OR", (current_and, self.gate_reference.get(f"pc{i:02}"))
                )
                if carry_out:
                    self.gate_reference[f"c{i:02}"] = carry_out

                current_z = self.find_gate(
                    "XOR", (current_xor, self.gate_reference.get(f"c{i-1:02}"))
                )

                if current_z is None:
                    to_swap = set(
                        self.gates[f"z{i:02}"].input_wires
                    ).symmetric_difference(
                        [self.gate_reference[f"c{i-1:02}"], current_xor]
                    )
                    self.swap_gates(*to_swap)
                    broken.update(to_swap)
                    continue

                elif current_z != f"z{i:02}":
                    to_swap = set([current_z, f"z{i:02}"])
                    broken.update(to_swap)
                    self.swap_gates(*to_swap)
                    continue
                self.gate_reference[f"z{i:02}"] = current_z
                i += 1

        return broken

    def find_gate(
        self, operator: str, input_gates: tuple[str | None, str | None]
    ) -> str | None:
        for wire, gate in self.gates.items():
            if set(gate.input_wires) == set(input_gates) and gate.operator == operator:
                return wire
        return None

    def solve_unknown_wires(self) -> None:
        unknown_wires = set(self.gates.keys()).difference(self.wire_outputs.keys())

        wires_to_calculate = [
            unknown_wire
            for unknown_wire in unknown_wires
            if all(
                wire in self.wire_outputs
                for wire in self.gates[unknown_wire].input_wires
            )
        ]
        queue = deque(wires_to_calculate)

        while queue:
            wire = queue.popleft()
            gate = self.gates[wire]
            a, b = gate.input_wires
            self.wire_outputs[wire] = self.OPERATORS[gate.operator](
                self.wire_outputs[a], self.wire_outputs[b]
            )
            unknown_wires.remove(wire)

            wires_to_calculate = [
                unknown_wire
                for unknown_wire in unknown_wires
                if all(
                    [
                        wire in self.wire_outputs
                        for wire in self.gates[unknown_wire].input_wires
                    ]
                )
            ]
            for wire_to_calculate in wires_to_calculate:
                if wire_to_calculate not in queue:
                    queue.append(wire_to_calculate)


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        initial_vals, gates = input_file.read().strip().split("\n\n")
        self.x_vals = {}
        self.y_vals = {}
        for initial_val in initial_vals.splitlines():
            wire, val = initial_val.split(": ")
            if wire[0] == "x":
                self.x_vals[wire] = int(val)

            elif wire[0] == "y":
                self.y_vals[wire] = int(val)

        self.gates = dict()
        for g in gates.splitlines():
            first, operator, second, _, output = re.split(
                r"(AND|XOR|OR|->)", g.replace(" ", "")
            )
            self.gates[output] = Gate(operator, [first, second])

    def solve_part_1(self) -> int:
        circuit = Circuit(self.x_vals, self.y_vals, self.gates)
        circuit.solve_unknown_wires()
        z_wires = sorted(
            [wire for wire in circuit.wire_outputs.keys() if wire.startswith("z")]
        )
        return sum(
            [circuit.wire_outputs[z_wire] * 2**i for i, z_wire in enumerate(z_wires)]
        )

    def solve_part_2(self) -> str:
        circuit = Circuit(self.x_vals, self.y_vals, self.gates)
        broken = circuit.find_gate_swaps()
        return ",".join(sorted(broken))


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 24:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
