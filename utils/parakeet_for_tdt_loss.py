
def ParakeetForTDTLoss(
    token_logits,
    duration_logits,
    labels,
    logit_lengths,
    label_lengths,
    blank_token_id,
    durations,
    sigma=0.0,
    reduction="mean",
    **kwargs,
):
    device = token_logits.device
    return tdt_loss(
        token_logits=token_logits,
        duration_logits=duration_logits,
        targets=labels.to(device).int(),
        logit_lengths=logit_lengths.to(device).int(),
        target_lengths=label_lengths.to(device).int(),
        blank_token_id=blank_token_id,
        durations=durations,
        sigma=sigma,
        reduction=reduction,
    )

