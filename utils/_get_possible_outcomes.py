import math


def _get_possible_outcomes(m, bits):
    """Get the possible states that can be produced in a measurement.

    Parameters
    ----------
    m : Matrix
        The matrix representing the state of the system.
    bits : tuple, list
        Which bits will be measured.

    Returns
    -------
    result : list
        The list of possible states which can occur given this measurement.
        These are un-normalized so we can derive the probability of finding
        this state by taking the inner product with itself
    """

    # This is filled with loads of dirty binary tricks...You have been warned

    size = max(m.shape)  # Max of shape to account for bra or ket
    nqubits = int(math.log2(size) + .1)  # Number of qubits possible

    # Make the output states and put in output_matrices, nothing in them now.
    # Each state will represent a possible outcome of the measurement
    # Thus, output_matrices[0] is the matrix which we get when all measured
    # bits return 0. and output_matrices[1] is the matrix for only the 0th
    # bit being true
    output_matrices = []
    for i in range(1 << len(bits)):
        output_matrices.append(zeros(2**nqubits, 1))

    # Bitmasks will help sort how to determine possible outcomes.
    # When the bit mask is and-ed with a matrix-index,
    # it will determine which state that index belongs to
    bit_masks = []
    for bit in bits:
        bit_masks.append(1 << bit)

    # Make possible outcome states
    for i in range(2**nqubits):
        trueness = 0  # This tells us to which output_matrix this value belongs
        # Find trueness
        for j in range(len(bit_masks)):
            if i & bit_masks[j]:
                trueness += j + 1
        # Put the value in the correct output matrix
        output_matrices[trueness][i] = m[i]
    return output_matrices

