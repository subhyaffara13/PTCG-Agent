
def _has_gen_schema(op: HigherOrderOperator):
    # There is an InvokeQuant argument we cannot gen_schema.
    if op is torch.ops.higher_order.invoke_quant_packed:
        return False
    method = "gen_schema"
    return hasattr(type(op), method) and getattr(type(op), method) is not getattr(
        HigherOrderOperator, method
    )

