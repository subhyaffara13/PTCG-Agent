
def run_significance_test(rows, output_csv_path):
    """Run U test and T test."""
    utest_wins = {}
    ttest_wins = {}
    for row in rows:
        run_id = row["run_id"]
        utest_wins[run_id] = 0
        ttest_wins[run_id] = 0

    with open(output_csv_path, "w", newline="") as csvfile:
        column_names = [
            "model_name",
            "run_id_1",
            "experiment_1",
            "top1_match_rate_1",
            "run_id_2",
            "experiment_2",
            "top1_match_rate_2",
            "U_statistic",
            "U_pvalue",
            "T_statistic",
            "T_pvalue",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()

        required_match_columns = ["model_name", "test_cases", "runs"]
        num_results = len(rows)
        for i in range(num_results - 1):
            result1 = rows[i]

            if isinstance(result1["top1_match_rate_per_run"], str):
                a = json.loads(result1["top1_match_rate_per_run"])
            else:
                a = result1["top1_match_rate_per_run"]

            for j in range(i + 1, num_results, 1):
                result2 = rows[j]

                all_matched = True
                for column in required_match_columns:
                    if result1[column] != result2[column]:
                        all_matched = False
                        break
                if not all_matched:
                    continue

                if isinstance(result2["top1_match_rate_per_run"], str):
                    b = json.loads(result2["top1_match_rate_per_run"])
                else:
                    b = result2["top1_match_rate_per_run"]

                try:
                    utest_statistic, utest_pvalue = scipy.stats.mannwhitneyu(
                        a, b, use_continuity=True, alternative="two-sided"
                    )  # TODO: shall we use one-sided: less or greater according to "top1_match_rate"
                except ValueError:  # ValueError: All numbers are identical in mannwhitneyu
                    utest_statistic = None
                    utest_pvalue = None
                ttest_statistic, ttest_pvalue = scipy.stats.ttest_ind(a, b, axis=None, equal_var=True)

                if utest_pvalue is not None and utest_pvalue < 0.05:
                    if float(result1["top1_match_rate"]) > float(result2["top1_match_rate"]):
                        utest_wins[result1["run_id"]] += 1
                    else:
                        utest_wins[result2["run_id"]] += 1

                if ttest_pvalue < 0.05:
                    if float(result1["top1_match_rate"]) > float(result2["top1_match_rate"]):
                        ttest_wins[result1["run_id"]] += 1
                    else:
                        ttest_wins[result2["run_id"]] += 1

                row = {
                    "model_name": result1["model_name"],
                    "run_id_1": result1["run_id"],
                    "experiment_1": result1["experiment"],
                    "top1_match_rate_1": float(result1["top1_match_rate"]),
                    "run_id_2": result2["run_id"],
                    "experiment_2": result2["experiment"],
                    "top1_match_rate_2": float(result2["top1_match_rate"]),
                    "U_statistic": utest_statistic,
                    "U_pvalue": utest_pvalue,
                    "T_statistic": ttest_statistic,
                    "T_pvalue": ttest_pvalue,
                }

                writer.writerow(row)
    logger.info(f"U-Test and T-Test results are output to {output_csv_path}")
    print_wins(utest_wins, rows, "U-Test")
    print_wins(ttest_wins, rows, "T-Test")

