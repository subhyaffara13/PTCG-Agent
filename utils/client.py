
def client(original_function):
    Rules = getattr(sys.modules[__name__], "Rules")
    rules_obj = Rules()

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        # DO NOT MOVE THIS. It always needs to run first
        # Check if this is an async function. If so only execute the async function
        call_type = original_function.__name__
        if _is_async_request(kwargs):
            # [OPTIONAL] CHECK MAX RETRIES / REQUEST
            if litellm.num_retries_per_request is not None:
                # check if previous_models passed in as ['litellm_params']['metadata]['previous_models']
                previous_models = (kwargs.get("metadata") or {}).get(
                    "previous_models", None
                )
                if previous_models is not None:
                    if litellm.num_retries_per_request <= len(previous_models):
                        raise Exception("Max retries per request hit!")

            # MODEL CALL
            result = original_function(*args, **kwargs)
            if _is_streaming_request(
                kwargs=kwargs,
                call_type=call_type,
            ):
                if (
                    "complete_response" in kwargs
                    and kwargs["complete_response"] is True
                ):
                    chunks = []
                    for idx, chunk in enumerate(result):
                        chunks.append(chunk)
                    return litellm.stream_chunk_builder(
                        chunks, messages=kwargs.get("messages", None)
                    )
                else:
                    return result

            return result

        # Prints Exactly what was passed to litellm function - don't execute any logic here - it should just print
        print_args_passed_to_litellm(original_function, args, kwargs)
        start_time = datetime.datetime.now()
        result = None
        logging_obj: Optional[LiteLLMLoggingObject] = kwargs.get(
            "litellm_logging_obj", None
        )

        # only set litellm_call_id if its not in kwargs
        if "litellm_call_id" not in kwargs:
            kwargs["litellm_call_id"] = str(uuid.uuid4())

        model: Optional[str] = args[0] if len(args) > 0 else kwargs.get("model", None)

        try:
            if logging_obj is None:
                logging_obj, kwargs = function_setup(
                    original_function.__name__, rules_obj, start_time, *args, **kwargs
                )

            # Type assertion: logging_obj is guaranteed to be non-None after function_setup
            assert (
                logging_obj is not None
            ), "logging_obj should not be None after function_setup"

            ## LOAD CREDENTIALS
            load_credentials_from_list(kwargs)
            kwargs["litellm_logging_obj"] = logging_obj
            LLMCachingHandler = _get_cached_llm_caching_handler()
            _llm_caching_handler: "LLMCachingHandler" = LLMCachingHandler(
                original_function=original_function,
                request_kwargs=kwargs,
                start_time=start_time,
            )
            logging_obj._llm_caching_handler = _llm_caching_handler

            # [OPTIONAL] CHECK BUDGET
            if litellm.max_budget:
                if litellm._current_cost > litellm.max_budget:
                    raise BudgetExceededError(
                        current_cost=litellm._current_cost,
                        max_budget=litellm.max_budget,
                    )

            # [OPTIONAL] CHECK MAX RETRIES / REQUEST
            if litellm.num_retries_per_request is not None:
                # check if previous_models passed in as ['litellm_params']['metadata]['previous_models']
                previous_models = (kwargs.get("metadata") or {}).get(
                    "previous_models", None
                )
                if previous_models is not None:
                    if litellm.num_retries_per_request <= len(previous_models):
                        raise Exception("Max retries per request hit!")

            # [OPTIONAL] CHECK CACHE
            print_verbose(
                f"SYNC kwargs[caching]: {kwargs.get('caching', False)}; litellm.cache: {litellm.cache}; kwargs.get('cache')['no-cache']: {kwargs.get('cache', {}).get('no-cache', False)}"
            )
            # if caching is false or cache["no-cache"]==True, don't run this
            if (
                (
                    (
                        (
                            kwargs.get("caching", None) is None
                            and litellm.cache is not None
                        )
                        or kwargs.get("caching", False) is True
                    )
                    and kwargs.get("cache", {}).get("no-cache", False) is not True
                )
                and kwargs.get("aembedding", False) is not True
                and kwargs.get("atext_completion", False) is not True
                and kwargs.get("acompletion", False) is not True
                and kwargs.get("aimg_generation", False) is not True
                and kwargs.get("atranscription", False) is not True
                and kwargs.get("arerank", False) is not True
                and kwargs.get("_arealtime", False) is not True
            ):  # allow users to control returning cached responses from the completion function
                # checking cache
                verbose_logger.debug("INSIDE CHECKING SYNC CACHE")
                caching_handler_response: "CachingHandlerResponse" = (
                    _llm_caching_handler._sync_get_cache(
                        model=model or "",
                        original_function=original_function,
                        logging_obj=logging_obj,
                        start_time=start_time,
                        call_type=call_type,
                        kwargs=kwargs,
                        args=args,
                    )
                )

                if caching_handler_response.cached_result is not None:
                    verbose_logger.debug("Cache hit!")
                    return caching_handler_response.cached_result

            # CHECK MAX TOKENS
            if (
                kwargs.get("max_tokens", None) is not None
                and model is not None
                and litellm.modify_params
                is True  # user is okay with params being modified
                and (
                    call_type == CallTypes.acompletion.value
                    or call_type == CallTypes.completion.value
                    or call_type == CallTypes.anthropic_messages.value
                )
            ):
                try:
                    base_model = model
                    if kwargs.get("hf_model_name", None) is not None:
                        base_model = f"huggingface/{kwargs.get('hf_model_name')}"
                    messages = None
                    if len(args) > 1:
                        messages = args[1]
                    elif kwargs.get("messages", None):
                        messages = kwargs["messages"]
                    user_max_tokens = kwargs.get("max_tokens")
                    modified_max_tokens = _get_modified_max_tokens()(
                        model=model,
                        base_model=base_model,
                        messages=messages,
                        user_max_tokens=user_max_tokens,
                        buffer_num=None,
                        buffer_perc=None,
                    )
                    kwargs["max_tokens"] = modified_max_tokens
                except Exception as e:
                    print_verbose(f"Error while checking max token limit: {str(e)}")
            # MODEL CALL
            result = original_function(*args, **kwargs)
            end_time = datetime.datetime.now()
            if _is_streaming_request(
                kwargs=kwargs,
                call_type=call_type,
            ):
                if (
                    "complete_response" in kwargs
                    and kwargs["complete_response"] is True
                ):
                    chunks = []
                    for idx, chunk in enumerate(result):
                        chunks.append(chunk)
                    return litellm.stream_chunk_builder(
                        chunks, messages=kwargs.get("messages", None)
                    )
                else:
                    # RETURN RESULT
                    update_response_metadata = getattr(
                        sys.modules[__name__], "update_response_metadata"
                    )
                    update_response_metadata(
                        result=result,
                        logging_obj=logging_obj,
                        model=model,
                        kwargs=kwargs,
                        start_time=start_time,
                        end_time=end_time,
                    )
                    return result
            elif "acompletion" in kwargs and kwargs["acompletion"] is True:
                return result
            elif "aembedding" in kwargs and kwargs["aembedding"] is True:
                return result
            elif "aimg_generation" in kwargs and kwargs["aimg_generation"] is True:
                return result
            elif "atranscription" in kwargs and kwargs["atranscription"] is True:
                return result
            elif "aspeech" in kwargs and kwargs["aspeech"] is True:
                return result
            elif asyncio.iscoroutine(result):  # bubble up to relevant async function
                return result

            ### POST-CALL RULES ###
            post_call_processing(
                original_response=result,
                model=model or None,
                optional_params=kwargs,
                original_function=original_function,
                rules_obj=rules_obj,
            )

            # [OPTIONAL] ADD TO CACHE
            _llm_caching_handler.sync_set_cache(
                result=result,
                args=args,
                kwargs=kwargs,
            )

            # LOG SUCCESS - handle streaming success logging in the _next_ object, remove `handle_success` once it's deprecated
            verbose_logger.info("Wrapper: Completed Call, calling success_handler")
            # Copy the current context to propagate it to the background thread
            # This is essential for OpenTelemetry span context propagation
            ctx = contextvars.copy_context()
            executor = getattr(sys.modules[__name__], "executor")
            executor.submit(
                ctx.run,
                logging_obj.success_handler,
                result,
                start_time,
                end_time,
            )
            # RETURN RESULT
            update_response_metadata = getattr(
                sys.modules[__name__], "update_response_metadata"
            )
            update_response_metadata(
                result=result,
                logging_obj=logging_obj,
                model=model,
                kwargs=kwargs,
                start_time=start_time,
                end_time=end_time,
            )
            return result
        except Exception as e:
            call_type = original_function.__name__
            if call_type == CallTypes.completion.value:
                num_retries = (
                    kwargs.get("num_retries", None) or litellm.num_retries or None
                )
                if kwargs.get("retry_policy", None):
                    get_num_retries_from_retry_policy = getattr(
                        sys.modules[__name__], "get_num_retries_from_retry_policy"
                    )
                    reset_retry_policy = getattr(
                        sys.modules[__name__], "reset_retry_policy"
                    )
                    num_retries = get_num_retries_from_retry_policy(
                        exception=e,
                        retry_policy=kwargs.get("retry_policy"),
                    )
                    kwargs["retry_policy"] = (
                        reset_retry_policy()
                    )  # prevent infinite loops
                litellm.num_retries = (
                    None  # set retries to None to prevent infinite loops
                )
                context_window_fallback_dict = kwargs.get(
                    "context_window_fallback_dict", {}
                )

                _is_litellm_router_call = "model_group" in (
                    kwargs.get("metadata") or {}
                )  # check if call from litellm.router/proxy
                if (
                    num_retries and not _is_litellm_router_call
                ):  # only enter this if call is not from litellm router/proxy. router has it's own logic for retrying
                    if (
                        isinstance(e, openai.APIError)
                        or isinstance(e, openai.Timeout)
                        or isinstance(e, openai.APIConnectionError)
                    ):
                        kwargs["num_retries"] = num_retries
                        return litellm.completion_with_retries(*args, **kwargs)
                elif (
                    isinstance(e, litellm.exceptions.ContextWindowExceededError)
                    and context_window_fallback_dict
                    and model in context_window_fallback_dict
                    and not _is_litellm_router_call
                ):
                    if len(args) > 0:
                        args[0] = context_window_fallback_dict[model]  # type: ignore
                    else:
                        kwargs["model"] = context_window_fallback_dict[model]
                    return original_function(*args, **kwargs)
            elif call_type == CallTypes.responses.value:
                num_retries = (
                    kwargs.get("num_retries", None) or litellm.num_retries or None
                )
                if kwargs.get("retry_policy", None):
                    get_num_retries_from_retry_policy = getattr(
                        sys.modules[__name__], "get_num_retries_from_retry_policy"
                    )
                    reset_retry_policy = getattr(
                        sys.modules[__name__], "reset_retry_policy"
                    )
                    num_retries = get_num_retries_from_retry_policy(
                        exception=e,
                        retry_policy=kwargs.get("retry_policy"),
                    )
                    kwargs["retry_policy"] = (
                        reset_retry_policy()
                    )  # prevent infinite loops
                litellm.num_retries = (
                    None  # set retries to None to prevent infinite loops
                )

                _is_litellm_router_call = "model_group" in (
                    kwargs.get("metadata") or {}
                )  # check if call from litellm.router/proxy
                if (
                    num_retries and not _is_litellm_router_call
                ):  # only enter this if call is not from litellm router/proxy. router has it's own logic for retrying
                    if (
                        isinstance(e, openai.APIError)
                        or isinstance(e, openai.Timeout)
                        or isinstance(e, openai.APIConnectionError)
                    ):
                        kwargs["num_retries"] = num_retries
                        return litellm.responses_with_retries(*args, **kwargs)
            traceback_exception = traceback.format_exc()
            end_time = datetime.datetime.now()

            # LOG FAILURE - handle streaming failure logging in the _next_ object, remove `handle_failure` once it's deprecated
            if logging_obj:
                logging_obj.failure_handler(
                    e, traceback_exception, start_time, end_time
                )  # DO NOT MAKE THREADED - router retry fallback relies on this!
            raise e

    @wraps(original_function)
    async def wrapper_async(*args, **kwargs):
        print_args_passed_to_litellm(original_function, args, kwargs)
        start_time = datetime.datetime.now()
        result = None
        _update_response_metadata = getattr(
            sys.modules[__name__], "update_response_metadata"
        )
        logging_obj: Optional[LiteLLMLoggingObject] = kwargs.get(
            "litellm_logging_obj", None
        )
        LLMCachingHandler = _get_cached_llm_caching_handler()
        _llm_caching_handler: "LLMCachingHandler" = LLMCachingHandler(
            original_function=original_function,
            request_kwargs=kwargs,
            start_time=start_time,
        )
        # only set litellm_call_id if its not in kwargs
        call_type = original_function.__name__
        if "litellm_call_id" not in kwargs:
            kwargs["litellm_call_id"] = str(uuid.uuid4())

        model: Optional[str] = args[0] if len(args) > 0 else kwargs.get("model", None)
        is_completion_with_fallbacks = kwargs.get("fallbacks") is not None
        kwargs.pop("_is_litellm_internal_call", None)  # discard if injected
        _is_litellm_internal_call = is_internal_call.get()

        try:
            if logging_obj is None:
                logging_obj, kwargs = function_setup(
                    original_function.__name__, rules_obj, start_time, *args, **kwargs
                )

            # Type assertion: logging_obj is guaranteed to be non-None after function_setup
            assert (
                logging_obj is not None
            ), "logging_obj should not be None after function_setup"

            modified_kwargs = await async_pre_call_deployment_hook(kwargs, call_type)
            if modified_kwargs is not None:
                kwargs = modified_kwargs

            # Sync logging_obj.stream after deployment hooks (they may convert it).
            _hook_stream = kwargs.get("stream")
            if _hook_stream is not None and logging_obj.stream != _hook_stream:
                logging_obj.stream = _hook_stream

            kwargs["litellm_logging_obj"] = logging_obj
            ## LOAD CREDENTIALS
            load_credentials_from_list(kwargs)
            logging_obj._llm_caching_handler = _llm_caching_handler
            # [OPTIONAL] CHECK BUDGET
            if litellm.max_budget:
                if litellm._current_cost > litellm.max_budget:
                    raise BudgetExceededError(
                        current_cost=litellm._current_cost,
                        max_budget=litellm.max_budget,
                    )

            # [OPTIONAL] CHECK CACHE
            if _is_debugging_on():
                print_verbose(
                    f"ASYNC kwargs[caching]: {kwargs.get('caching', False)}; litellm.cache: {litellm.cache}; kwargs.get('cache'): {kwargs.get('cache', None)}"
                )
            _caching_handler_response: "Optional[CachingHandlerResponse]" = (
                await _llm_caching_handler._async_get_cache(
                    model=model or "",
                    original_function=original_function,
                    logging_obj=logging_obj,
                    start_time=start_time,
                    call_type=call_type,
                    kwargs=kwargs,
                    args=args,
                )
            )

            if _caching_handler_response is not None:
                if (
                    _caching_handler_response.cached_result is not None
                    and _caching_handler_response.final_embedding_cached_response
                    is None
                ):
                    return _caching_handler_response.cached_result

                elif _caching_handler_response.embedding_all_elements_cache_hit is True:
                    return _caching_handler_response.final_embedding_cached_response

            # CHECK MAX TOKENS
            if (
                kwargs.get("max_tokens", None) is not None
                and model is not None
                and litellm.modify_params
                is True  # user is okay with params being modified
                and (
                    call_type == CallTypes.acompletion.value
                    or call_type == CallTypes.completion.value
                    or call_type == CallTypes.anthropic_messages.value
                )
            ):
                try:
                    base_model = model
                    if kwargs.get("hf_model_name", None) is not None:
                        base_model = f"huggingface/{kwargs.get('hf_model_name')}"
                    messages = None
                    if len(args) > 1:
                        messages = args[1]
                    elif kwargs.get("messages", None):
                        messages = kwargs["messages"]
                    user_max_tokens = kwargs.get("max_tokens")
                    modified_max_tokens = _get_modified_max_tokens()(
                        model=model,
                        base_model=base_model,
                        messages=messages,
                        user_max_tokens=user_max_tokens,
                        buffer_num=None,
                        buffer_perc=None,
                    )
                    kwargs["max_tokens"] = modified_max_tokens
                except Exception as e:
                    print_verbose(f"Error while checking max token limit: {str(e)}")

            # MODEL CALL
            result = await original_function(*args, **kwargs)
            end_time = datetime.datetime.now()

            if _is_streaming_request(
                kwargs=kwargs,
                call_type=call_type,
            ):
                if (
                    "complete_response" in kwargs
                    and kwargs["complete_response"] is True
                ):
                    chunks = []
                    for idx, chunk in enumerate(result):
                        chunks.append(chunk)
                    return litellm.stream_chunk_builder(
                        chunks, messages=kwargs.get("messages", None)
                    )
                else:
                    _update_response_metadata(
                        result=result,
                        logging_obj=logging_obj,
                        model=model,
                        kwargs=kwargs,
                        start_time=start_time,
                        end_time=end_time,
                    )
                    return result
            elif call_type == CallTypes.arealtime.value:
                return result
            ### POST-CALL RULES ###
            post_call_processing(
                original_response=result,
                model=model,
                optional_params=kwargs,
                original_function=original_function,
                rules_obj=rules_obj,
            )
            # Only run if call_type is a valid value in CallTypes
            _call_type_enum = _CALL_TYPE_ENUM_MAP.get(call_type)
            if _call_type_enum is not None:
                result = await async_post_call_success_deployment_hook(
                    request_data=kwargs,
                    response=result,
                    call_type=_call_type_enum,
                )

            ## Add response to cache
            await _llm_caching_handler.async_set_cache(
                result=result,
                original_function=original_function,
                kwargs=kwargs,
                args=args,
            )

            # LOG SUCCESS - handle streaming success logging in the _next_ object
            # Internal sub-calls (e.g. emulated file-search steps) share the
            # parent's logging obj; skip async logging here so only the outer call bills once.
            # NOTE: streaming requests return early (before this point) via
            # CustomStreamWrapper, so this block is non-streaming only.
            if not _is_litellm_internal_call:
                if getattr(logging_obj, "_defer_async_logging", False):

                    def _enqueue_deferred_logging() -> None:
                        asyncio.create_task(
                            _client_async_logging_helper(
                                logging_obj=logging_obj,
                                result=result,
                                start_time=start_time,
                                end_time=end_time,
                                is_completion_with_fallbacks=is_completion_with_fallbacks,
                            )
                        )

                    logging_obj._enqueue_deferred_logging = _enqueue_deferred_logging  # type: ignore
                else:
                    asyncio.create_task(
                        _client_async_logging_helper(
                            logging_obj=logging_obj,
                            result=result,
                            start_time=start_time,
                            end_time=end_time,
                            is_completion_with_fallbacks=is_completion_with_fallbacks,
                        )
                    )

            logging_obj.handle_sync_success_callbacks_for_async_calls(
                result=result,
                start_time=start_time,
                end_time=end_time,
            )
            # REBUILD EMBEDDING CACHING
            if (
                isinstance(result, EmbeddingResponse)
                and _caching_handler_response is not None
                and _caching_handler_response.final_embedding_cached_response
                is not None
            ):
                return _llm_caching_handler._combine_cached_embedding_response_with_api_result(
                    _caching_handler_response=_caching_handler_response,
                    embedding_response=result,
                    start_time=start_time,
                    end_time=end_time,
                )

            _update_response_metadata(
                result=result,
                logging_obj=logging_obj,
                model=model,
                kwargs=kwargs,
                start_time=start_time,
                end_time=end_time,
            )

            return result
        except Exception as e:
            traceback_exception = traceback.format_exc()
            end_time = datetime.datetime.now()
            if logging_obj and not _is_litellm_internal_call:
                try:
                    logging_obj.failure_handler(
                        e, traceback_exception, start_time, end_time
                    )  # DO NOT MAKE THREADED - router retry fallback relies on this!
                except Exception as e:
                    raise e
                try:
                    await logging_obj.async_failure_handler(
                        e, traceback_exception, start_time, end_time
                    )
                except Exception as e:
                    raise e

            call_type = original_function.__name__
            num_retries, kwargs = _get_wrapper_num_retries(kwargs=kwargs, exception=e)
            if call_type == CallTypes.acompletion.value:
                context_window_fallback_dict = kwargs.get(
                    "context_window_fallback_dict", {}
                )

                _is_litellm_router_call = "model_group" in (
                    kwargs.get("metadata") or {}
                )  # check if call from litellm.router/proxy

                if (
                    num_retries and not _is_litellm_router_call
                ):  # only enter this if call is not from litellm router/proxy. router has it's own logic for retrying
                    try:
                        litellm.num_retries = (
                            None  # set retries to None to prevent infinite loops
                        )
                        kwargs["num_retries"] = num_retries
                        kwargs["original_function"] = original_function
                        if isinstance(
                            e, openai.RateLimitError
                        ):  # rate limiting specific error
                            kwargs["retry_strategy"] = "exponential_backoff_retry"
                        elif isinstance(e, openai.APIError):  # generic api error
                            kwargs["retry_strategy"] = "constant_retry"
                        return await litellm.acompletion_with_retries(*args, **kwargs)
                    except Exception:
                        pass
                elif (
                    isinstance(e, litellm.exceptions.ContextWindowExceededError)
                    and context_window_fallback_dict
                    and model in context_window_fallback_dict
                    and not _is_litellm_router_call
                ):
                    if len(args) > 0:
                        args[0] = context_window_fallback_dict[model]  # type: ignore
                    else:
                        kwargs["model"] = context_window_fallback_dict[model]
                    return await original_function(*args, **kwargs)
            elif call_type == CallTypes.aresponses.value:
                _is_litellm_router_call = "model_group" in (
                    kwargs.get("metadata") or {}
                )  # check if call from litellm.router/proxy

                if (
                    num_retries and not _is_litellm_router_call
                ):  # only enter this if call is not from litellm router/proxy. router has it's own logic for retrying
                    try:
                        litellm.num_retries = (
                            None  # set retries to None to prevent infinite loops
                        )
                        kwargs["num_retries"] = num_retries
                        kwargs["original_function"] = original_function
                        if isinstance(
                            e, openai.RateLimitError
                        ):  # rate limiting specific error
                            kwargs["retry_strategy"] = "exponential_backoff_retry"
                        elif isinstance(e, openai.APIError):  # generic api error
                            kwargs["retry_strategy"] = "constant_retry"
                        return await litellm.aresponses_with_retries(*args, **kwargs)
                    except Exception:
                        pass

            setattr(
                e, "num_retries", num_retries
            )  ## IMPORTANT: returns the deployment's num_retries to the router

            timeout = _get_wrapper_timeout(kwargs=kwargs, exception=e)
            setattr(e, "timeout", timeout)
            raise e

    get_coroutine_checker = getattr(sys.modules[__name__], "get_coroutine_checker")
    is_coroutine = get_coroutine_checker().is_async_callable(original_function)

    # Return the appropriate wrapper based on the original function type
    if is_coroutine:
        return wrapper_async
    else:
        return wrapper

