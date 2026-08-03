from typing import Any, Callable

def _reduce_multidim_lists(
    lists_to_reduce: list[Any], reduce_func: Callable[[list[Any]], Any]
) -> Any:
    """
    Reduces a list of multi-dimensional lists, assuming they all have
    the exact same shape.

    Args:
        lists_to_reduce (list): A list where each item is a multi-dimensional
                                list (e.g., [md_list_1, md_list_2, ...]).
                                All inner md_lists must have the same shape.
        reduce_func (callable): A function that takes an iterable (list) of
                                values and returns a single reduced value.
                                For example: sum, max, min, or
                                lambda x: sum(x) / len(x) for mean.

    Returns:
        A single multi-dimensional list of the same shape as the inputs,
        where each value is the result of the reduce_func.

    Raises:
        ValueError: If the input list is empty or if shapes are inconsistent
                    (which may also raise IndexError or TypeError).
    """
    if not lists_to_reduce:
        raise ValueError("Input 'lists_to_reduce' cannot be empty.")

    # Get the first list to inspect its structure (shape)
    first_list = lists_to_reduce[0]

    # Check if the first element of this list is *also* a list.
    # This determines if we are at the base case or need to recurse.
    if isinstance(first_list[0], list):
        # --- RECURSIVE STEP ---
        # The elements are lists, so we need to go one level deeper.

        # We find the number of sub-lists from the first list.
        # (e.g., for [[1,2], [3,4]], this is 2)
        num_sublists = len(first_list)

        result = []
        # Iterate by the index of the sub-lists (e.g., i = 0, then i = 1)
        for i in range(num_sublists):
            # Build a new list to pass to the recursive call.
            # This list will contain the i-th sublist from *each* of the
            # input lists.
            # e.g., if lists_to_reduce = [ L1, L2 ] and i = 0,
            # this creates [ L1[0], L2[0] ]
            sublists_to_reduce = [l[i] for l in lists_to_reduce]

            # Recurse and append the result
            result.append(_reduce_multidim_lists(sublists_to_reduce, reduce_func))
        return result
    else:
        # --- BASE CASE ---
        # The elements are values (int, float, etc.), not lists.
        # We are at the innermost dimension.

        # Find the number of values in the innermost list.
        # (e.g., for [1, 2], this is 2)
        num_values = len(first_list)

        result = []
        # Iterate by the index of the values (e.g., i = 0, then i = 1)
        for i in range(num_values):
            # Get the values at this specific position (i) from *all*
            # input lists.
            # e.g., if lists_to_reduce = [ [1,2], [10,20] ] and i = 0,
            # this creates [ 1, 10 ]
            values_at_pos = [l[i] for l in lists_to_reduce]

            # Apply the user-provided reduction function to this list of values
            # and append the single result.
            result.append(reduce_func(values_at_pos))
        return result

