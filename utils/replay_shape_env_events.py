
def replay_shape_env_events(events: list[ShapeEnvEvent]) -> ShapeEnv:
    from torch.fx.experimental.symbolic_shapes import ShapeEnv

    constructor_event = events[0]
    if constructor_event.f != ShapeEnv:
        raise AssertionError(
            f"First event must be ShapeEnv constructor, got {constructor_event.f}"
        )

    # Constructs the new ShapeEnv.
    shape_env = constructor_event.run()

    for event in events[1:]:
        try:
            # Actually replays each event.
            # We need to call create_mapping_fn every time, since the node list might
            # change after each event is replayed.
            event.run(shape_env)
        except Exception:
            log.error("failed when running event: %s", event)
            raise

    return shape_env

