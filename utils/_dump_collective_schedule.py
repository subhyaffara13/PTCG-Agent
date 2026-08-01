
def _dump_collective_schedule(schedule: list[str | None]) -> None:
    try:
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "inductor_collective_schedule",
                "encoding": "json",
            },
            payload_fn=lambda: schedule,
        )
    except Exception:
        log.debug(
            "Failed to log inductor_collective_schedule via structured logging",
            exc_info=True,
        )

