"""
Instruction-to-program template.

This file converts a natural language editing instruction into a symbolic program.
Each program step is later executed by a concept executor.
"""


def instruction_to_program(instruction: str):
    # Convert instruction to lowercase for easier matching
    instruction = instruction.lower()

    # Case 1: Make image warmer and preserve objects
    if "warmer" in instruction and "without changing" in instruction:
        return [
            # Increase image warmth
            {"op": "Modify", "concept": "Warmth", "direction": "increase"},

            # Preserve the original object set
            {"op": "Preserve", "concept": "ObjectSet"},

            # Do not add new objects
            {"op": "Forbid", "concept": "AddObject"},

            # Do not remove existing objects
            {"op": "Forbid", "concept": "RemoveObject"},
        ]

    # Case 2: Only make image warmer
    if "warmer" in instruction:
        return [
            # Increase image warmth
            {"op": "Modify", "concept": "Warmth", "direction": "increase"},
        ]

    # Case 3: Increase image contrast
    if "contrast" in instruction:
        return [
            # Increase image contrast
            {"op": "Modify", "concept": "Contrast", "direction": "increase"},
        ]

    # Raise an error if the instruction is not supported
    raise ValueError(f"Unknown instruction: {instruction}")
