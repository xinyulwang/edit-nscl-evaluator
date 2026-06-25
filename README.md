# edit-nscl-evaluator

A lightweight NS-CL-inspired evaluator for instruction-guided image editing.

## Motivation

When I ask an image editing model to change the style of an image, the model may also make unwanted changes, such as adding new objects or changing the image size.

Example instruction:

```text
Please make this image in a Wong Kar-wai style.
```

The expected behavior is to change the style while preserving the original content.

## Goal

The long-term goal is to use NS-CL-style instruction decomposition to help LLM/image editing models make fewer mistakes.

Instead of sending a vague instruction directly to an image editing model, the instruction can be decomposed into explicit constraints:

```text
Modify(Style)
Preserve(ObjectSet)
Preserve(ImageSize)
```

These constraints can be used to evaluate the edited image and provide structured feedback.

## Current stage: Evaluator

This project is currently an evaluator prototype, not an end-to-end image editing system.

I do not directly call an LLM or image editing model in the code. Instead, I manually obtain an edited image from a model using an instruction such as:

```text
Please make this image in a Wong Kar-wai style.
```

Then I put the original image, the instruction, and the edited image into the evaluator.

Current evaluator v1:

- `Modify(Style)`: assumed to pass in the current prototype.
- `Preserve(ObjectSet)`: checked by comparing manually annotated object categories between the original and edited images.
- `Preserve(ImageSize)`: checked by comparing image width and height.

The evaluator focuses on detecting unintended preservation failures, such as added/removed objects or image size changes.

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
Constraint-level pass/fail results
        ↓
Overall result + failure type
```

## Supported concepts

Current prototype:

- `Modify(Style)`
- `Preserve(ObjectSet)`
- `Preserve(ImageSize)`

For `Modify(Style)`, the current prototype assumes success. The main focus is on detecting unintended preservation failures, especially object set changes and image size changes.


## Next step

After the evaluator works, it can be used as a feedback module:

```text
Generate edited image
        ↓
Evaluate constraints
        ↓
Find failure type
        ↓
Send structured feedback to the model
        ↓
Regenerate or revise the image
```

The final goal is to use this neuro-symbolic decomposition as a guardrail for LLM-based image editing.


## Warmth toy demo

As a first sanity check, I implemented a small warmth-editing example:

```text
make the image warmer without changing the objects
```

This instruction is decomposed into:

```text
Modify(Warmth)
Preserve(ObjectSet)
```

The demo checks whether the edited image becomes warmer while keeping the same object set. It verifies that the basic NS-CL-style pipeline works:

```text
instruction → symbolic program → concept executors → pass/fail results
```

This toy demo is used to validate the program-execution structure before moving to the main style-editing evaluation task.
