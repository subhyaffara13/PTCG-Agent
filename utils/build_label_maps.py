
def build_label_maps(logits: torch.FloatTensor, input_ids: torch.LongTensor) -> tuple[torch.FloatTensor]:
    """
    Computes a mapping between tokens and their corresponding labels, where `num_labels` is determined by the number of classes in the input prompt.
    The function identifies segments of tokens between specific delimiter tokens and generates label maps for those segments.
    Args:
        logits (`torch.Tensor` of shape `(batch_size, seq_length, hidden_size)`):
            The output logits from the model, where `hidden_size` corresponds to the dimension of the model's output features.

        input_ids (`torch.Tensor` of shape `(batch_size, seq_length)`):
            The input token IDs corresponding to the input prompt. For example, given the prompt "fish. shark.",
            `input_ids` might look like `[101, 3869, 1012, 11420, 1012, 102]` where each number corresponds to a token including special tokens.
    Returns:
        tuple: A tuple containing label maps for each instance in the batch.
        - label_maps (tuple of `torch.Tensor`):
            A tuple of tensors, where each tensor in the tuple corresponds to an instance in the batch. Each tensor
            has shape `(num_labels, hidden_size)` and contains binary values (0 or 1), where `1` indicates the tokens
            that are associated with a specific label (class) between delimiter tokens, and `0` elsewhere.
    Example:
        Given an input prompt "fish. shark." and corresponding `input_ids` as `[101, 3869, 1012, 11420, 1012, 102]`:
        - The function identifies the tokens for "fish" (IDs `[3869]`) and "shark" (IDs `[11420]`).
        - The function then constructs label maps for these tokens, where each label map indicates which tokens
          correspond to which label between the delimiter tokens (e.g., between the period `.`).
        - The output is a tuple of label maps, one for each instance in the batch.
    Note:
        - `SPECIAL_TOKENS` should be a predefined list of tokens that are considered special (e.g., `[CLS]`, `[SEP]`, etc.).
    """
    max_seq_len = logits.shape[-1]
    # Add [PAD] token to the list of special tokens
    delimiter_tokens = torch.tensor(SPECIAL_TOKENS + [0], device=input_ids.device)

    delimiter_token_masks = torch.isin(input_ids, delimiter_tokens)
    label_groups = torch.cumsum(delimiter_token_masks, dim=1) * (~delimiter_token_masks).to(torch.int32)

    label_maps = ()

    # Iterate over batch dimension as we can have different number of labels
    for label_group in label_groups:
        # `label_group` is a tensor of shape `(seq_len,)` with zeros for non-label tokens and integers for label tokens
        # label tokens with same integer value are part of the same label group

        # Get unique labels and exclude 0 (i.e. non-label tokens)
        unique_labels = torch.unique(label_group)[1:, None]
        num_labels = unique_labels.shape[0]

        # Create one-hot encoding for each label group
        label_map = label_group.unsqueeze(0).repeat(num_labels, 1)
        label_map = torch.where(label_map == unique_labels, 1, 0)

        # Pad label_map to match `max_seq_len`
        label_map = F.pad(label_map, (0, max_seq_len - label_map.shape[1]), value=0)

        label_maps += (label_map,)

    return label_maps


def build_label_maps(logits: torch.FloatTensor, input_ids: torch.LongTensor) -> tuple[torch.FloatTensor]:
    """
    Computes a mapping between tokens and their corresponding labels, where `num_labels` is determined by the number of classes in the input prompt.
    The function identifies segments of tokens between specific delimiter tokens and generates label maps for those segments.
    Args:
        logits (`torch.Tensor` of shape `(batch_size, seq_length, hidden_size)`):
            The output logits from the model, where `hidden_size` corresponds to the dimension of the model's output features.

        input_ids (`torch.Tensor` of shape `(batch_size, seq_length)`):
            The input token IDs corresponding to the input prompt. For example, given the prompt "fish. shark.",
            `input_ids` might look like `[101, 3869, 1012, 11420, 1012, 102]` where each number corresponds to a token including special tokens.
    Returns:
        tuple: A tuple containing label maps for each instance in the batch.
        - label_maps (tuple of `torch.Tensor`):
            A tuple of tensors, where each tensor in the tuple corresponds to an instance in the batch. Each tensor
            has shape `(num_labels, hidden_size)` and contains binary values (0 or 1), where `1` indicates the tokens
            that are associated with a specific label (class) between delimiter tokens, and `0` elsewhere.
    Example:
        Given an input prompt "fish. shark." and corresponding `input_ids` as `[101, 3869, 1012, 11420, 1012, 102]`:
        - The function identifies the tokens for "fish" (IDs `[3869]`) and "shark" (IDs `[11420]`).
        - The function then constructs label maps for these tokens, where each label map indicates which tokens
          correspond to which label between the delimiter tokens (e.g., between the period `.`).
        - The output is a tuple of label maps, one for each instance in the batch.
    Note:
        - `SPECIAL_TOKENS` should be a predefined list of tokens that are considered special (e.g., `[CLS]`, `[SEP]`, etc.).
    """
    max_seq_len = logits.shape[-1]
    # Add [PAD] token to the list of special tokens
    delimiter_tokens = torch.tensor(SPECIAL_TOKENS + [0], device=input_ids.device)

    delimiter_token_masks = torch.isin(input_ids, delimiter_tokens)
    label_groups = torch.cumsum(delimiter_token_masks, dim=1) * (~delimiter_token_masks).to(torch.int32)

    label_maps = ()

    # Iterate over batch dimension as we can have different number of labels
    for label_group in label_groups:
        # `label_group` is a tensor of shape `(seq_len,)` with zeros for non-label tokens and integers for label tokens
        # label tokens with same integer value are part of the same label group

        # Get unique labels and exclude 0 (i.e. non-label tokens)
        unique_labels = torch.unique(label_group)[1:, None]
        num_labels = unique_labels.shape[0]

        # Create one-hot encoding for each label group
        label_map = label_group.unsqueeze(0).repeat(num_labels, 1)
        label_map = torch.where(label_map == unique_labels, 1, 0)

        # Pad label_map to match `max_seq_len`
        label_map = F.pad(label_map, (0, max_seq_len - label_map.shape[1]), value=0)

        label_maps += (label_map,)

    return label_maps

