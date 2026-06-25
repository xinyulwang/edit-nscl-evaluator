"""
Run evaluation.

This file loads samples, converts instructions into symbolic programs,
runs the evaluator, and saves the results.
"""

import json
from pathlib import Path

from programs.templates import instruction_to_program
from evaluation.evaluator import evaluate_sample


def main():
    samples_path = Path("data/samples.json")
    output_path = Path("results/result.json")

    with open(samples_path, "r") as f:
        samples = json.load(f)

    all_results = []

    for sample in samples:
        program = instruction_to_program(sample["instruction"])
        result = evaluate_sample(sample, program)
        all_results.append(result)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"Saved results to {output_path}")


if __name__ == "__main__":
    main()
