import json
import csv

from programs.templates import instruction_to_program
from executors.warmth import execute_warmth
from executors.object_set import (
    execute_object_set,
    execute_forbid_add_object,
    execute_forbid_remove_object,
)


def execute_step(sample, step):
    original_image = sample["original_image"]
    edited_image = sample["edited_image"]

    original_objects = sample.get("original_objects", [])
    edited_objects = sample.get("edited_objects", [])

    op = step["op"]
    concept = step["concept"]

    if op == "Modify" and concept == "Warmth":
        return execute_warmth(
            original_image,
            edited_image,
            direction=step.get("direction", "increase"),
        )

    if op == "Preserve" and concept == "ObjectSet":
        return execute_object_set(original_objects, edited_objects)

    if op == "Forbid" and concept == "AddObject":
        return execute_forbid_add_object(original_objects, edited_objects)

    if op == "Forbid" and concept == "RemoveObject":
        return execute_forbid_remove_object(original_objects, edited_objects)

    return {
        "op": op,
        "concept": concept,
        "pass": False,
        "failure_type": "missing executor",
        "explanation": f"No executor implemented for {op}({concept}).",
    }


def execute_program(sample, program):
    module_results = []

    for step in program:
        result = execute_step(sample, step)
        module_results.append(result)

    overall_success = all(result["pass"] for result in module_results)

    failure_types = [
        result["failure_type"]
        for result in module_results
        if not result["pass"] and result["failure_type"] != "none"
    ]

    if not failure_types:
        failure_types = ["none"]

    return {
        "module_results": module_results,
        "overall_success": overall_success,
        "failure_types": failure_types,
    }


def main():
    with open("data/samples.json", "r") as f:
        samples = json.load(f)

    rows = []

    for sample in samples:
        program = instruction_to_program(sample["instruction"])
        execution = execute_program(sample, program)

        print("=" * 60)
        print("ID:", sample["id"])
        print("Instruction:", sample["instruction"])

        print("\nProgram:")
        for step in program:
            print(" ", step)

        print("\nExecution:")
        for result in execution["module_results"]:
            status = "PASS" if result["pass"] else "FAIL"
            print(f"  {result['op']}({result['concept']}): {status}")
            print(f"    {result['explanation']}")

        predicted_label = "success" if execution["overall_success"] else "failure"

        print("\nOverall:", predicted_label)
        print("Failure types:", execution["failure_types"])

        rows.append({
            "id": sample["id"],
            "instruction": sample["instruction"],
            "human_label": sample.get("human_label", ""),
            "human_failure_type": sample.get("failure_type", ""),
            "predicted_label": predicted_label,
            "predicted_failure_type": "; ".join(execution["failure_types"]),
        })

    with open("results/results.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "instruction",
                "human_label",
                "human_failure_type",
                "predicted_label",
                "predicted_failure_type",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print("\nSaved results to results/results.csv")


if __name__ == "__main__":
    main()
