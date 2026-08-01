
def gen_unused_symbols(used: str, n: int) -> Iterator[str]:
    """Generate ``n`` symbols that are not already in ``used``.

    **Examples:**
    ```python
    list(oe.parser.gen_unused_symbols("abd", 2))
    #> ['c', 'e']
    ```
    """
    i = cnt = 0
    while cnt < n:
        s = get_symbol(i)
        i += 1
        if s in used:
            continue
        yield s
        cnt += 1

