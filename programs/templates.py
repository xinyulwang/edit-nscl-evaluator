"""
Instruction-to-program templates.

This file converts a natural language instruction into a symbolic program.
"""


def instruction_to_program(instruction: str):
    instruction_lower = instruction.lower()

    if "wong kar-wai" in instruction_lower or "style" in instruction_lower:
        return [
            {
                "op": "Modify",
                "concept": "Style",
                "target": "Wong Kar-wai"
            },
            {
                "op": "Preserve",
                "concept": "ObjectSet"
            },
            {
                "op": "Preserve",
                "concept": "ImageSize"
            }
        ]

    if "warmer" in instruction_lower or "warm" in instruction_lower:
        return [
            {
                "op": "Modify",
                "concept": "Warmth",
                "direction": "increase"
            },
            {
                "op": "Preserve",
                "concept": "ObjectSet"
            }
        ]

    raise ValueError(f"Unknown instruction: {instruction}")
