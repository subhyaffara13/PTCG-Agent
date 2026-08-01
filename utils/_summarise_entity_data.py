
def _summarise_entity_data(data: Dict[str, Any], entity_label: str) -> str:
    """Summarise team/tag entity usage data."""
    results = data.get("results", [])
    if not results:
        return f"No {entity_label} usage data found for the given date range."

    totals: Dict[str, Dict[str, Any]] = {}
    for day in results:
        for eid, entry in day.get("breakdown", {}).get("entities", {}).items():
            if eid not in totals:
                alias = entry.get("metadata", {}).get("alias", eid)
                totals[eid] = {"alias": alias, "spend": 0.0, "requests": 0, "tokens": 0}
            m = entry.get("metrics", {})
            totals[eid]["spend"] += m.get("spend", 0)
            totals[eid]["requests"] += m.get("api_requests", 0)
            totals[eid]["tokens"] += m.get("total_tokens", 0)

    lines = [f"{entity_label} Usage ({len(totals)} {entity_label.lower()}s):", ""]
    for eid, d in sorted(totals.items(), key=lambda x: -x[1]["spend"]):
        label = d["alias"] if d["alias"] != eid else eid
        lines.append(
            f"- {label} (ID: {eid}): ${d['spend']:.4f} | "
            f"{int(d['requests'])} reqs | {int(d['tokens'])} tokens"
        )
    return "\n".join(lines)

