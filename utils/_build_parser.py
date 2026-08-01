
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m idna",
        description=(
            "Convert a domain name between its Unicode (U-label) and "
            "ASCII-compatible (A-label) forms. With no mode flag, the "
            "direction is chosen from the first input — if it contains "
            "an xn-- label the stream is decoded, otherwise it is "
            "encoded — and the same mode is applied to every remaining "
            "input. UTS #46 mapping is applied by default; pass "
            "--strict to disable it. When no domains are given on the "
            "command line and stdin is piped, one domain per line is "
            "read from stdin."
        ),
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "-e",
        "--encode",
        dest="mode",
        action="store_const",
        const="encode",
        help="Encode the input to its ASCII A-label form.",
    )
    mode.add_argument(
        "-d",
        "--decode",
        dest="mode",
        action="store_const",
        const="decode",
        help="Decode the input from its ASCII A-label form.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Disable the default UTS #46 mapping and apply IDNA 2008 rules verbatim.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"idna {__version__}",
    )
    parser.add_argument(
        "domain",
        nargs="*",
        help="One or more domain names to convert. Omit to read from stdin.",
    )
    return parser


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m kaggle_environments.ablation",
        description="Prompt-ablation runner for Kaggle game environments.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("run", help="Run a paired-seat ablation tournament.")
    pr.add_argument("--env", required=True, help="Env name, e.g. open_spiel_bargaining.")
    pr.add_argument("--models", required=True,
                    help="Comma-separated model names (proxy-side, no openai/ prefix).")
    pr.add_argument("--games", type=int, default=20,
                    help="Games per matchup (must be even; default 20).")
    pr.add_argument("--variants", default="",
                    help="Comma-separated variant names; default all.")
    pr.add_argument("--concurrency", type=int, default=8,
                    help="Max concurrent games (worker process count).")
    pr.add_argument("--llm-call-timeout", type=int, default=900,
                    help="Per-LLM-call timeout in seconds. Passed to "
                         "litellm via the LLM_CALL_TIMEOUT env var, which "
                         "core_harness._call_llm reads. Single hung calls "
                         "fail at this limit so the agent's retry loop "
                         "can recover. Default 900s = 15 min.")
    pr.add_argument("--game-timeout", type=int, default=0,
                    help="Per-game SIGALRM watchdog (seconds). Default 0 "
                         "(disabled) -- the per-call timeout above is the "
                         "primary protection. Set to e.g. 3600 if you want "
                         "a hard ceiling on cumulative game wall time on "
                         "top of the per-call limit.")
    pr.add_argument("--status-interval", type=float, default=10.0,
                    help="Seconds between live status snapshots printed "
                         "by the monitor thread. Set to 0 to disable.")
    pr.add_argument("--self-play", action="store_true",
                    help="Add the M self-play cells per leaderboard.")
    pr.add_argument("--resume", action="store_true",
                    help="Skip cells already present in games.csv.")
    pr.add_argument("--dry-run", action="store_true",
                    help="Print the cell count and exit.")
    pr.add_argument("--out", default="ablation_results",
                    help="Output directory for games.csv + summary.md.")
    pr.set_defaults(func=cmd_run)

    pc = sub.add_parser("check", help="Verify baseline parity + variant rendering.")
    pc.add_argument("--env", required=True)
    pc.add_argument("--parity-seeds", type=int, default=5,
                    help="How many seeded observations to test.")
    pc.set_defaults(func=cmd_check)
    return p


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m kaggle_environments.ablation_analysis",
        description="Permutation test for prompt-ablation rank shifts.",
    )
    p.add_argument("--csv", required=True, help="Path to games.csv.")
    p.add_argument("--baseline", default="baseline",
                   help="Name of the baseline variant (default: baseline).")
    p.add_argument("--null", default="null",
                   help="Name of the null variant (byte-identical to "
                        "baseline). Set to empty string to disable.")
    p.add_argument("--permutations", type=int, default=2000,
                   help="Number of label-shuffles per test (default 2000).")
    p.add_argument("--seed", type=int, default=0,
                   help="RNG seed for the permutation shuffles.")
    p.add_argument("--out", default="",
                   help="Optional output file for the Markdown report; "
                        "default prints to stdout.")
    return p

