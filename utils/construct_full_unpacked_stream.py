
def construct_full_unpacked_stream(
    num_real_text_tokens: Union[list[list[int]], "torch.Tensor"],
    input_stream: "torch.Tensor",
    image_tokens: list[list["torch.Tensor"]],
    batch_size: int,
    num_sub_sequences: int,
) -> list["torch.Tensor"]:
    """Takes an input_stream tensor of shape B x S x ?. For each subsequence, adds any required
    padding to account for images and then unpacks the subsequences to create a single sequence per item in the batch.
    Returns a list of tensors, one for each item in the batch."""

    all_bi_stream = []

    for batch_index in range(batch_size):
        all_si_stream = []

        # First, construct full token stream (including image placeholder tokens) and loss mask for each subsequence
        # and append to lists. We use lists rather than tensors because each subsequence is variable-sized.
        # TODO Remove this logic in a subsequent release since subsequences are not supported.
        image_adjustment = image_tokens[batch_index][0]
        subsequence_stream = torch.cat([image_adjustment, input_stream[batch_index, 0]], dim=0)
        num_real_tokens = image_adjustment.shape[0] + num_real_text_tokens[batch_index][0]
        all_si_stream.append(subsequence_stream[:num_real_tokens])
        all_bi_stream.append(torch.cat(all_si_stream, dim=0))

    return all_bi_stream

