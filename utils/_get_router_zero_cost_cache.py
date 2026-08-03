from typing import Dict, Optional

def _get_router_zero_cost_cache(llm_router: Router) -> Optional[Dict[str, bool]]:
    """
    Return the router's per-instance zero-cost cache, or ``None`` for objects
    that don't expose one (e.g. ``MagicMock`` stand-ins in unit tests).

    The cache lives on the ``Router`` instance so it:
        * is invalidated by ``Router._invalidate_model_group_info_cache`` on
          any model add/remove/upsert (including in-place pricing changes via
          ``/model/update``, which go through ``upsert_deployment``);
        * dies with the router itself — no risk of CPython reusing the
          previous router's ``id()`` and serving its cached entries.
    """
    cache = getattr(llm_router, "_zero_cost_cache", None)
    return cache if isinstance(cache, dict) else None

