
def get_permutation(items: List, seed: int) -> List:
    """
    Generates a deterministic permutation of a list based on a seed.

    This function implements a Fisher-Yates shuffle using a simple Linear
    Congruential Generator (LCG) for pseudo-random number generation. This
    ensures that the permutation is reproducible across different platforms
    and languages, as it does not depend on Python's built-in 'random' module.

    The LCG parameters (m, a, c) are chosen from the glibc standard for
    broad compatibility.

    Args:
        items: The list of items to be permuted.
        seed: An integer used to initialize the random number generator.

    Returns:
        A new list containing the items in a permuted order.
    """
    # LCG parameters (from glibc)
    m = 2**31
    a = 1103515245
    c = 12345

    # Make a copy to avoid modifying the original list
    shuffled_items = list(items)
    n = len(shuffled_items)

    current_seed = seed

    for i in range(n - 1, 0, -1):
        # Generate a pseudo-random number
        current_seed = (a * current_seed + c) % m

        # Get an index j such that 0 <= j <= i
        j = current_seed % (i + 1)

        # Swap elements
        shuffled_items[i], shuffled_items[j] = shuffled_items[j], shuffled_items[i]

    return shuffled_items

