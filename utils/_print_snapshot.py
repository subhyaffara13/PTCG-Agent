import time
from pathlib import Path


def _print_snapshot(status_dir: str, csv_path: Path, total: int,
                    overall_start: float) -> None:
    done, timed_out, crashed = _classify_csv(csv_path)
    in_flight = _read_status_dir(status_dir)
    in_flight.sort(key=lambda r: r.get("started_at", 0))
    now = time.time()
    overall_elapsed = _fmt_elapsed(now - overall_start)
    print(
        f"\n[{overall_elapsed}] {done}/{total} done "
        f"({timed_out} timeouts, {crashed} crashes) | {len(in_flight)} running:",
        flush=True,
    )
    for r in in_flight:
        cell_elapsed = now - r.get("started_at", now)
        moves = (r.get("moves_p0", 0) or 0) + (r.get("moves_p1", 0) or 0)
        m0 = (r.get("model_p0") or "")[-25:]
        m1 = (r.get("model_p1") or "")[-25:]
        print(
            f"  {r.get('variant',''):18s} {m0:25s} vs {m1:25s}"
            f"  seed={r.get('seed')} {r.get('pair_role',''):4s}"
            f"  moves={moves:2d}  {_fmt_elapsed(cell_elapsed)}"
            f"  ({r.get('state','?')})",
            flush=True,
        )


def _print_snapshot(snapshot: dict[torch.device, dict[str, int]], units: str) -> None:
    if len(snapshot) == 0:
        print("No memory tracked.")
        return
    divisor = _get_mem_divisor(units)
    for dev, dev_snap in snapshot.items():
        if _rounding_fn(dev_snap[_TOTAL_KEY], divisor, 2) <= 0:
            continue
        print(
            f"Device: {dev}",
            *(
                f"\t{k.value}: {_rounding_fn(v, divisor, 2)} {units}"
                if isinstance(k, _RefType)
                else f"\t{k}: {_rounding_fn(v, divisor, 2)} {units}"
                for k, v in dev_snap.items()
            ),
            sep="\n",
        )

