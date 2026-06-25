"""
Evaluator.

This file executes the symbolic program and collects module-level results.
"""

from executors.style import execute_style
from executors.object_set import (
    execute_object_set,
    execute_forbid_add_object,
    execute_forbid_remove_object,
)
from executors.image_size import execute_image_size


def evaluate_sample(sample: dict, program: list):
    original_path = sample["original_image"]
    edited_path = sample["edited_image"]

    results = []

    for step in program:
        op = step["op"]
        concept = step["concept"]

        if op == "Modify" and concept == "Style":
            result = execute_style(
                original_path=original_path,
                edited_path=edited_path,
                target_style=step.get("target", sample.get("target_style", "unknown"))
            )

        elif op == "Preserve" and concept == "ObjectSet":
            result = execute_object_set(
                original_objects=sample["original_objects"],
                edited_objects=sample["edited_objects"]
            )

        elif op == "Preserve" and concept == "ImageSize":
            result = execute_image_size(
                original_path=original_path,
                edited_path=edited_path
            )

        elif op == "Forbid" and concept == "AddObject":
            result = execute_forbid_add_object(
                original_objects=sample["original_objects"],
                edited_objects=sample["edited_objects"]
            )

        elif op == "Forbid" and concept == "RemoveObject":
            result = execute_forbid_remove_object(
                original_objects=sample["original_objects"],
                edited_objects=sample["edited_objects"]
            )

        else:
            result = {
                "op": op,
                "concept": concept,
                "pass": False,
                "failure_type": "unsupported constraint",
                "explanation": f"Unsupported constraint: {op}({concept})"
            }

        results.append(result)

    overall_passed = all(result["pass"] for result in results)

    failure_types = [
        result["failure_type"]
        for result in results
        if not result["pass"]
    ]

    return {
        "sample_id": sample["id"],
        "instruction": sample["instruction"],
        "program": program,
        "overall_passed": overall_passed,
        "failure_types": failure_types,
        "results": results
    }
