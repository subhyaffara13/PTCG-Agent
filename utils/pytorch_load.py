
def pytorch_load(context):
    """
    This plugin checks for unsafe use of `torch.load` and
    `torch.serialization.load`. Using `torch.load` or
    `torch.serialization.load` with untrusted data can lead to
    arbitrary code execution. The safe alternative is to use
    `weights_only=True` or the safetensors library.
    """
    imported = context.is_module_imported_exact("torch")
    qualname = context.call_function_name_qual
    if not imported and isinstance(qualname, str):
        return

    if qualname in {"torch.load", "torch.serialization.load"}:
        # For torch.load, check if weights_only=True is specified
        weights_only = context.get_call_arg_value("weights_only")
        if weights_only == "True" or weights_only is True:
            return

        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.HIGH,
            text="Use of unsafe PyTorch load",
            cwe=issue.Cwe.DESERIALIZATION_OF_UNTRUSTED_DATA,
            lineno=context.get_lineno_for_call_arg("load"),
        )

