
def sort_problems(problems):
    """Sort problem groups by their most severe problem type."""
    return dict(
        sorted(
            problems.items(),
            key=lambda _: -min(
                (
                    (InterpolatableProblem.severity[p["type"]] + p.get("tolerance", 0))
                    for p in _[1]
                ),
            ),
            reverse=True,
        )
    )

