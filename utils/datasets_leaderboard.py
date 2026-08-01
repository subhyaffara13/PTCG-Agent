
def datasets_leaderboard(
    dataset_id: Annotated[str, typer.Argument(help="The benchmark dataset ID (e.g. `SWE-bench/SWE-bench_Verified`).")],
    limit: LimitOpt = 20,
    token: TokenOpt = None,
) -> None:
    """List model scores from a dataset leaderboard. This command helps find the best models for a task or compare models by benchmark scores. Use 'hf datasets ls --filter benchmark:official' to list available leaderboards."""
    api = get_hf_api(token=token)
    leaderboard = api.get_dataset_leaderboard(repo_id=dataset_id)
    results = [_dataclass_to_dict(entry) for entry in leaderboard[:limit]]
    out.table(
        results,
        headers=["rank", "model_id", "value", "source"],
        id_key="model_id",
    )
    out.hint("Use 'hf datasets ls --filter benchmark:official' to list available leaderboards.")
    if leaderboard:
        out.hint(f"Use 'hf models info {leaderboard[0].model_id}' to get details about a model.")

