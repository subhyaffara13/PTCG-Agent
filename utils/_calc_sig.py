
def _calc_sig(action: str, bench_sigs: Dict[int, str], gs: dict) -> str:
    parts = action.split(":")
    if len(parts) < 2:
        return action
    target = parts[1]
    if target.startswith("bench_"):
        try:
            idx = int(target.split("_")[1])
            if idx in bench_sigs:
                return f"{parts[0]}:bench_sig_{bench_sigs[idx]}"
        except (ValueError, IndexError):
            pass
    return action


def _calc_sig(action: str, bench_sigs: Dict[int, str], gs: dict) -> str:
    parts = action.split(":")
    if len(parts) < 2:
        return action
    target = parts[1]
    if target.startswith("bench_"):
        try:
            idx = int(target.split("_")[1])
            if idx in bench_sigs:
                return f"{parts[0]}:bench_sig_{bench_sigs[idx]}"
        except (ValueError, IndexError):
            pass
    return action


def _calc_sig(action: str, bench_sigs: Dict[int, str], gs: dict) -> str:
    parts = action.split(":")
    if len(parts) < 2:
        return action
    target = parts[1]
    if target.startswith("bench_"):
        try:
            idx = int(target.split("_")[1])
            if idx in bench_sigs:
                return f"{parts[0]}:bench_sig_{bench_sigs[idx]}"
        except (ValueError, IndexError):
            pass
    return action

