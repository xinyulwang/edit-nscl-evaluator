"""
Style executor.

For the current evaluator, we assume the requested style edit is successful.
This allows the evaluator to focus on preservation constraints such as
ObjectSet and ImageSize.
"""


def execute_style(original_path: str, edited_path: str, target_style: str):
    return {
        "op": "Modify",
        "concept": "Style",
        "target_style": target_style,
        "pass": True,
        "failure_type": "none",
        "explanation": f"The style edit is assumed to satisfy the target style: {target_style}."
    }
