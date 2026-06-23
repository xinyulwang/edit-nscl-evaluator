"""
This file runs the NS-CL-style evaluator.

It loads image editing samples, converts each instruction into a symbolic program,
executes module-level checks, prints the evaluation results, and saves predictions
to a CSV file.
"""


import json
import csv

# Convert an instruction into a symbolic program
from programs.templates import instruction_to_program

# Executor for warmth change
from executors.warmth import execute_warmth

# Executors for object preservation checks
from executors.object_set import (
    execute_object_set,
    execute_forbid_add_object,
    execute_forbid_remove_object,
)


def execute_step(sample, step):
    # Get image paths
    original_image = sample["original_image"]
    edited_image = sample["edited_image"]

    # Get object lists
    original_objects = sample.get("original_objects", [])
    edited_objects = sample.get("edited_objects", [])

    # Get operation and concept from the program step
    op = step["op"]
    concept = step["concept"]

    # Check warmth modification
    if op == "Modify" and concept == "Warmth":
        return execute_warmth(
            original_image,
            edited_image,
            direction=step.get("direction", "increase"),
        )

    # Check whether object sets are preserved
    if op == "Preserve" and concept == "ObjectSet":
        return execute_object_set(original_objects, edited_objects)

    # Check whether new objects are added
    if op == "Forbid" and concept == "AddObject":
        return execute_forbid_add_object(original_objects, edited_objects)

    # Check whether existing objects are removed
    if op == "Forbid" and concept == "RemoveObject":
        return execute_forbid_remove_object(original_objects, edited_objects)

    # Return failure if no executor is implemented
    return {
        "op": op,
        "concept": concept,
        "pass": False,
        "failure_type": "missing executor",
        "explanation": f"No executor implemented for {op}({concept}).",
    }


def execute_program(sample, program):
    # Store results for each program step
    module_results = []

    # Execute each step in the symbolic program
    for step in program:
        result = execute_step(sample, step)
        module_results.append(result)

    # Overall success only if all modules pass
    overall_success = all(result["pass"] for result in module_results)

    # Collect failure types from failed modules
    failure_types = [
        result["failure_type"]
        for result in module_results
        if not result["pass"] and result["failure_type"] != "none"
    ]

    # Use "none" if there is no failure
    if not failure_types:
        failure_types = ["none"]

    return {
        "module_results": module_results,
        "overall_success": overall_success,
        "failure_types": failure_types,
    }


def main():
    # Load evaluation samples
    with open("data/samples.json", "r") as f:
        samples = json.load(f)

    # Store rows for the output CSV
    rows = []

    # Run evaluation for each sample
    for sample in samples:
        # Convert instruction to symbolic program
        program = instruction_to_program(sample["instruction"])

        # Execute the symbolic program
        execution = execute_program(sample, program)

        # Print sample information
        print("=" * 60)
        print("ID:", sample["id"])
        print("Instruction:", sample["instruction"])

        # Print symbolic program
        print("\nProgram:")
        for step in program:
            print(" ", step)

        # Print module-level execution results
        print("\nExecution:")
        for result in execution["module_results"]:
            status = "PASS" if result["pass"] else "FAIL"
            print(f"  {result['op']}({result['concept']}): {status}")
            print(f"    {result['explanation']}")

        # Convert boolean result to label
        predicted_label = "success" if execution["overall_success"] else "failure"

        # Print final prediction
        print("\nOverall:", predicted_label)
        print("Failure types:", execution["failure_types"])

        # Add one row to the CSV output
        rows.append({
            "id": sample["id"],
            "instruction": sample["instruction"],
            "human_label": sample.get("human_label", ""),
            "human_failure_type": sample.get("failure_type", ""),
            "predicted_label": predicted_label,
            "predicted_failure_type": "; ".join(execution["failure_types"]),
        })

    # Save results to CSV
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

        # Write CSV header and rows
        writer.writeheader()
        writer.writerows(rows)

    print("\nSaved results to results/results.csv")


# Run main function
if __name__ == "__main__":
    main()
