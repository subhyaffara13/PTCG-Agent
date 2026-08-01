
def accumulate_run_step(
    *,
    event: AssistantStreamEvent,
    run_step_snapshots: dict[str, RunStep],
) -> None:
    if event.event == "thread.run.step.created":
        run_step_snapshots[event.data.id] = event.data
        return

    if event.event == "thread.run.step.delta":
        data = event.data
        snapshot = run_step_snapshots[data.id]

        if data.delta:
            merged = accumulate_delta(
                cast(
                    "dict[object, object]",
                    model_dump(snapshot, exclude_unset=True, warnings=False),
                ),
                cast(
                    "dict[object, object]",
                    model_dump(data.delta, exclude_unset=True, warnings=False),
                ),
            )
            run_step_snapshots[snapshot.id] = cast(RunStep, construct_type(type_=RunStep, value=merged))

    return None

