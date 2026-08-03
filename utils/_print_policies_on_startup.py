from typing import Any, Dict, List, Optional

def _print_policies_on_startup(
    policies_config: Dict[str, Any],
    policy_attachments_config: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """
    Print loaded policies to console on startup (similar to model list).
    """
    import sys

    print(  # noqa: T201
        f"{_green_color_code}\nLiteLLM Policy Engine: Loaded {len(policies_config)} policies{_reset_color_code}\n"
    )
    sys.stdout.flush()

    for policy_name, policy_data in policies_config.items():
        guardrails = policy_data.get("guardrails", {})
        inherit = policy_data.get("inherit")
        condition = policy_data.get("condition")
        description = policy_data.get("description")

        guardrails_add = (
            guardrails.get("add", []) if isinstance(guardrails, dict) else []
        )
        guardrails_remove = (
            guardrails.get("remove", []) if isinstance(guardrails, dict) else []
        )
        inherit_str = f" (inherits: {inherit})" if inherit else ""

        print(  # noqa: T201
            f"{_blue_color_code}  - {policy_name}{inherit_str}{_reset_color_code}"
        )
        if description:
            print(f"      description: {description}")  # noqa: T201
        if guardrails_add:
            print(f"      guardrails.add: {guardrails_add}")  # noqa: T201
        if guardrails_remove:
            print(f"      guardrails.remove: {guardrails_remove}")  # noqa: T201
        if condition:
            model_condition = (
                condition.get("model") if isinstance(condition, dict) else None
            )
            if model_condition:
                print(f"      condition.model: {model_condition}")  # noqa: T201

    # Print attachments
    if policy_attachments_config:
        print(  # noqa: T201
            f"\n{_yellow_color_code}Policy Attachments: {len(policy_attachments_config)} attachment(s){_reset_color_code}"
        )
        for attachment in policy_attachments_config:
            policy = attachment.get("policy", "unknown")
            scope = attachment.get("scope")
            teams = attachment.get("teams")
            keys = attachment.get("keys")
            models = attachment.get("models")

            scope_parts = []
            if scope == "*":
                scope_parts.append("scope=* (global)")
            if teams:
                scope_parts.append(f"teams={teams}")
            if keys:
                scope_parts.append(f"keys={keys}")
            if models:
                scope_parts.append(f"models={models}")
            scope_str = ", ".join(scope_parts) if scope_parts else "all"

            print(f"  - {policy} -> {scope_str}")  # noqa: T201
    else:
        print(  # noqa: T201
            f"\n{_yellow_color_code}Warning: No policy_attachments configured. Policies will not be applied to any requests.{_reset_color_code}"
        )

    print()  # noqa: T201
    sys.stdout.flush()

