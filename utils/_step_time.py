
def _step_time(gs: dict[str, Any], timer: TimeManager, router: RouterBus) -> dict[str, Any]:
    from router.bus import TimePacket
    return router.dispatch("TimeManager", TimePacket(
        time_elapsed=gs.get("time_elapsed", 0.0),
        time_limit=gs.get("time_limit", 600.0),
        legal_actions=gs.get("legal_actions", [])
    ))


def _step_time(gs: dict[str, Any], timer: TimeManager, router: RouterBus) -> dict[str, Any]:
    from router.bus import TimePacket
    return router.dispatch("TimeManager", TimePacket(
        time_elapsed=gs.get("time_elapsed", 0.0),
        time_limit=gs.get("time_limit", 600.0),
        legal_actions=gs.get("legal_actions", [])
    ))


def _step_time(gs: dict[str, Any], timer: TimeManager, router: RouterBus) -> dict[str, Any]:
    from router.bus import TimePacket
    return router.dispatch("TimeManager", TimePacket(
        time_elapsed=gs.get("time_elapsed", 0.0),
        time_limit=gs.get("time_limit", 600.0),
        legal_actions=gs.get("legal_actions", [])
    ))

