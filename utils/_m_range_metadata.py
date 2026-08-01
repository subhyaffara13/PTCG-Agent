
def _m_range_metadata(aggregation_type=None):
    if aggregation_type is None:
        # Aggregators are empty when TS.MRANGE/TS.MREVRANGE is called without
        # AGGREGATION; this mirrors RESP3 metadata such as {"aggregators": []}.
        return {"aggregators": []}
    if isinstance(aggregation_type, list):
        aggregators = aggregation_type
    else:
        aggregators = [aggregation_type]
    return {"aggregators": [nativestr(agg).lower() for agg in aggregators]}

