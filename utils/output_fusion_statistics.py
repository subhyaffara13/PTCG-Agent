
def output_fusion_statistics(model_fusion_statistics, csv_filename):
    with open(csv_filename, mode="a", newline="", encoding="ascii") as csv_file:
        column_names = [
            "model_filename",
            "datetime",
            "transformers",
            "torch",
            *list(next(iter(model_fusion_statistics.values())).keys()),
        ]
        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        csv_writer.writeheader()
        for key in model_fusion_statistics:
            model_fusion_statistics[key]["datetime"] = str(datetime.now())
            model_fusion_statistics[key]["transformers"] = transformers.__version__
            model_fusion_statistics[key]["torch"] = torch.__version__
            model_fusion_statistics[key]["model_filename"] = key
            csv_writer.writerow(model_fusion_statistics[key])
    logger.info(f"Fusion statistics is saved to csv file: {csv_filename}")

