import os
import sys
import time
from pathlib import Path


def cmd_run(args: argparse.Namespace) -> int:
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    if not models:
        print("--models must list at least one model.", file=sys.stderr)
        return 2

    variants_all = load_variants(args.env)
    if args.variants:
        names = [v.strip() for v in args.variants.split(",") if v.strip()]
        missing = [n for n in names if n not in variants_all]
        if missing:
            print(
                f"Unknown variant(s): {missing}. "
                f"Available: {sorted(variants_all)}",
                file=sys.stderr,
            )
            return 2
        variants_to_run = {n: variants_all[n] for n in names}
    else:
        variants_to_run = variants_all

    cells = build_cells(
        variants_to_run.keys(),
        models,
        args.games,
        include_self_play=args.self_play,
    )

    if args.dry_run:
        print(
            f"{len(cells)} games would be scheduled "
            f"({len(variants_to_run)} variants × {len(models)} models × "
            f"{args.games} games/matchup"
            f"{' + self-play' if args.self_play else ''})."
        )
        return 0

    api_key = os.environ.get("MODEL_PROXY_KEY", "")
    api_base = os.environ.get("MODEL_PROXY_URL", "dummy_url")
    if not api_key and api_base != "dummy_url":
        print(
            "MODEL_PROXY_KEY env var is required (or set "
            "MODEL_PROXY_URL=dummy_url for offline testing).",
            file=sys.stderr,
        )
        return 2

    # Propagate the per-call timeout via env var so forked workers (and the
    # core_harness._call_llm inside them) inherit it without an API change.
    if args.llm_call_timeout and args.llm_call_timeout > 0:
        os.environ["LLM_CALL_TIMEOUT"] = str(int(args.llm_call_timeout))

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "games.csv"
    summary_path = out_dir / "summary.md"

    done = _read_existing_cells(csv_path) if args.resume else set()
    todo = [c for c in cells if _cell_key(c) not in done]
    if args.resume:
        print(f"Resume: {len(done)} cells already done, {len(todo)} to go.")
    else:
        print(f"Scheduling {len(todo)} games.")

    csv_file, writer = _open_csv_for_append(csv_path)

    # Status dir for the live monitor. Workers write per-cell JSON files
    # here on each agent invocation; the parent's monitor thread reads
    # them every --status-interval seconds and prints a snapshot.
    status_dir = str(out_dir / "status")
    os.makedirs(status_dir, exist_ok=True)
    # Stale status files from a previous run would otherwise show as
    # "in-flight" cells that don't exist. Clear on launch.
    for fname in os.listdir(status_dir):
        try:
            os.remove(os.path.join(status_dir, fname))
        except OSError:
            pass

    # Build the work items eagerly so workers receive a self-contained
    # tuple they can run without any reference to the parent process.
    work_items = [
        (args.env, c, variants_to_run[c.variant], api_key, api_base,
         args.game_timeout, status_dir)
        for c in todo
    ]

    completed = 0
    overall_start = time.time()
    stop_event = threading.Event()
    monitor: threading.Thread | None = None
    if args.status_interval > 0:
        monitor = threading.Thread(
            target=_monitor_thread_target,
            args=(status_dir, csv_path, len(todo), stop_event,
                  overall_start, args.status_interval),
            daemon=True,
        )
        monitor.start()

    try:
        ctx = mp.get_context("fork")
        with ProcessPoolExecutor(
            max_workers=args.concurrency,
            mp_context=ctx,
        ) as pool:
            futures = {pool.submit(_worker_entry, item): item for item in work_items}
            for fut in as_completed(futures):
                result = fut.result()
                writer.writerow(_row_dict(result))
                csv_file.flush()
                completed += 1
                if (
                    completed % max(1, len(todo) // 20) == 0
                    or completed == len(todo)
                ):
                    print(
                        f"  [{completed}/{len(todo)}] {result.variant}"
                        f" {result.model_p0} vs {result.model_p1}"
                        f" pair={result.pair_role} seed={result.seed}"
                        f" -> ({result.score_p0:+.2f}, {result.score_p1:+.2f})"
                        f" in {result.duration_s:.1f}s"
                    )
    finally:
        stop_event.set()
        if monitor is not None:
            monitor.join(timeout=2.0)
        csv_file.close()

    # Re-read everything to build the summary (works under --resume).
    with csv_path.open() as f:
        all_rows = list(csv.DictReader(f))
    summary = render_summary(
        args.env, list(variants_to_run.keys()), models, all_rows,
    )
    summary_path.write_text(summary)
    print(f"\nWrote {len(all_rows)} rows to {csv_path}")
    print(f"Wrote summary to {summary_path}")
    return 0

