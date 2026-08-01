
def _pad_extra_bos_eos_tokens(
    input_ids,
    attention_mask=None,
    pad_token_id=0,
    bos_token_id=255,
    eos_token_id=0,
    add_bos_token=True,
    add_eos_token=True,
):
    """
    This method adds extra bos and eos tokens to input_ids and accordingly modifies the attention_mask which is used in
    `ClvpConditioningEncoder` and the generation loop of the `ClvpModelForConditionalGeneration`.
    """

    # add the bos token at the beginning
    if add_bos_token:
        input_ids = torch.nn.functional.pad(input_ids, (1, 0), value=bos_token_id)
        attention_mask = (
            torch.nn.functional.pad(attention_mask, (1, 0), value=1) if attention_mask is not None else attention_mask
        )

    modified_input_ids = input_ids
    if add_eos_token:
        modified_input_ids = torch.zeros(
            (input_ids.shape[0], input_ids.shape[1] + 1), dtype=input_ids.dtype, device=input_ids.device
        )
        for i, each_input_id in enumerate(input_ids):
            # locate where the valid tokens end and then add the eos token
            if torch.isin(each_input_id, pad_token_id).sum():
                pos = torch.where(each_input_id == pad_token_id)[0].min()
                modified_input_ids[i] = torch.concatenate(
                    [each_input_id[:pos], torch.tensor([eos_token_id], device=input_ids.device), each_input_id[pos:]]
                )
            else:
                # if there are no pad tokens present, then add eos to the end
                modified_input_ids[i] = torch.nn.functional.pad(each_input_id, (0, 1), value=eos_token_id)
        attention_mask = (
            torch.nn.functional.pad(attention_mask, (1, 0), value=1) if attention_mask is not None else attention_mask
        )

    return modified_input_ids, attention_mask

