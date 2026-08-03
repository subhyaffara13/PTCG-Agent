from typing import Any

def maybe_sequence_to_range(sequence) -> Any | range:
    """
    Convert a 1D, non-pandas sequence to a range if possible.

    Returns the input if not possible.

    Parameters
    ----------
    sequence : 1D sequence
    names : sequence of str

    Returns
    -------
    Any : input or range
    """
    if isinstance(sequence, (range, ExtensionArray)):
        return sequence
    elif len(sequence) == 1 or lib.infer_dtype(sequence, skipna=False) != "integer":
        return sequence
    elif isinstance(sequence, (ABCSeries, Index)) and not (
        isinstance(sequence.dtype, np.dtype) and sequence.dtype.kind == "i"
    ):
        return sequence
    if len(sequence) == 0:
        return range(0)
    try:
        np_sequence = np.asarray(sequence, dtype=np.int64)
    except OverflowError:
        return sequence
    diff = np_sequence[1] - np_sequence[0]
    if diff == 0:
        return sequence
    elif len(sequence) == 2 or lib.is_sequence_range(np_sequence, diff):
        return range(np_sequence[0], np_sequence[-1] + diff, diff)
    else:
        return sequence

