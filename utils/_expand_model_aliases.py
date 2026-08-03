from typing import Dict, List, Optional

def _expand_model_aliases(model_cost: dict) -> dict:
    """
    Expand ``aliases`` lists in model cost entries into top-level entries.

    Each alias gets a reference to the **same** dict object as the canonical
    entry (zero memory overhead).  The ``aliases`` key is removed from the
    entry so downstream code never sees it.

    If an alias collides with an existing canonical entry the alias is
    skipped and a warning is logged.
    """
    aliases_to_add: Dict[str, dict] = {}
    keys_with_aliases: List[str] = []

    for model_name, model_info in model_cost.items():
        aliases: Optional[list] = model_info.get("aliases")
        if aliases is None:
            continue
        keys_with_aliases.append(model_name)
        if not isinstance(aliases, list):
            verbose_logger.warning(
                "LiteLLM model alias field for '%s' is not a list (got %s) — skipping.",
                model_name,
                type(aliases).__name__,
            )
            continue
        if not aliases:
            continue
        for alias in aliases:
            if alias in model_cost:
                verbose_logger.warning(
                    "LiteLLM model alias conflict: alias '%s' (from '%s') "
                    "already exists as a canonical entry — skipping.",
                    alias,
                    model_name,
                )
                continue
            if alias in aliases_to_add:
                verbose_logger.warning(
                    "LiteLLM model alias conflict: alias '%s' (from '%s') "
                    "was already claimed by another entry — skipping.",
                    alias,
                    model_name,
                )
                continue
            aliases_to_add[alias] = model_info  # same dict reference

    # Remove the ``aliases`` key from entries so it doesn't pollute model info
    for key in keys_with_aliases:
        model_cost[key].pop("aliases", None)

    model_cost.update(aliases_to_add)
    return model_cost

