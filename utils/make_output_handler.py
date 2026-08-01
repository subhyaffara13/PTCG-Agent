
def make_output_handler(
    info: Any, runtime_metadata: ViewAndMutationMeta, trace_joint: bool
) -> Any:
    handler_type = _HANDLER_MAP[info.output_type]
    return handler_type(info, runtime_metadata, trace_joint)

