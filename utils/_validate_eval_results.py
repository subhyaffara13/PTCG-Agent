
def _validate_eval_results(
    eval_results: EvalResult | list[EvalResult] | None,
    model_name: str | None,
) -> list[EvalResult]:
    if eval_results is None:
        return []
    if isinstance(eval_results, EvalResult):
        eval_results = [eval_results]
    if not isinstance(eval_results, list) or not all(isinstance(r, EvalResult) for r in eval_results):
        raise ValueError(
            f"`eval_results` should be of type `EvalResult` or a list of `EvalResult`, got {type(eval_results)}."
        )
    if model_name is None:
        raise ValueError("Passing `eval_results` requires `model_name` to be set.")
    return eval_results

