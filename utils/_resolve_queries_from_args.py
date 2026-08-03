from typing import Any, Dict, List

def _resolve_queries_from_args(args: Dict[str, Any], input: Any) -> List[str]:
    """Pull the queries list out of parsed tool-call arguments, with backward-compat fallbacks."""
    queries_from_call = args.get("queries")
    if not queries_from_call:
        # Fallback: check for single "query" field (backward compat)
        single_query = args.get("query")
        return [single_query] if single_query else [str(input)]
    if not isinstance(queries_from_call, list):
        return [str(queries_from_call)]
    return queries_from_call

