
def transform_ft(
    details: dict[str, dict[str, Any]], group_world_size: int
) -> dict[str, dict[str, Any]]:
    for dump_key, dump in details.items():
        rank = dump["rank"]
        for key, pg_config in dump["pg_config"].items():
            if pg_config["desc"] == "default_pg":
                ranks = eval(pg_config["ranks"])
                replica_id = rank // group_world_size
                first_rank = replica_id * group_world_size
                new_ranks = [r + first_rank for r in ranks]
                details[dump_key]["pg_config"][key]["ranks"] = f"{new_ranks}"

    return details

