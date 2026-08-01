
def update_db_model(
    db_model: Deployment, updated_patch: updateDeployment
) -> PrismaCompatibleUpdateDBModel:
    merged_deployment_dict = DeploymentTypedDict(
        model_name=db_model.model_name,
        litellm_params=LiteLLMParamsTypedDict(
            **db_model.litellm_params.model_dump(exclude_none=True)  # type: ignore
        ),
        model_info=db_model.model_info.model_dump(exclude_none=True),
    )
    # update model name
    if updated_patch.model_name:
        merged_deployment_dict["model_name"] = updated_patch.model_name

    # update litellm params
    if updated_patch.litellm_params:
        # Encrypt any sensitive values
        encrypted_params = {
            k: encrypt_value_helper(v)
            for k, v in updated_patch.litellm_params.model_dump(
                exclude_none=True
            ).items()
        }

        merged_deployment_dict["litellm_params"].update(encrypted_params)  # type: ignore

    # update model info
    if updated_patch.model_info:
        if "model_info" not in merged_deployment_dict:
            merged_deployment_dict["model_info"] = {}
        merged_deployment_dict["model_info"].update(
            updated_patch.model_info.model_dump(exclude_none=True)
        )

    # Honor explicit-null clears LAST, after both merges, so a model_info blob the UI
    # passes through (which today re-sends the OLD pricing on every save) cannot
    # silently undo a litellm_params clear via .update().
    #
    # Restricted to SPECIAL_MODEL_INFO_PARAMS (input/output cost per token/character
    # and cache read/write costs) so this path cannot be used to null out privileged
    # model_info fields like team_id or access groups. SPECIAL_MODEL_INFO_PARAMS are
    # mirrored between litellm_params and model_info by Deployment.__init__, so the
    # clear propagates to both blobs.
    if updated_patch.litellm_params:
        for field in updated_patch.litellm_params.model_fields_set:
            if (
                field in SPECIAL_MODEL_INFO_PARAMS
                and getattr(updated_patch.litellm_params, field) is None
            ):
                merged_deployment_dict["litellm_params"].pop(field, None)  # type: ignore
                merged_deployment_dict.get("model_info", {}).pop(field, None)
    if updated_patch.model_info:
        for field in updated_patch.model_info.model_fields_set:
            if (
                field in SPECIAL_MODEL_INFO_PARAMS
                and getattr(updated_patch.model_info, field) is None
            ):
                merged_deployment_dict["model_info"].pop(field, None)  # type: ignore
                merged_deployment_dict.get("litellm_params", {}).pop(field, None)  # type: ignore

    # convert to prisma compatible format

    prisma_compatible_model_dict = PrismaCompatibleUpdateDBModel()
    if "model_name" in merged_deployment_dict:
        prisma_compatible_model_dict["model_name"] = merged_deployment_dict[
            "model_name"
        ]

    if "litellm_params" in merged_deployment_dict:
        prisma_compatible_model_dict["litellm_params"] = json.dumps(
            merged_deployment_dict["litellm_params"]
        )

    if "model_info" in merged_deployment_dict:
        model_info = merged_deployment_dict["model_info"]
        for key, value in model_info.items():
            if isinstance(value, datetime.datetime):
                model_info[key] = value.isoformat()
        prisma_compatible_model_dict["model_info"] = json.dumps(model_info)

    if updated_patch.blocked is not None:
        prisma_compatible_model_dict["blocked"] = updated_patch.blocked

    return prisma_compatible_model_dict

