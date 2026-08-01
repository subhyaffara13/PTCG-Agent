
def datasets_parquet(
    dataset_id: Annotated[str, typer.Argument(help="The dataset ID (e.g. `username/repo-name`).")],
    subset: Annotated[str | None, typer.Option("--subset", help="Filter parquet entries by subset/config.")] = None,
    split: Annotated[str | None, typer.Option(help="Filter parquet entries by split.")] = None,
    token: TokenOpt = None,
) -> None:
    """List parquet file URLs available for a dataset."""
    api = get_hf_api(token=token)
    entries = api.list_dataset_parquet_files(repo_id=dataset_id, config=subset)
    filtered = [entry for entry in entries if split is None or entry.split == split]
    results = [
        {"subset": entry.config, "split": entry.split, "url": entry.url, "size": entry.size} for entry in filtered
    ]
    out.table(results, headers=["subset", "split", "url", "size"], id_key="url")

