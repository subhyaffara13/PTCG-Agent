
def _build_validate_report(staged_path, timestamp, version_id, checks):
    return {"version_id": version_id, "timestamp": timestamp, "staged_file": str(staged_path),
            "checks": checks, "all_passed": False, "promoted": False,
            "failed_check": None, "reason": None}

