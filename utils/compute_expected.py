
def compute_expected(df_left, df_right, on=None, left_on=None, right_on=None, how=None):
    """
    Compute the expected merge result for the test case.

    This method computes the expected result of merging two DataFrames on
    a combination of their columns and index levels. It does so by
    explicitly dropping/resetting their named index levels, performing a
    merge on their columns, and then finally restoring the appropriate
    index in the result.

    Parameters
    ----------
    df_left : DataFrame
        The left DataFrame (may have zero or more named index levels)
    df_right : DataFrame
        The right DataFrame (may have zero or more named index levels)
    on : list of str
        The on parameter to the merge operation
    left_on : list of str
        The left_on parameter to the merge operation
    right_on : list of str
        The right_on parameter to the merge operation
    how : str
        The how parameter to the merge operation

    Returns
    -------
    DataFrame
        The expected merge result
    """
    # Handle on param if specified
    if on is not None:
        left_on, right_on = on, on

    # Compute input named index levels
    left_levels = [n for n in df_left.index.names if n is not None]
    right_levels = [n for n in df_right.index.names if n is not None]

    # Compute output named index levels
    output_levels = [i for i in left_on if i in right_levels and i in left_levels]

    # Drop index levels that aren't involved in the merge
    drop_left = [n for n in left_levels if n not in left_on]
    if drop_left:
        df_left = df_left.reset_index(drop_left, drop=True)

    drop_right = [n for n in right_levels if n not in right_on]
    if drop_right:
        df_right = df_right.reset_index(drop_right, drop=True)

    # Convert remaining index levels to columns
    reset_left = [n for n in left_levels if n in left_on]
    if reset_left:
        df_left = df_left.reset_index(level=reset_left)

    reset_right = [n for n in right_levels if n in right_on]
    if reset_right:
        df_right = df_right.reset_index(level=reset_right)

    # Perform merge
    expected = df_left.merge(df_right, left_on=left_on, right_on=right_on, how=how)

    # Restore index levels
    if output_levels:
        expected = expected.set_index(output_levels)

    return expected

