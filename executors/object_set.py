"""
Object set executors.

This file checks whether the edited image preserves the original objects.
It detects added objects, removed objects, and returns module-level pass/fail results.
"""


def execute_object_set(original_objects, edited_objects):
    # Convert object lists to sets for comparison
    original_set = set(original_objects)
    edited_set = set(edited_objects)

    # Objects that appear only in the edited image
    added = sorted(list(edited_set - original_set))

    # Objects that appear only in the original image
    removed = sorted(list(original_set - edited_set))

    # Pass only if no object is added or removed
    passed = len(added) == 0 and len(removed) == 0

    # Decide the failure type
    if added:
        failure_type = "added object"
    elif removed:
        failure_type = "removed object"
    else:
        failure_type = "none"

    # Return the module-level result
    return {
        "op": "Preserve",
        "concept": "ObjectSet",
        "pass": passed,
        "original_objects": original_objects,
        "edited_objects": edited_objects,
        "added_objects": added,
        "removed_objects": removed,
        "failure_type": failure_type,
        "explanation": (
            "The object set is preserved."
            if passed
            else f"Object set changed. Added: {added}, Removed: {removed}"
        ),
    }


def execute_forbid_add_object(original_objects, edited_objects):
    # Convert object lists to sets
    original_set = set(original_objects)
    edited_set = set(edited_objects)

    # Find newly added objects
    added = sorted(list(edited_set - original_set))

    # Pass only if no new object is added
    passed = len(added) == 0

    # Return the result for AddObject check
    return {
        "op": "Forbid",
        "concept": "AddObject",
        "pass": passed,
        "added_objects": added,
        "failure_type": "none" if passed else "added object",
        "explanation": (
            "No new object was added."
            if passed
            else f"New objects were added: {added}"
        ),
    }


def execute_forbid_remove_object(original_objects, edited_objects):
    # Convert object lists to sets
    original_set = set(original_objects)
    edited_set = set(edited_objects)

    # Find removed objects
    removed = sorted(list(original_set - edited_set))

    # Pass only if no object is removed
    passed = len(removed) == 0

    # Return the result for RemoveObject check
    return {
        "op": "Forbid",
        "concept": "RemoveObject",
        "pass": passed,
        "removed_objects": removed,
        "failure_type": "none" if passed else "removed object",
        "explanation": (
            "No object was removed."
            if passed
            else f"Objects were removed: {removed}"
        ),
    }
