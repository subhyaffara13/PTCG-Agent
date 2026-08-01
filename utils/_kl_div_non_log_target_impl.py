
def _kl_div_non_log_target_impl(g: jit_utils.GraphContext, input, target):
    log_ = log(g, target)
    diff_ = sub(g, log_, input)
    output_pos = mul(g, target, diff_)
    zeros_ = zeros_like(g, output_pos)
    mask_ = gt(g, target, g.op("Constant", value_t=torch.tensor(0)))
    output = where(g, mask_, output_pos, zeros_)
    return output

