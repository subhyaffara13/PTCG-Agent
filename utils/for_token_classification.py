
def ForTokenClassification(logits: torch.Tensor, labels, config, **kwargs):
    # Upcast to float if we need to compute the loss to avoid potential precision issues
    logits = logits.view(-1, config.num_labels)
    labels = labels.view(-1).to(logits.device)
    logits = logits.float()
    # Flatten the tokens
    return fixed_cross_entropy(logits, labels, **kwargs)

