
def reduce_graph_module(body: dict[Any, Any], import_block: str) -> torch.nn.Module:
    # BC: attribute name was changed from `code` to `_code` to facilitate
    # making `code` into a property and adding a docstring to it
    fn_src = body.get("_code") or body["code"]
    forward = _forward_from_src(import_block + fn_src, {})
    return _deserialize_graph_module(forward, body)

