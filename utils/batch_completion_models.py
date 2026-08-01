
def batch_completion_models(*args, **kwargs):
    """
    Send a request to multiple language models concurrently and return the response
    as soon as one of the models responds.

    Args:
        *args: Variable-length positional arguments passed to the completion function.
        **kwargs: Additional keyword arguments:
            - models (str or list of str): The language models to send requests to.
            - Other keyword arguments to be passed to the completion function.

    Returns:
        str or None: The response from one of the language models, or None if no response is received.

    Note:
        This function utilizes a ThreadPoolExecutor to parallelize requests to multiple models.
        It sends requests concurrently and returns the response from the first model that responds.
    """

    if "model" in kwargs:
        kwargs.pop("model")
    if "models" in kwargs:
        models = kwargs["models"]
        kwargs.pop("models")
        futures = {}
        with ThreadPoolExecutor(max_workers=len(models)) as executor:
            for model in models:
                futures[model] = executor.submit(
                    litellm.completion, *args, model=model, **kwargs
                )

            for model, future in sorted(
                futures.items(), key=lambda x: models.index(x[0])
            ):
                if future.result() is not None:
                    return future.result()
    elif "deployments" in kwargs:
        deployments = kwargs["deployments"]
        kwargs.pop("deployments")
        kwargs.pop("model_list")
        nested_kwargs = kwargs.pop("kwargs", {})
        futures = {}
        with ThreadPoolExecutor(max_workers=len(deployments)) as executor:
            for deployment in deployments:
                for key in kwargs.keys():
                    if (
                        key not in deployment
                    ):  # don't override deployment values e.g. model name, api base, etc.
                        deployment[key] = kwargs[key]
                kwargs = {**deployment, **nested_kwargs}
                futures[deployment["model"]] = executor.submit(
                    litellm.completion, **kwargs
                )

            while futures:
                # wait for the first returned future
                print_verbose("\n\n waiting for next result\n\n")
                done, _ = wait(futures.values(), return_when=FIRST_COMPLETED)
                print_verbose(f"done list\n{done}")
                for future in done:
                    try:
                        result = future.result()
                        return result
                    except Exception:
                        # if model 1 fails, continue with response from model 2, model3
                        print_verbose(
                            "\n\ngot an exception, ignoring, removing from futures"
                        )
                        print_verbose(futures)
                        new_futures = {}
                        for key, value in futures.items():
                            if future == value:
                                print_verbose(f"removing key{key}")
                                continue
                            else:
                                new_futures[key] = value
                        futures = new_futures
                        print_verbose(f"new futures{futures}")
                        continue

                print_verbose("\n\ndone looping through futures\n\n")
                print_verbose(futures)

    return None  # If no response is received from any model

