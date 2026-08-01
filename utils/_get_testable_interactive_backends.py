
def _get_testable_interactive_backends():
    # We re-create this because some of the callers below might modify the markers.
    return [pytest.param({**env}, marks=[*marks],
                         id='-'.join(f'{k}={v}' for k, v in env.items()))
            for env, marks in _get_available_interactive_backends()]

