
def _parse_bar(observation: str) -> dict[str, int]:
    for line in observation.splitlines():
        if line.startswith("Bar:"):
            payload = line[len("Bar:") :]
            return {_X: payload.count(_X), _O: payload.count(_O)}
    return {_X: 0, _O: 0}

