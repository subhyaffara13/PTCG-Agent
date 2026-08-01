
def _set_stance(stance: DynamoStance) -> DynamoStance:
    global _stance

    from torch._C._dynamo.eval_frame import get_eval_frame_callback

    callback = get_eval_frame_callback()

    if callback is not False and callback is not None:
        raise RuntimeError("attempted to set_stance in a torch.compile region")

    prior = _stance
    _stance = stance
    return prior

