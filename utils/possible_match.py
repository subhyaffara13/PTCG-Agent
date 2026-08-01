
def possible_match(results: ResultHolder, used: set[int] | None = None) -> bool:
    if used is None:
        used = set()
    curr_row = len(used)
    if curr_row == len(results.results):
        return True
    return any(
        val is None and i not in used and possible_match(results, used | {i})
        for (i, val) in enumerate(results.results[curr_row])
    )

