
def _parse_cli(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an LLM harness end-to-end against a Kaggle environment.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override MODEL_NAME for this run.",
    )
    parser.add_argument(
        "--replay-path",
        default=None,
        help="Override the replay save path (default: <caller_dir>/visualizer/default/replays/<replay_filename>).",
    )
    return parser.parse_args(argv)

