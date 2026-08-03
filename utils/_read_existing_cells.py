from pathlib import Path


def _read_existing_cells(csv_path: Path) -> set[tuple]:
    """Return the set of cell keys already present in games.csv (for --resume)."""
    if not csv_path.exists():
        return set()
    done: set[tuple] = set()
    with csv_path.open() as f:
        for row in csv.DictReader(f):
            done.add((
                row["variant"], row["model_p0"], row["model_p1"],
                row["pair_role"], int(row["seed"]),
            ))
    return done

