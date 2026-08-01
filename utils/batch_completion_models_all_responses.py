
def batch_completion_models_all_responses(*args, **kwargs):
    """
    Send a request to multiple language models concurrently and return a list of responses
    from all models that respond.

    Args:
        *args: Variable-length positional arguments passed to the completion function.
        **kwargs: Additional keyword arguments:
            - models (str or list of str): The language models to send requests to.
            - Other keyword arguments to be passed to the completion function.

    Returns:
        list: A list of responses from the language models that responded.

    Note:
        This function utilizes a ThreadPoolExecutor to parallelize requests to multiple models.
        It sends requests concurrently and collects responses from all models that respond.
    """
    import concurrent.futures

    # ANSI escape codes for colored output

    if "model" in kwargs:
        kwargs.pop("model")
    if "models" in kwargs:
        models = kwargs.pop("models")
    else:
        raise Exception("'models' param not in kwargs")

    if isinstance(models, str):
        models = [models]
    elif isinstance(models, (list, tuple)):
        models = list(models)
    else:
        raise TypeError("'models' must be a string or list of strings")

    if len(models) == 0:
        return []

    responses = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(models)) as executor:
        futures = [
            executor.submit(litellm.completion, *args, model=model, **kwargs)
            for model in models
        ]

        for future in futures:
            try:
                result = future.result()
                if result is not None:
                    responses.append(result)
            except Exception as e:
                print_verbose(
                    f"batch_completion_models_all_responses: model request failed: {str(e)}"
                )
                continue

    return responses

