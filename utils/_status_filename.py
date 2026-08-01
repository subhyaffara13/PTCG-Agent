
def _status_filename(cell: GameCell) -> str:
    """Sanitize cell coords into a single filesystem-safe filename."""
    def s(x: str) -> str:
        return str(x).replace("/", "_").replace(" ", "_")
    return (
        f"{s(cell.variant)}__{s(cell.model_p0)}__vs__{s(cell.model_p1)}"
        f"__{s(cell.pair_role)}__seed{cell.seed}.json"
    )

