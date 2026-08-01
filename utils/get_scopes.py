
def get_scopes(event: _ProfilerEvent | None) -> tuple[RecordScope, ...]:
    scopes = []
    while event:
        if event.typed[0] == _EventType.TorchOp:
            scopes.append(event.typed[1].scope)
        event = event.parent
    return tuple(scopes)

