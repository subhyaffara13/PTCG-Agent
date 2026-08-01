
def _chart_from_metrics(metrics: Any) -> List[Dict[str, Any]]:
    chart_by_date: Dict[str, Dict[str, int]] = {}
    for m in metrics:
        d = m.date
        if d not in chart_by_date:
            chart_by_date[d] = {"passed": 0, "blocked": 0}
        chart_by_date[d]["passed"] += int(m.passed_count or 0)
        chart_by_date[d]["blocked"] += int(m.blocked_count or 0)
    return [
        {"date": d, "passed": v["passed"], "blocked": v["blocked"]}
        for d, v in sorted(chart_by_date.items())
    ]

