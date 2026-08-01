
def get_common_xfix(series: Any, xfix: str = "suffix") -> str:
    """
    Finds the longest common suffix or prefix of all the values in a series
    """
    common_xfix = ""
    while True:
        common_xfixes = (
            series.str[-(len(common_xfix) + 1) :] if xfix == "suffix" else series.str[: len(common_xfix) + 1]
        )  # first few or last few characters
        if common_xfixes.nunique() != 1:  # we found the character at which we don't have a unique xfix anymore
            break
        elif common_xfix == common_xfixes.values[0]:  # the entire first row is a prefix of every other row
            break
        else:  # the first or last few characters are still common across all rows - let's try to add one more
            common_xfix = common_xfixes.values[0]
    return common_xfix

