
def print_wins(wins, rows, test_name):
    print()
    print("*" * 10)

    row_map = {}
    for row in rows:
        row_map[row["run_id"]] = row

    sorted_wins = dict(
        sorted(
            wins.items(),
            key=lambda item: (item[1], score(row_map[item[0]])),
            reverse=True,
        )
    )
    logger.debug(f"{test_name} Wins:{sorted_wins}")
    logger.info(f"Based on {test_name} wins and a scoring function, the ranking:")

    rank = 0
    previous_value = -1
    for count, (key, value) in enumerate(sorted_wins.items()):
        if value != previous_value:
            rank = count
        previous_value = value

        for row in rows:
            if row["run_id"] == key:
                logger.info(
                    "{:02d}: WINs={:02d}, run_id={}, latency={:5.2f}, top1_match={:.4f}, size={}_MB, experiment={}, {}".format(  # noqa: G001
                        rank,
                        value,
                        key,
                        get_latency(row),
                        float(row["top1_match_rate"]),
                        row["onnx_size_in_MB"],
                        row["experiment"],
                        get_ort_environment_variables(),
                    )
                )
                break

