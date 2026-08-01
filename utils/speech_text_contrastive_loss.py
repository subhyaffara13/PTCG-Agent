
def speech_text_contrastive_loss(similarity: torch.Tensor) -> torch.Tensor:
    caption_loss = contrastive_loss(similarity)
    speech_loss = contrastive_loss(similarity.T)
    return (caption_loss + speech_loss) / 2.0

