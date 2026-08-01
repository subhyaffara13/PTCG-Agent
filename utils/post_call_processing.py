
def post_call_processing(
    original_response,
    model,
    optional_params: Optional[dict],
    original_function,
    rules_obj,
):
    try:
        if original_response is None:
            pass
        else:
            call_type = original_function.__name__
            if (
                call_type == CallTypes.completion.value
                or call_type == CallTypes.acompletion.value
            ):
                is_coroutine = check_coroutine(original_response)
                if is_coroutine is True:
                    pass
                else:
                    if (
                        isinstance(original_response, ModelResponse)
                        and len(original_response.choices) > 0
                    ):
                        model_response: Optional[str] = original_response.choices[
                            0
                        ].message.content  # type: ignore
                        if model_response is not None:
                            ### POST-CALL RULES ###
                            rules_obj.post_call_rules(input=model_response, model=model)
                            ### JSON SCHEMA VALIDATION ###
                            # Per-request flag takes priority over global flag
                            _per_request_validation = (
                                optional_params.get("enable_json_schema_validation")
                                if optional_params is not None
                                else None
                            )
                            _enable_json_schema_validation = (
                                _per_request_validation
                                if _per_request_validation is not None
                                else litellm.enable_json_schema_validation
                            )
                            if _enable_json_schema_validation is True:
                                try:
                                    if (
                                        optional_params is not None
                                        and "response_format" in optional_params
                                        and optional_params["response_format"]
                                        is not None
                                    ):
                                        json_response_format: Optional[dict] = None
                                        if (
                                            isinstance(
                                                optional_params["response_format"],
                                                dict,
                                            )
                                            and optional_params["response_format"].get(
                                                "json_schema"
                                            )
                                            is not None
                                        ):
                                            json_response_format = optional_params[
                                                "response_format"
                                            ]
                                        elif _parsing._completions.is_basemodel_type(
                                            optional_params["response_format"]  # type: ignore
                                        ):
                                            json_response_format = (
                                                type_to_response_format_param(
                                                    response_format=optional_params[
                                                        "response_format"
                                                    ]
                                                )
                                            )
                                        if json_response_format is not None:
                                            litellm.litellm_core_utils.json_validation_rule.validate_schema(
                                                schema=json_response_format[
                                                    "json_schema"
                                                ]["schema"],
                                                response=model_response,
                                            )
                                except TypeError:
                                    pass
                            if (
                                optional_params is not None
                                and "response_format" in optional_params
                                and isinstance(optional_params["response_format"], dict)
                                and "type" in optional_params["response_format"]
                                and optional_params["response_format"]["type"]
                                == "json_object"
                                and "response_schema"
                                in optional_params["response_format"]
                                and isinstance(
                                    optional_params["response_format"][
                                        "response_schema"
                                    ],
                                    dict,
                                )
                                and "enforce_validation"
                                in optional_params["response_format"]
                                and optional_params["response_format"][
                                    "enforce_validation"
                                ]
                                is True
                            ):
                                # schema given, json response expected, and validation enforced
                                litellm.litellm_core_utils.json_validation_rule.validate_schema(
                                    schema=optional_params["response_format"][
                                        "response_schema"
                                    ],
                                    response=model_response,
                                )

    except Exception as e:
        raise e

