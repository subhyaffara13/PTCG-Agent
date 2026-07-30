def _build_validate_report(staged_path, timestamp, version_id, checks):
    return {"version_id": version_id, "timestamp": timestamp, "staged_file": str(staged_path),
            "checks": checks, "all_passed": False, "promoted": False,
            "failed_check": None, "reason": None}

def _do_promote_and_log(report, history_file, validation_log_file, new_score, baseline_score, staged_path, factory_dir, agents_dir, version_id, timestamp, eval_report):
    import shutil
    from factory.validator_helpers import append_to_history, write_validation_log
    is_factory = any(x in staged_path.name for x in ["logger", "runner", "eval", "improvement", "builder", "validator"])
    try:
        shutil.copy2(staged_path, (factory_dir if is_factory else agents_dir) / staged_path.name)
    except Exception as e: return None
    report.update({"all_passed": True, "promoted": True})
    new_baseline = new_score
    append_to_history(history_file, {"version_id": version_id, "timestamp": timestamp,
        "staged_file": str(staged_path), "version_score": new_score,
        "improvement_vs_baseline": round(new_score - baseline_score, 4),
        "checks_passed": 9, "promoted": True, "raw_scores": eval_report.get("raw_scores", {})})
    write_validation_log(report, validation_log_file)
    return report, new_baseline
