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

The first version supports:

- warmth change
- contrast change
- object preservation

## Project structure

```text
data/
images/
programs/
executors/
evaluation/
results/
docs/
