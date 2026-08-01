
def _get_rolling_aggregations():
    # list pairs of name and function
    # each function has this signature:
    # (const float64_t[:] values, ndarray[int64_t] start,
    #  ndarray[int64_t] end, int64_t minp) -> np.ndarray
    named_roll_aggs = (
        [
            ("roll_sum", window_aggregations.roll_sum),
            ("roll_mean", window_aggregations.roll_mean),
        ]
        + [
            (f"roll_var({ddof})", partial(window_aggregations.roll_var, ddof=ddof))
            for ddof in [0, 1]
        ]
        + [
            ("roll_skew", window_aggregations.roll_skew),
            ("roll_kurt", window_aggregations.roll_kurt),
            ("roll_median_c", window_aggregations.roll_median_c),
            ("roll_max", window_aggregations.roll_max),
            ("roll_min", window_aggregations.roll_min),
            ("roll_first", window_aggregations.roll_first),
            ("roll_last", window_aggregations.roll_last),
            ("roll_nunique", window_aggregations.roll_nunique),
        ]
        + [
            (
                f"roll_quantile({quantile},{interpolation})",
                partial(
                    window_aggregations.roll_quantile,
                    quantile=quantile,
                    interpolation=interpolation,
                ),
            )
            for quantile in [0.0001, 0.5, 0.9999]
            for interpolation in window_aggregations.interpolation_types
        ]
        + [
            (
                f"roll_rank({percentile},{method},{ascending})",
                partial(
                    window_aggregations.roll_rank,
                    percentile=percentile,
                    method=method,
                    ascending=ascending,
                ),
            )
            for percentile in [True, False]
            for method in window_aggregations.rolling_rank_tiebreakers.keys()
            for ascending in [True, False]
        ]
    )
    # unzip to a list of 2 tuples, names and functions
    unzipped = list(zip(*named_roll_aggs, strict=True))
    return {"ids": unzipped[0], "params": unzipped[1]}

