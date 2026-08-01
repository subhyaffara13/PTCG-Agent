
def incremental_to_binary_attention_mask(incremental_mask, return_tensors, num_classes=-1):
    # Set elements >= num_classes to -1
    if num_classes != -1:
        if return_tensors == "pt":
            incremental_mask[incremental_mask >= num_classes] = -1

    # Create mask for negative values
    if return_tensors == "pt":
        negatives = incremental_mask == -1
        incremental_mask[negatives] = 0
        attn_mask = torch.nn.functional.one_hot(incremental_mask, num_classes=num_classes)
        attn_mask[negatives, :] = 0

    return attn_mask

