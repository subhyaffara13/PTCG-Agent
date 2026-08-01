
def ParakeetForRNNTLoss(
    logits,
    labels,
    logit_lengths,
    label_lengths,
    blank_token_id,
    reduction="mean_volume",
    **kwargs,
):
    return rnnt_loss(
        logits=logits,
        targets=labels,
        logit_lengths=logit_lengths,
        target_lengths=label_lengths,
        blank_token_id=blank_token_id,
        reduction=reduction,
    )

