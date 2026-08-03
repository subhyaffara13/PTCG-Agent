import sys
from typing import Any, Callable, Dict, List, Optional, Union

def function_setup(
    original_function: str, rules_obj, start_time, *args, **kwargs
):  # just run once to check if user wants to send their data anywhere - PostHog/Sentry/Slack/etc.
    ### NOTICES ###
    if litellm.set_verbose is True:
        verbose_logger.warning(
            "`litellm.set_verbose` is deprecated. Please set `os.environ['LITELLM_LOG'] = 'DEBUG'` for debug logs."
        )
    try:
        global callback_list, add_breadcrumb, user_logger_fn, Logging

        ## CUSTOM LLM SETUP ##
        custom_llm_setup()

        ## GET APPLIED GUARDRAILS
        applied_guardrails = get_applied_guardrails(kwargs)

        ## LOGGING SETUP
        function_id: Optional[str] = kwargs["id"] if "id" in kwargs else None

        ## LAZY LOAD COROUTINE CHECKER ##
        get_coroutine_checker_fn = getattr(
            sys.modules[__name__], "get_coroutine_checker"
        )
        coroutine_checker = get_coroutine_checker_fn()

        ## DYNAMIC CALLBACKS ##
        dynamic_callbacks: Optional[List[Union[str, Callable, "CustomLogger"]]] = (
            kwargs.pop("callbacks", None)
        )
        all_callbacks = get_dynamic_callbacks(dynamic_callbacks=dynamic_callbacks)

        if len(all_callbacks) > 0:
            for callback in all_callbacks:
                # check if callback is a string - e.g. "lago", "openmeter"
                if isinstance(callback, str):
                    callback = litellm.litellm_core_utils.litellm_logging._init_custom_logger_compatible_class(  # type: ignore
                        callback, internal_usage_cache=None, llm_router=None  # type: ignore
                    )
                    if callback is None or any(
                        isinstance(cb, type(callback))
                        for cb in litellm._async_success_callback
                    ):  # don't double add a callback
                        continue
                if callback not in litellm.input_callback:
                    litellm.input_callback.append(callback)  # type: ignore
                if callback not in litellm.success_callback:
                    litellm.logging_callback_manager.add_litellm_success_callback(callback)  # type: ignore
                if callback not in litellm.failure_callback:
                    litellm.logging_callback_manager.add_litellm_failure_callback(callback)  # type: ignore
                if callback not in litellm._async_success_callback:
                    litellm.logging_callback_manager.add_litellm_async_success_callback(callback)  # type: ignore
                if callback not in litellm._async_failure_callback:
                    litellm.logging_callback_manager.add_litellm_async_failure_callback(callback)  # type: ignore
            print_verbose(
                f"Initialized litellm callbacks, Async Success Callbacks: {litellm._async_success_callback}"
            )

        if (
            len(litellm.input_callback) > 0
            or len(litellm.success_callback) > 0
            or len(litellm.failure_callback) > 0
        ) and len(
            callback_list  # type: ignore
        ) == 0:  # type: ignore
            callback_list = list(
                set(
                    litellm.input_callback  # type: ignore
                    + litellm.success_callback
                    + litellm.failure_callback
                )
            )
            get_set_callbacks = getattr(sys.modules[__name__], "get_set_callbacks")
            get_set_callbacks()(callback_list=callback_list, function_id=function_id)
        ## ASYNC CALLBACKS - safety net for callbacks added via direct append
        if len(litellm.input_callback) > 0:
            removed_async_items = []
            for index, callback in enumerate(litellm.input_callback):  # type: ignore
                if coroutine_checker.is_async_callable(callback):
                    litellm._async_input_callback.append(callback)
                    removed_async_items.append(index)

            # Pop the async items from input_callback in reverse order to avoid index issues
            for index in reversed(removed_async_items):
                litellm.input_callback.pop(index)
        if len(litellm.success_callback) > 0:
            removed_async_items = []
            for index, callback in enumerate(litellm.success_callback):  # type: ignore
                if coroutine_checker.is_async_callable(callback):
                    litellm.logging_callback_manager.add_litellm_async_success_callback(
                        callback
                    )
                    removed_async_items.append(index)
                elif callback == "dynamodb" or callback == "openmeter":
                    # dynamo is an async callback, it's used for the proxy and needs to be async
                    # we only support async dynamo db logging for acompletion/aembedding since that's used on proxy
                    litellm.logging_callback_manager.add_litellm_async_success_callback(
                        callback
                    )
                    removed_async_items.append(index)
                elif (
                    callback in litellm._known_custom_logger_compatible_callbacks
                    and isinstance(callback, str)
                ):
                    _add_custom_logger_callback_to_specific_event(callback, "success")

            # Pop the async items from success_callback in reverse order to avoid index issues
            for index in reversed(removed_async_items):
                litellm.success_callback.pop(index)

        if len(litellm.failure_callback) > 0:
            removed_async_items = []
            for index, callback in enumerate(litellm.failure_callback):  # type: ignore
                if coroutine_checker.is_async_callable(callback):
                    litellm.logging_callback_manager.add_litellm_async_failure_callback(
                        callback
                    )
                    removed_async_items.append(index)
                elif (
                    callback in litellm._known_custom_logger_compatible_callbacks
                    and isinstance(callback, str)
                ):
                    _add_custom_logger_callback_to_specific_event(callback, "failure")

            # Pop the async items from failure_callback in reverse order to avoid index issues
            for index in reversed(removed_async_items):
                litellm.failure_callback.pop(index)
        ### DYNAMIC CALLBACKS ###
        dynamic_success_callbacks: Optional[
            List[Union[str, Callable, "CustomLogger"]]
        ] = None
        dynamic_async_success_callbacks: Optional[
            List[Union[str, Callable, "CustomLogger"]]
        ] = None
        dynamic_failure_callbacks: Optional[
            List[Union[str, Callable, "CustomLogger"]]
        ] = None
        dynamic_async_failure_callbacks: Optional[
            List[Union[str, Callable, "CustomLogger"]]
        ] = None
        if kwargs.get("success_callback", None) is not None and isinstance(
            kwargs["success_callback"], list
        ):
            removed_async_items = []
            for index, callback in enumerate(kwargs["success_callback"]):
                if (
                    coroutine_checker.is_async_callable(callback)
                    or callback == "dynamodb"
                    or callback == "s3"
                ):
                    if dynamic_async_success_callbacks is not None and isinstance(
                        dynamic_async_success_callbacks, list
                    ):
                        dynamic_async_success_callbacks.append(callback)
                    else:
                        dynamic_async_success_callbacks = [callback]
                    removed_async_items.append(index)
            # Pop the async items from success_callback in reverse order to avoid index issues
            for index in reversed(removed_async_items):
                kwargs["success_callback"].pop(index)
            dynamic_success_callbacks = kwargs.pop("success_callback")
        if kwargs.get("failure_callback", None) is not None and isinstance(
            kwargs["failure_callback"], list
        ):
            dynamic_failure_callbacks = kwargs.pop("failure_callback")

        if add_breadcrumb:
            try:
                from litellm.litellm_core_utils.core_helpers import safe_deep_copy

                details_to_log = safe_deep_copy(kwargs)
            except Exception:
                details_to_log = kwargs

            if litellm.turn_off_message_logging:
                # make a copy of the _model_Call_details and log it
                details_to_log.pop("messages", None)
                details_to_log.pop("input", None)
                details_to_log.pop("prompt", None)
            add_breadcrumb(
                category="litellm.llm_call",
                message=f"Keyword Args: {details_to_log}",
                level="info",
            )
        if "logger_fn" in kwargs:
            user_logger_fn = kwargs["logger_fn"]
        # INIT LOGGER - for user-specified integrations
        model = args[0] if len(args) > 0 else kwargs.get("model", None)
        call_type = original_function
        if (
            call_type == CallTypes.completion.value
            or call_type == CallTypes.acompletion.value
            or call_type == CallTypes.anthropic_messages.value
        ):
            messages = None
            if len(args) > 1:
                messages = args[1]
            elif kwargs.get("messages", None):
                messages = kwargs["messages"]
            ### PRE-CALL RULES ###
            Rules = getattr(sys.modules[__name__], "Rules")
            if (
                Rules.has_pre_call_rules()
                and isinstance(messages, list)
                and len(messages) > 0
                and isinstance(messages[0], dict)
                and "content" in messages[0]
            ):
                buffer = StringIO()
                for m in messages:
                    content = m.get("content", "")
                    if content is not None and isinstance(content, str):
                        buffer.write(content)

                rules_obj.pre_call_rules(
                    input=buffer.getvalue(),
                    model=model,
                )

            ### REMOVE THOUGHT SIGNATURES FROM TOOL CALL IDS FOR NON-GEMINI MODELS ###
            # Gemini models embed thought signatures in tool call IDs. When sending
            # messages with tool calls to non-Gemini providers, we need to remove these
            # signatures to ensure compatibility.
            if isinstance(messages, list) and len(messages) > 0:
                try:
                    from litellm.litellm_core_utils.get_llm_provider_logic import (
                        get_llm_provider,
                    )
                    from litellm.litellm_core_utils.prompt_templates.factory import (
                        THOUGHT_SIGNATURE_SEPARATOR,
                    )

                    # Get custom_llm_provider to determine target provider
                    custom_llm_provider = kwargs.get("custom_llm_provider")

                    # If custom_llm_provider not in kwargs, try to determine it from the model
                    if not custom_llm_provider and model:
                        try:
                            _, custom_llm_provider, _, _ = get_llm_provider(
                                model=model,
                                custom_llm_provider=custom_llm_provider,
                            )
                        except Exception:
                            # If we can't determine the provider, skip this processing
                            pass

                    # Only process if target is NOT a Gemini model
                    if not _is_gemini_model(model, custom_llm_provider):
                        verbose_logger.debug(
                            "Removing thought signatures from tool call IDs for non-Gemini model"
                        )

                        # Process messages to remove thought signatures
                        processed_messages = _remove_thought_signatures_from_messages(
                            messages, THOUGHT_SIGNATURE_SEPARATOR
                        )

                        # Update messages in kwargs or args
                        if "messages" in kwargs:
                            kwargs["messages"] = processed_messages
                        elif len(args) > 1:
                            args_list = list(args)
                            args_list[1] = processed_messages
                            args = tuple(args_list)

                except Exception as e:
                    # Log the error but don't fail the request
                    verbose_logger.warning(
                        f"Error removing thought signatures from tool call IDs: {str(e)}"
                    )
        elif (
            call_type == CallTypes.embedding.value
            or call_type == CallTypes.aembedding.value
        ):
            messages = args[1] if len(args) > 1 else kwargs.get("input", None)
        elif (
            call_type == CallTypes.image_generation.value
            or call_type == CallTypes.aimage_generation.value
        ):
            messages = args[0] if len(args) > 0 else kwargs["prompt"]
        elif (
            call_type == CallTypes.moderation.value
            or call_type == CallTypes.amoderation.value
        ):
            messages = args[1] if len(args) > 1 else kwargs["input"]
        elif (
            call_type == CallTypes.atext_completion.value
            or call_type == CallTypes.text_completion.value
        ):
            messages = args[0] if len(args) > 0 else kwargs["prompt"]
        elif (
            call_type == CallTypes.rerank.value or call_type == CallTypes.arerank.value
        ):
            messages = kwargs.get("query")
        elif (
            call_type == CallTypes.atranscription.value
            or call_type == CallTypes.transcription.value
        ):
            _file_obj: FileTypes = args[1] if len(args) > 1 else kwargs["file"]
            # Lazy import audio_utils.utils only when needed for transcription calls
            audio_utils = _get_cached_audio_utils()
            file_checksum = audio_utils.get_audio_file_content_hash(file_obj=_file_obj)
            if "metadata" in kwargs:
                kwargs["metadata"]["file_checksum"] = file_checksum
            else:
                kwargs["metadata"] = {"file_checksum": file_checksum}
            messages = file_checksum
        elif (
            call_type == CallTypes.aspeech.value or call_type == CallTypes.speech.value
        ):
            messages = kwargs.get("input", "speech")
        elif (
            call_type == CallTypes.aresponses.value
            or call_type == CallTypes.responses.value
        ):
            # Handle both 'input' (standard Responses API) and 'messages' (Cursor chat format)
            messages = (
                args[0]
                if len(args) > 0
                else kwargs.get("input")
                or kwargs.get("messages", "default-message-value")
            )
        elif (
            call_type == CallTypes.generate_content.value
            or call_type == CallTypes.agenerate_content.value
            or call_type == CallTypes.generate_content_stream.value
            or call_type == CallTypes.agenerate_content_stream.value
        ):
            try:
                from litellm.google_genai.adapters.transformation import (
                    GoogleGenAIAdapter,
                )
                from litellm.litellm_core_utils.prompt_templates.common_utils import (
                    get_last_user_message,
                )

                contents_param = args[1] if len(args) > 1 else kwargs.get("contents")
                model_param = args[0] if len(args) > 0 else kwargs.get("model", "")

                if contents_param:
                    adapter = GoogleGenAIAdapter()
                    transformed = adapter.translate_generate_content_to_completion(
                        model=model_param,
                        contents=contents_param,
                        config=kwargs.get("config"),
                    )
                    transformed_messages = transformed.get("messages", [])
                    messages = (
                        get_last_user_message(transformed_messages)
                        or "default-message-value"
                    )
                else:
                    messages = "default-message-value"
            except Exception as e:
                verbose_logger.debug(
                    f"Error extracting messages from Google contents: {str(e)}"
                )
                messages = "default-message-value"
        else:
            messages = "default-message-value"
        stream = False
        if _is_streaming_request(
            kwargs=kwargs,
            call_type=call_type,
        ):
            stream = True
        get_litellm_logging_class = getattr(
            sys.modules[__name__], "get_litellm_logging_class"
        )
        logging_obj = get_litellm_logging_class()(  # Victim for object pool
            model=model,  # type: ignore
            messages=messages,
            stream=stream,
            litellm_call_id=kwargs["litellm_call_id"],
            litellm_trace_id=kwargs.get("litellm_trace_id"),
            function_id=function_id or "",
            call_type=call_type,
            start_time=start_time,
            dynamic_success_callbacks=dynamic_success_callbacks,
            dynamic_failure_callbacks=dynamic_failure_callbacks,
            dynamic_async_success_callbacks=dynamic_async_success_callbacks,
            dynamic_async_failure_callbacks=dynamic_async_failure_callbacks,
            kwargs=kwargs,
            applied_guardrails=applied_guardrails,
        )

        ## check if metadata is passed in
        litellm_params: Dict[str, Any] = {"api_base": ""}
        if "metadata" in kwargs:
            litellm_params["metadata"] = kwargs["metadata"]
        if "litellm_metadata" in kwargs and isinstance(
            kwargs["litellm_metadata"], dict
        ):
            litellm_params["litellm_metadata"] = kwargs["litellm_metadata"].copy()
            # For endpoints like /v1/messages that use "litellm_metadata" instead
            # of "metadata" (to avoid conflicting with provider API metadata fields),
            # populate litellm_params["metadata"] so callbacks (e.g. Langfuse) that
            # read API key info from litellm_params["metadata"] see the fields.
            if not litellm_params.get("metadata"):
                litellm_params["metadata"] = kwargs["litellm_metadata"].copy()

        logging_obj.update_environment_variables(
            model=model,
            user="",
            optional_params={},
            litellm_params=litellm_params,
            stream_options=kwargs.get("stream_options", None),
        )
        return logging_obj, kwargs
    except Exception as e:
        verbose_logger.exception(
            "litellm.utils.py::function_setup() - [Non-Blocking] Error in function_setup"
        )
        raise e

