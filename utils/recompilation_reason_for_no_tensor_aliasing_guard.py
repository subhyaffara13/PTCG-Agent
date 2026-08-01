
def recompilation_reason_for_no_tensor_aliasing_guard(
    guard_manager: GuardManagerWrapper, scope: Scope
) -> list[str]:
    assert guard_manager.global_scope is not None
    global_scope = dict(guard_manager.global_scope)
    ids_to_source = collections.defaultdict(list)
    for tensor_source in guard_manager.no_tensor_aliasing_sources:
        global_scope["__compile_source__"] = tensor_source
        tensor_id = id(eval(tensor_source, global_scope, scope))
        ids_to_source[tensor_id].append(tensor_source)

    duplicate_tensors = [
        f"{ids_to_source[key]}" for key in ids_to_source if len(ids_to_source[key]) > 1
    ]

    reason = ", ".join(duplicate_tensors)
    return [f"Duplicate tensors found: {reason}"]

