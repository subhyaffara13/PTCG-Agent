
def _collect_all_valid_cia_ops_for_aten_namespace() -> set["OperatorBase"]:
    return _collect_all_valid_cia_ops_for_namespace(torch.ops.aten)

