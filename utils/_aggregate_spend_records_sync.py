
def _aggregate_spend_records_sync(
    *,
    records: List[Any],
    api_key_metadata: Dict[str, Dict[str, Any]],
    entity_id_field: Optional[str],
    entity_metadata_field: Optional[Dict[str, dict]],
) -> Dict[str, Any]:
    model_metadata: Dict[str, Dict[str, Any]] = {}
    provider_metadata: Dict[str, Dict[str, Any]] = {}

    results: List[DailySpendData] = []
    total_metrics = SpendMetrics()
    grouped_data: Dict[str, Dict[str, Any]] = {}

    for record in records:
        date_str = record.date
        if date_str not in grouped_data:
            grouped_data[date_str] = {
                "metrics": SpendMetrics(),
                "breakdown": BreakdownMetrics(),
            }

        grouped_data[date_str]["metrics"] = update_metrics(
            grouped_data[date_str]["metrics"], record
        )

        grouped_data[date_str]["breakdown"] = update_breakdown_metrics(
            grouped_data[date_str]["breakdown"],
            record,
            model_metadata,
            provider_metadata,
            api_key_metadata,
            entity_id_field=entity_id_field,
            entity_metadata_field=entity_metadata_field,
        )

        total_metrics = update_metrics(total_metrics, record)

    for date_str, data in grouped_data.items():
        results.append(
            DailySpendData(
                date=datetime.strptime(date_str, "%Y-%m-%d").date(),
                metrics=data["metrics"],
                breakdown=data["breakdown"],
            )
        )

    results.sort(key=lambda x: x.date, reverse=True)

    return {"results": results, "totals": total_metrics}

