from typing import Callable

def newer_pairwise(
    sources: Iterable[_SourcesT],
    targets: Iterable[_TargetsT],
    newer: Callable[[_SourcesT, _TargetsT], bool] = newer,
) -> tuple[list[_SourcesT], list[_TargetsT]]:
    """
    Filter filenames where sources are newer than targets.

    Walk two filename iterables in parallel, testing if each source is newer
    than its corresponding target.  Returns a pair of lists (sources,
    targets) where source is newer than target, according to the semantics
    of 'newer()'.
    """
    newer_pairs = filter(splat(newer), zip_strict(sources, targets))
    return tuple(map(list, zip(*newer_pairs))) or ([], [])

