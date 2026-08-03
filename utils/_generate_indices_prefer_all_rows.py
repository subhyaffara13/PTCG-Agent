import random
import math


def _generate_indices_prefer_all_rows(rows: int, cols: int, num_indices: int) -> torch.Tensor:
    """Generate indices for a row x cols matrix, preferring at least one index per row if possible."""
    indices = []  # type: ignore[var-annotated]
    n_per_row = math.ceil(num_indices / rows)
    col_indices = list(range(cols))

    for r in range(rows):
        # Note that this can yield overlapping indices
        indices.extend((r, c) for c in random.choices(col_indices, k=n_per_row))

    return torch.tensor(indices[:num_indices])

