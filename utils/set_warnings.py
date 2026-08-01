
def set_warnings():
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message=r"Exited (at iteration \d+|postprocessing) with accuracies.*",
    )
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message=r"The hashes produced for ",
    )
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, message="\n\nThe `normalized`"
    )
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, message="maybe_regular_expander"
    )
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, message="metric_closure is deprecated"
    )

