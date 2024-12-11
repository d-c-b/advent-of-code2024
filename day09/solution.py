from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        input_string = input_file.read().strip()
        self.memory_blocks = dict()
        self.file_locations_lengths = []
        self.empty_locations_lengths = []

        memory_index = 0
        file_id = 0
        for i, length in enumerate(input_string):
            block_length = int(length)
            if i % 2 == 0:
                for j in range(memory_index, memory_index + block_length):
                    self.memory_blocks[j] = file_id

                self.file_locations_lengths.append(
                    (file_id, (memory_index, block_length))
                )
                file_id += 1

            else:
                self.empty_locations_lengths.append((memory_index, block_length))

            memory_index += block_length

        self.MAX_FILLED_MEMORY_POSITION = max(
            [key for key in self.memory_blocks.keys()]
        )

    def calculate_checksum(self, memory: dict[int, int]) -> int:
        return sum(
            [
                memory_index * file_id
                for memory_index, file_id in memory.items()
                if file_id >= 0
            ]
        )

    def solve_part_1(self) -> int:
        reordered_memory = {**self.memory_blocks}
        l_pointer, r_pointer = 0, self.MAX_FILLED_MEMORY_POSITION

        while l_pointer < r_pointer:
            if l_pointer in reordered_memory:
                l_pointer += 1

            else:
                if r_pointer in reordered_memory:
                    reordered_memory[l_pointer] = reordered_memory[r_pointer]
                    reordered_memory[r_pointer] = -1
                r_pointer -= 1

        return self.calculate_checksum(reordered_memory)

    def solve_part_2(self) -> int:
        reordered_memory = {**self.memory_blocks}
        files_to_move = [*self.file_locations_lengths]
        empty_memory_positions = [*self.empty_locations_lengths]

        while files_to_move:
            file_id, (file_start_index, file_length) = files_to_move.pop()
            possible_locations = [
                (memory_index, empty_len)
                for (memory_index, empty_len) in empty_memory_positions
                if empty_len >= file_length and memory_index < file_start_index
            ]

            if len(possible_locations) > 0:
                (free_memory_start_index, free_memory_len), *_ = possible_locations

                for i in range(file_length):
                    reordered_memory[free_memory_start_index + i] = file_id
                    reordered_memory[file_start_index + i] = -1

                free_memory_list_index = empty_memory_positions.index(
                    (free_memory_start_index, free_memory_len)
                )

                updated = (
                    [
                        (
                            free_memory_start_index + file_length,
                            free_memory_len - file_length,
                        )
                    ]
                    if file_length < free_memory_len
                    else []
                )

                empty_memory_positions = [
                    *empty_memory_positions[:free_memory_list_index],
                    *updated,
                    *empty_memory_positions[free_memory_list_index + 1 :],
                ]

        return self.calculate_checksum(reordered_memory)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 09:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
