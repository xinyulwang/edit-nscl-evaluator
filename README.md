# edit-nscl-evaluator

A lightweight NS-CL-inspired evaluator for instruction-guided image editing.

This project adapts symbolic program execution from neuro-symbolic concept learning to image editing evaluation. The goal is to identify where an edited image fails with respect to the original instruction, rather than only giving a black-box success/failure judgment.

## Motivation

When using an image editing model to change an image style, the model may satisfy the requested style but also introduce unwanted changes, such as adding new objects, adding a face, removing original content, or changing the image size.

For example, given the instruction:

```text
Please make this image in a Wong Kar-wai style.
```

the expected behavior is usually to change the visual style while preserving the original image content. However, the edited image may contain unexpected semantic changes.

This project explores whether an NS-CL-style program executor can make these failures easier to detect and explain.

## Goal

Given:

- original image
- editing instruction
- edited image

the system predicts:

- success or failure
- failure type
- module-level explanation

## Current stage: Evaluation

The current stage focuses on evaluation.

The pipeline is:

```text
Instruction
    ↓
Symbolic program
    ↓
Concept executors
    ↓
Constraint-level pass/fail results
    ↓
Overall success/failure + failure type
```

For a style editing instruction such as:

```text
给我提供王家卫风格的图片
```

or:

```text
apply a warm cinematic style
```

the system interprets the instruction as:

```text
Modify(Style)
Preserve(ObjectSet)
Preserve(ImageSize)
```

This means the edited image should change style while preserving the original object set and image size.

## Supported concepts

The current prototype supports:

- style modification
- object set preservation
- image size preservation

Earlier toy examples also support:

- warmth change
- object preservation

The warmth example is kept as a small sanity check for the program-execution pipeline.

## Example program

Input instruction:

```text
apply a warm cinematic style
```

Symbolic program:

```text
Modify(Style)
Preserve(ObjectSet)
Preserve(ImageSize)
```

Example output:

```text
Modify(Style): PASS
Preserve(ObjectSet): FAIL
Preserve(ImageSize): PASS

Overall: failure
Failure type: added object
```

This means the edited image achieved the requested style, but it added an unexpected object.

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

## Data format

Each sample contains:

```json
{
  "id": "style_001",
  "original_image": "images/originals/style_demo.png",
  "edited_image": "images/edits/style_demo_edited.png",
  "instruction": "apply a warm cinematic style",
  "human_label": "failure",
  "failure_type": "added object",
  "style_success": true,
  "original_objects": ["lighthouse", "building", "rocks", "ocean", "sky", "clouds"],
  "edited_objects": ["lighthouse", "building", "rocks", "ocean", "sky", "clouds", "face"]
}
```

Object annotations are manually prepared in the current prototype. Future versions will replace them with automatic object detection or VLM-based object extraction.

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

The first prototype uses manually prepared edited images and annotations to validate the program-execution pipeline. The next step is to evaluate real outputs from image editing models and analyze whether the evaluator can detect semantic drift, such as added objects or changed image size.
