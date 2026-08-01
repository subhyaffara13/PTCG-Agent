
def iris(datapath) -> DataFrame:
    """
    The iris dataset as a DataFrame.
    """
    return read_csv(datapath("io", "data", "csv", "iris.csv"))

