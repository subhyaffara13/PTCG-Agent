
def source_code_location(event: _ProfilerEvent | None) -> str:
    while event:
        if event.tag == _EventType.PyCall or event.tag == _EventType.PyCCall:
            if not isinstance(
                event.extra_fields, (_ExtraFields_PyCall, _ExtraFields_PyCCall)
            ):
                raise AssertionError(
                    f"expected _ExtraFields_PyCall or _ExtraFields_PyCCall, "
                    f"got {type(event.extra_fields).__name__}"
                )
            if not event.extra_fields.caller.file_name.startswith("torch" + os.sep):
                return f"{event.extra_fields.caller.file_name}:{event.extra_fields.caller.line_number}"
        event = event.parent
    return "No source code location found"


def source_code_location(event):
    while event is not None:
        match = re.search(r"\.py\(.*\)", event.name)
        if match is None:
            event = event.parent
            continue
        return event.name
    return "No source code location found"

