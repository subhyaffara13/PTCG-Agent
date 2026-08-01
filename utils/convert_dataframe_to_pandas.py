
def convert_dataframe_to_pandas(data: object) -> pd.DataFrame:
    """Use the DataFrame exchange protocol, or fail gracefully."""
    if isinstance(data, pd.DataFrame):
        return data

    if not hasattr(pd.api, "interchange"):
        msg = (
            "Support for non-pandas DataFrame objects requires a version of pandas "
            "that implements the DataFrame interchange protocol. Please upgrade "
            "your pandas version or coerce your data to pandas before passing "
            "it to seaborn."
        )
        raise TypeError(msg)

    if _version_predates(pd, "2.0.2"):
        msg = (
            "DataFrame interchange with pandas<2.0.2 has some known issues. "
            f"You are using pandas {pd.__version__}. "
            "Continuing, but it is recommended to carefully inspect the results and to "
            "consider upgrading."
        )
        warnings.warn(msg, stacklevel=2)

    try:
        # This is going to convert all columns in the input dataframe, even though
        # we may only need one or two of them. It would be more efficient to select
        # the columns that are going to be used in the plot prior to interchange.
        # Solving that in general is a hard problem, especially with the objects
        # interface where variables passed in Plot() may only be referenced later
        # in Plot.add(). But noting here in case this seems to be a bottleneck.
        return pd.api.interchange.from_dataframe(data)
    except Exception as err:
        msg = (
            "Encountered an exception when converting data source "
            "to a pandas DataFrame. See traceback above for details."
        )
        raise RuntimeError(msg) from err

