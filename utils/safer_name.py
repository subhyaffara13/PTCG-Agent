import re

def safer_name(value: str) -> str:
    """Like ``safe_name`` but can be used as filename component for wheel"""
    # See bdist_wheel.safer_name
    return (
        # Per https://packaging.python.org/en/latest/specifications/name-normalization/#name-normalization
        re
        .sub(r"[-_.]+", "-", safe_name(value))
        .lower()
        # Per https://packaging.python.org/en/latest/specifications/binary-distribution-format/#escaping-and-unicode
        .replace("-", "_")
    )


def safer_name(name: str) -> str:
    return safe_name(name).replace("-", "_")

