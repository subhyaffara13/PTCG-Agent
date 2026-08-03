from typing import Any, Dict, List

def compute_size_by_dict(indices: Iterable[int], idx_dict: List[int]) -> int: ...


def compute_size_by_dict(indices: Collection[str], idx_dict: Dict[str, int]) -> int: ...


def compute_size_by_dict(indices: Any, idx_dict: Any) -> int:
    """Computes the product of the elements in indices based on the dictionary
    idx_dict.

    Parameters
    ----------
    indices : iterable
        Indices to base the product on.
    idx_dict : dictionary
        Dictionary of index _sizes

    Returns:
    -------
    ret : int
        The resulting product.

    Examples:
    --------
    >>> compute_size_by_dict('abbc', {'a': 2, 'b':3, 'c':5})
    90

    """
    ret = 1
    for i in indices:  # lgtm [py/iteration-string-and-sequence]
        ret *= idx_dict[i]
    return ret

