
def _backends_kwargs_from_request(request, skip_or_xfail):
    """A helper for {skip,xfail}_xp_backends.

    Return dict of {backend to skip/xfail: top reason to skip/xfail it}
    """
    markers = list(request.node.iter_markers(f'{skip_or_xfail}_xp_backends'))
    reasons = {backend: [] for backend in xp_known_backends}

    for marker in markers:
        invalid_kwargs = set(marker.kwargs) - {
            "cpu_only", "np_only", "eager_only", "reason", "exceptions"}
        if invalid_kwargs:
            raise TypeError(f"Invalid kwargs: {invalid_kwargs}")

        exceptions = set(marker.kwargs.get('exceptions', []))
        invalid_exceptions = exceptions - xp_known_backends
        if (invalid_exceptions := list(exceptions - xp_known_backends)):
            raise ValueError(f"Unknown backend(s): {invalid_exceptions}; "
                             f"must be a subset of {list(xp_known_backends)}")

        if marker.kwargs.get('np_only', False):
            reason = marker.kwargs.get("reason") or "do not run with non-NumPy backends"
            for backend, backend_reasons in reasons.items():
                if backend != 'numpy' and backend not in exceptions:
                    backend_reasons.append(reason)

        elif marker.kwargs.get('cpu_only', False):
            reason = marker.kwargs.get("reason") or (
                "no array-agnostic implementation or delegation available "
                "for this backend and device")
            for backend in xp_skip_cpu_only_backends - exceptions:
                reasons[backend].append(reason)

        elif marker.kwargs.get('eager_only', False):
            reason = marker.kwargs.get("reason") or (
                "eager checks not executed on lazy backends")
            for backend in xp_skip_eager_only_backends - exceptions:
                reasons[backend].append(reason)

        # add backends, if any
        if len(marker.args) == 1:
            backend = marker.args[0]
            if backend not in xp_known_backends:
                raise ValueError(f"Unknown backend: {backend}; "
                                 f"must be one of {list(xp_known_backends)}")
            reason = marker.kwargs.get("reason") or (
                f"do not run with array API backend: {backend}")
            # reason overrides the ones from cpu_only, np_only, and eager_only.
            # This is regardless of order of appearence of the markers.
            reasons[backend].insert(0, reason)

            for kwarg in ("cpu_only", "np_only", "eager_only", "exceptions"):
                if kwarg in marker.kwargs:
                    raise ValueError(f"{kwarg} is mutually exclusive with {backend}")

        elif len(marker.args) == 2 and isinstance(marker.args[1], bool | type(None)):
            # condition is provided:
            #   1. check it
            #   2. reason is required (similar to pytest's xfail/skipif)
            backend, condition = marker.args

            if backend not in xp_known_backends:
                raise ValueError(f"Unknown backend: {backend}; "
                                 f"must be one of {list(xp_known_backends)}")

            if condition:
                reason = marker.kwargs.get("reason")
                # reason overrides the ones from cpu_only, np_only, and eager_only.
                # This is regardless of order of appearance of the markers.
                reasons[backend].insert(0, reason)

            for kwarg in ("cpu_only", "np_only", "eager_only", "exceptions"):
                if kwarg in marker.kwargs:
                    raise ValueError(f"{kwarg} is mutually exclusive with {backend}")

        elif len(marker.args) > 1:
            raise ValueError(
                f"Please specify only one backend per marker: {marker.args}"
            )

    return {backend: backend_reasons[0]
            for backend, backend_reasons in reasons.items()
            if backend_reasons}

