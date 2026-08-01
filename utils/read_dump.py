
def read_dump(prefix: str, filename: str) -> dict[str, str | int | list[Any]]:
    basename = os.path.basename(filename)

    rank = int(basename[len(prefix) :])
    host_name = f"host_rank{rank}"

    with open(filename, "rb") as infile:
        dump = pickle.load(infile)

    entries = dump["entries"]
    version = dump["version"]
    pg_config = dump["pg_config"]

    return {
        "host_name": host_name,
        "rank": rank,
        "entries": entries,
        "version": version,
        "pg_config": pg_config,
    }

