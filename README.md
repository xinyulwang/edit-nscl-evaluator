# edit-nscl-evaluator

A lightweight NS-CL-inspired evaluator for instruction-guided image editing.

This project adapts the idea of symbolic program execution from neuro-symbolic concept learning to image editing evaluation.

## Goal

Given:

- original image
- editing instruction
- edited image

the system predicts:

- success or failure
- failure type
- module-level explanation

## First version

The first version focuses on one editing instruction:

```text
make the image warmer without changing the objects
```

This instruction is converted into a symbolic program:

```text
Modify(Warmth, increase)
Preserve(ObjectSet)
Forbid(AddObject)
Forbid(RemoveObject)
```

The current prototype supports two types of concept checks:

- warmth change
- object preservation

Contrast change and other editing concepts will be added in later versions.

## Pipeline

```text
Original image + Instruction + Edited image
        ↓
Instruction-to-program template
        ↓
Symbolic program
        ↓
Concept executors
        ↓
Module-level pass/fail results
        ↓
Overall success/failure + failure type
```

## Example

Input instruction:

```text
make the image warmer without changing the objects
```

Example output:

```text
Modify(Warmth): PASS
Preserve(ObjectSet): PASS
Forbid(AddObject): PASS
Forbid(RemoveObject): PASS

Overall: success
Failure type: none
```

## Project structure

```text
data/
images/
programs/
executors/
evaluation/
results/
docs/
```

## Notes

This repository is a framework-level adaptation of NS-CL-style program execution, not a direct fork of the original NS-CL codebase.

In the first prototype, edited images and object annotations are manually prepared to validate the program-execution pipeline. Future versions will replace manual object annotations with automatic detectors or VLM-based object extraction, and use outputs from real image editing models.
