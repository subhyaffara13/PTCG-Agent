
def get_safe_global_name(tx: InstructionTranslatorBase, root: str, obj: Any) -> str:
    # The global_mangled_class_name should be different for different
    # invocations of torch.compile. Otherwise, we can run into a situation
    # where multiple torch.compile invocations reuse the same global name,
    # but the global's lifetime is tied to the first invocation (and
    # may be deleted when the first torch.compile invocation is deleted)
    # We mangle it based off of the output_graph's id.
    return f"{root}_{id(obj)}_c{tx.output.compile_id}"

