
def build_text_mask(logits, attention_mask):
    """
    Create text_mask based on the matching indices
    """
    seq_len = attention_mask.shape[1]
    text_mask = torch.zeros_like(logits, device=logits.device, dtype=attention_mask.dtype)
    text_mask[:, :, :seq_len] = attention_mask[:, None, :]

    return text_mask.bool()


def build_text_mask(logits, attention_mask):
    """
    Create text_mask based on the matching indices
    """
    seq_len = attention_mask.shape[1]
    text_mask = torch.zeros_like(logits, device=logits.device, dtype=attention_mask.dtype)
    text_mask[:, :, :seq_len] = attention_mask[:, None, :]

    return text_mask.bool()

