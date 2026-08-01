
def _classify_csv(csv_path: Path) -> tuple[int, int, int]:
    """Return (done, timed_out, crashed_other) from games.csv."""
    if not csv_path.exists():
        return 0, 0, 0
    done = timed_out = crashed = 0
    try:
        with csv_path.open() as f:
            for row in csv.DictReader(f):
                done += 1
                err = row.get("error") or ""
                if "TimeoutError" in err:
                    timed_out += 1
                elif err:
                    crashed += 1
                else:
                    # Even with no error string, crash_p* may be true
                    # (agent ERROR detected by env without raising).
                    if (str(row.get("crash_p0", "")).lower() == "true"
                            or str(row.get("crash_p1", "")).lower() == "true"):
                        crashed += 1
    except FileNotFoundError:
        pass
    return done, timed_out, crashed

