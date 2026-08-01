
def call_prepare_scriptable_func(obj):
    memo: dict[int, torch.nn.Module] = {}
    return call_prepare_scriptable_func_impl(obj, memo)

