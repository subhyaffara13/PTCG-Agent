
def _where_standard(cond, left_op, right_op):
    # Caller is responsible for extracting ndarray if necessary
    return np.where(cond, left_op, right_op)

