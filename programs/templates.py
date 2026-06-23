def instruction_to_program(instruction: str):
    instruction = instruction.lower()

    if "warmer" in instruction and "without changing" in instruction:
        return [
            {"op": "Modify", "concept": "Warmth", "direction": "increase"},
            {"op": "Preserve", "concept": "ObjectSet"},
            {"op": "Forbid", "concept": "AddObject"},
            {"op": "Forbid", "concept": "RemoveObject"},
        ]

    if "warmer" in instruction:
        return [
            {"op": "Modify", "concept": "Warmth", "direction": "increase"},
        ]

    if "contrast" in instruction:
        return [
            {"op": "Modify", "concept": "Contrast", "direction": "increase"},
        ]

    raise ValueError(f"Unknown instruction: {instruction}")
