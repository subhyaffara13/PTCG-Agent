
def _maybe_in_subresource(
    in_value: Set[str] = frozenset(),
    in_subvalues: Set[str] = frozenset(),
    in_subarray: Set[str] = frozenset(),
):
    in_child = in_subvalues | in_subarray

    def maybe_in_subresource(
        segments: Sequence[int | str],
        resolver: _Resolver[Any],
        subresource: Resource[Any],
    ) -> _Resolver[Any]:
        _segments = iter(segments)
        for segment in _segments:
            if segment not in in_value and (
                segment not in in_child or next(_segments, None) is None
            ):
                return resolver
        return resolver.in_subresource(subresource)

    return maybe_in_subresource

