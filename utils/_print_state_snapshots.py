
def _print_state_snapshots(
    snapshots: dict[_State, list[dict[torch.device, dict[str, int]]]], units: str
) -> None:
    for state, snapshot_list in snapshots.items():
        print(f"{state.value}")
        for i, snapshot in enumerate(snapshot_list):
            print(f"# {i + 1}:")
            _print_snapshot(snapshot, units)
    print()

