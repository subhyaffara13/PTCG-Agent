
def has_valid_einsum_chars_only(einsum_str: str) -> bool:
    """Check if ``einsum_str`` contains only valid characters for numpy einsum.

    **Examples:**

    ```python
    has_valid_einsum_chars_only("abAZ")
    #> True

    has_valid_einsum_chars_only("Över")
    #> False
    ```
    """
    return all(map(is_valid_einsum_char, einsum_str))

