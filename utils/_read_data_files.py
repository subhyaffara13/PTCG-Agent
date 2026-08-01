
def _read_data_files():
    from pathlib import Path
    bandit_report_path = Path("bandit_report.json")
    report_data = "{}"
    if bandit_report_path.exists():
        report_data = bandit_report_path.read_text(encoding="utf-8")
    donts_path = Path("skills/learned_donts.json")
    dos_path = Path("skills/learned_dos.json")
    donts_data = "{}"; dos_data = "{}"
    if donts_path.exists(): donts_data = donts_path.read_text(encoding="utf-8")
    if dos_path.exists(): dos_data = dos_path.read_text(encoding="utf-8")
    return report_data, donts_data, dos_data

