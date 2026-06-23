def execute_object_set(original_objects, edited_objects):
    original_set = set(original_objects)
    edited_set = set(edited_objects)

    added = sorted(list(edited_set - original_set))
    removed = sorted(list(original_set - edited_set))

    passed = len(added) == 0 and len(removed) == 0

    if added:
        failure_type = "added object"
    elif removed:
        failure_type = "removed object"
    else:
        failure_type = "none"

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
    original_set = set(original_objects)
    edited_set = set(edited_objects)

    added = sorted(list(edited_set - original_set))
    passed = len(added) == 0

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
    original_set = set(original_objects)
    edited_set = set(edited_objects)

    removed = sorted(list(original_set - edited_set))
    passed = len(removed) == 0

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
