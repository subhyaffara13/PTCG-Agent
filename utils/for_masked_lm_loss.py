
def ForMaskedLMLoss(
    logits: torch.Tensor,
    labels: torch.Tensor,
    vocab_size: int,
    num_items_in_batch: torch.Tensor | None = None,
    ignore_index: int = -100,
    **kwargs,
):
    # Upcast to float if we need to compute the loss to avoid potential precision issues
    logits = logits.float()

    # Flatten the tokens
    logits = logits.view(-1, vocab_size)
    labels = labels.view(-1)

    labels = labels.to(logits.device)
    loss = fixed_cross_entropy(logits, labels, num_items_in_batch, ignore_index, **kwargs)
    return loss

