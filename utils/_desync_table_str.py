from typing import Any

def _desync_table_str(tag: str, value_ranks: dict[Any, set[int]]) -> str:
    headers = ["Ranks", f"{tag} values"]
    rank_values = [
        [_summarize_ranks(ranks), str(value)] for value, ranks in value_ranks.items()
    ]
    if importlib.util.find_spec("tabulate"):
        from tabulate import tabulate

        return tabulate(rank_values, headers=headers)
    row_str = "\n".join([str(row) for row in rank_values])
    return str(f"{headers}\n{row_str}")

