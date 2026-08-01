
def ForSemanticSegmentationLoss(
    logits: torch.Tensor,
    labels: torch.Tensor,
    ignore_index: int = 255,
    num_items_in_batch: torch.Tensor | None = None,
    auxiliary_logits: torch.Tensor | None = None,
    auxiliary_loss_weight: float = 0.4,
    **kwargs,
) -> torch.Tensor:
    upsampled_logits = nn.functional.interpolate(logits, size=labels.shape[-2:], mode="bilinear", align_corners=False)
    loss = fixed_cross_entropy(
        upsampled_logits, labels, num_items_in_batch=num_items_in_batch, ignore_index=ignore_index
    )
    if auxiliary_logits is not None:
        upsampled_auxiliary_logits = nn.functional.interpolate(
            auxiliary_logits, size=labels.shape[-2:], mode="bilinear", align_corners=False
        )
        loss = loss + auxiliary_loss_weight * fixed_cross_entropy(
            upsampled_auxiliary_logits, labels, num_items_in_batch=num_items_in_batch, ignore_index=ignore_index
        )
    return loss

