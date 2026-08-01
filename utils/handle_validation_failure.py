
def handle_validation_failure(report: dict, check_num: int, reason: str, log_file: Path) -> dict:
    report.update({"all_passed": False, "promoted": False, "failed_check": f"check_{check_num}", "reason": reason})
    check_mapping = {
        1: "syntax", 2: "base_inheritance", 3: "receive_method", 4: "router_boundaries",
        5: "no_auto_submit", 6: "no_api_keys", 7: "time_compliance", 8: "score_improvement",
        9: "staging_integrity"
    }
    name = check_mapping.get(check_num)
    if name: report["checks"][name] = "fail"
    write_validation_log(report, log_file)
    return report

