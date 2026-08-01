
def pad_sequence(seq, target_len, pad_value=0):
    if isinstance(seq, torch.Tensor):
        n = seq.shape[0]
    else:
        n = len(seq)
        seq = torch.tensor(seq)
    m = target_len - n
    if m > 0:
        ret = torch.stack([pad_value] * m).to(seq)
        seq = torch.cat([seq, ret], dim=0)
    return seq[:target_len]


def pad_sequence(sequences, batch_first=False, padding_value=0.0):
    torch._check(len(sequences) > 0, lambda: "received an empty list of sequences")
    sequences_size = len(sequences)
    max_size = sequences[0].size()
    trailing_dims = max_size[1:]
    max_len = max(x.size(0) for x in sequences)
    if batch_first:
        out_dims = (sequences_size, max_len)
    else:
        out_dims = (max_len, sequences_size)
    out_dims = out_dims + trailing_dims
    out = sequences[0].new_full(out_dims, padding_value)
    dim_paddings = (0, 0) * len(trailing_dims)
    for i in range(sequences_size):
        currseq = sequences[i]
        row = aten.constant_pad_nd(
            currseq, dim_paddings + (0, max_len - currseq.size(0)), padding_value
        )
        if batch_first:
            out = aten.select_scatter(out, row, dim=0, index=i)
        else:
            out = aten.select_scatter(out, row, dim=1, index=i)
    return out


def pad_sequence(
    sequences: Tensor | list[Tensor],
    batch_first: bool = False,
    padding_value: float = 0.0,
    padding_side: str = "right",
) -> Tensor:
    r"""Pad a list of variable length Tensors with :attr:`padding_value`.

    ``pad_sequence`` stacks a list of Tensors along a new dimension, and pads them
    to equal length. :attr:`sequences` can be list of sequences with size ``L x *``,
    where `L` is length of the sequence and ``*`` is any number of dimensions
    (including ``0``). If :attr:`batch_first` is ``False``, the output is of size
    ``T x B x *``, and ``B x T x *`` otherwise, where ``B`` is the batch size
    (the number of elements in :attr:`sequences`), ``T`` is the length of the longest
    sequence.

    Example:
        >>> from torch.nn.utils.rnn import pad_sequence
        >>> a = torch.ones(25, 300)
        >>> b = torch.ones(22, 300)
        >>> c = torch.ones(15, 300)
        >>> pad_sequence([a, b, c]).size()
        torch.Size([25, 3, 300])

    Note:
        This function returns a Tensor of size ``T x B x *`` or ``B x T x *``
        where `T` is the length of the longest sequence. This function assumes
        trailing dimensions and type of all the Tensors in sequences are same.

    Args:
        sequences (list[Tensor]): list of variable length sequences.
        batch_first (bool, optional): if ``True``, the output will be in ``B x T x *``
            format, ``T x B x *`` otherwise.
        padding_value (float, optional): value for padded elements. Default: ``0``.
        padding_side (str, optional): the side to pad the sequences on.
            Default: ``'right'``.

    Returns:
        Tensor of size ``T x B x *`` if :attr:`batch_first` is ``False``.
        Tensor of size ``B x T x *`` otherwise
    """
    if not (torch.jit.is_tracing() or torch.jit.is_scripting()):
        # JIT doesn't support `Iterable`
        if not isinstance(sequences, Iterable):
            msg = (
                "pad_sequence: Expected iterable for input sequences, but got arg of type: "
                f"{type(sequences)}"
            )
            raise RuntimeError(msg)

        # In JIT context this leads to,
        # RuntimeError: cannot statically infer the expected size of a list in this context
        sequences = tuple(sequences)  # type: ignore[assignment]
    else:
        # For JIT, we only support Union[Tensor, Tuple[Tensor]]
        if isinstance(sequences, torch.Tensor):
            sequences = sequences.unbind(0)  # type: ignore[assignment]

    # assuming trailing dimensions and type of all the Tensors
    # in sequences are same and fetching those from sequences[0]
    return torch._C._nn.pad_sequence(
        sequences,  # type: ignore[arg-type]
        batch_first,
        padding_value,
        padding_side,  # type: ignore[arg-type]
    )

