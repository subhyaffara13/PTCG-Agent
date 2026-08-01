
def is_valid_einsum_char(x: str) -> bool:
    """Check if the character ``x`` is valid for numpy einsum.

    **Examples:**

    ```python
    is_valid_einsum_char("a")
    #> True

    is_valid_einsum_char("Ǵ")
    #> False
    ```
    """
    return (x in _einsum_symbols_base) or (x in ",->.")

