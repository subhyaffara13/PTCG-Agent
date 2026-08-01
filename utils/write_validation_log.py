
def write_validation_log(report: dict, log_file: Path):
    try: log_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    except: pass

