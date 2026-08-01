
def set_feature_use(feature: str, usage: bool) -> None:
    """
    Records whether we are using a feature
    Generally a feature is a JK.
    """
    # Note that sometimes (tests etc...) we're not in a context which we can record into
    if get_metrics_context().in_progress():
        get_metrics_context().set_key_value("feature_usage", feature, usage)

