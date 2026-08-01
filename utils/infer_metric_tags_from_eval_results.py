
def infer_metric_tags_from_eval_results(eval_results):
    if eval_results is None:
        return {}
    result = {}
    for key in eval_results:
        if key.lower().replace(" ", "_") in METRIC_TAGS:
            result[key.lower().replace(" ", "_")] = key
        elif key.lower() == "rouge1":
            result["rouge"] = key
    return result

