
def _get_failed_batched_grad_test_msg(
    output_idx, input_idx, res, exp, is_forward_ad=False
):
    return f"""
For output {output_idx} and input {input_idx}:

{FAILED_BATCHED_GRAD_MSG_FWD_AD if is_forward_ad else FAILED_BATCHED_GRAD_MSG}

Got:
{res}

Expected:
{exp}
""".strip()

