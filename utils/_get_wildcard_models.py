from typing import List, Optional

def _get_wildcard_models(
    unique_models: List[str],
    return_wildcard_routes: Optional[bool] = False,
    llm_router: Optional[Router] = None,
    team_id: Optional[str] = None,
) -> List[str]:
    models_to_remove = set()
    all_wildcard_models = []
    for model in unique_models:
        if _check_wildcard_routing(model=model):
            if (
                return_wildcard_routes
            ):  # will add the wildcard route to the list eg: anthropic/*.
                all_wildcard_models.append(model)

            ## get litellm params from model
            if llm_router is not None:
                model_list = llm_router.get_model_list(
                    model_name=model, team_id=team_id
                )
                if model_list:
                    for router_model in model_list:
                        wildcard_models = get_known_models_from_wildcard(
                            wildcard_model=model,
                            litellm_params=LiteLLM_Params(
                                **router_model["litellm_params"]  # type: ignore
                            ),
                        )
                        all_wildcard_models.extend(wildcard_models)
                else:
                    # Router has no deployment for this wildcard (e.g., BYOK team models)
                    # Fall back to expanding from known provider models
                    wildcard_models = get_known_models_from_wildcard(
                        wildcard_model=model, litellm_params=None
                    )
                    if wildcard_models:
                        models_to_remove.add(model)
                        all_wildcard_models.extend(wildcard_models)
            else:
                # get all known provider models
                wildcard_models = get_known_models_from_wildcard(
                    wildcard_model=model, litellm_params=None
                )

                if wildcard_models:
                    models_to_remove.add(model)
                    all_wildcard_models.extend(wildcard_models)

    for model in models_to_remove:
        unique_models.remove(model)

    return all_wildcard_models

