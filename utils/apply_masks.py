
def apply_masks(tensor: torch.Tensor, masks: list[torch.Tensor]) -> torch.Tensor:
    """
    Args:
        tensor (`torch.Tensor`):
            Tensor of shape [batch_size, num_patches, feature_dim]
        masks (`List[torch.Tensor]`):
            List of tensors of shape [batch_size, num_patches] containing indices of patches to keep
    """
    all_masked_tensors = []
    for mask in masks:
        mask = mask.to(tensor.device)
        mask_keep = mask.unsqueeze(-1).repeat(1, 1, tensor.size(-1))
        all_masked_tensors += [torch.gather(tensor, dim=1, index=mask_keep)]

    return torch.cat(all_masked_tensors, dim=0)

