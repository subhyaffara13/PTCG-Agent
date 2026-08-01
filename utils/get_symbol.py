
def get_symbol(i: int) -> str:
    """Get the symbol corresponding to int ``i`` - runs through the usual 52
    letters before resorting to unicode characters, starting at ``chr(192)`` and skipping surrogates.

    **Examples:**

    ```python
    get_symbol(2)
    #> 'c'

    get_symbol(200)
    #> 'Ŕ'

    get_symbol(20000)
    #> '京'
    ```
    """
    if i < 52:
        return _einsum_symbols_base[i]
    elif i >= 55296:
        # Skip chr(57343) - chr(55296) as surrogates
        return chr(i + 2048)
    else:
        return chr(i + 140)

