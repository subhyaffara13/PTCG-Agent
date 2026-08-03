from typing import Any

def _combine_rank_results(rank_results: dict[int, Any], default: Any | None) -> Any:
    rank_ids = rank_results.keys()
    rank_value = rank_results[next(iter(rank_ids))]

    if isinstance(rank_value, (list, tuple)):
        max_rank_result_len = max(len(v) for v in rank_results.values())
        ret_list = []
        for i in range(max_rank_result_len):
            rank_col_results = {
                r: v[i] if i < len(v) else default for r, v in rank_results.items()
            }
            ret_list.append(_combine_any_rank_results(rank_col_results))
        return type(rank_value)(ret_list)
    else:
        return _combine_any_rank_results(rank_results)

