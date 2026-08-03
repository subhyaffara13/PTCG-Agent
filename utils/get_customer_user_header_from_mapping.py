from typing import Optional

def get_customer_user_header_from_mapping(user_id_mapping) -> Optional[list]:
    """Return the header_name mapped to CUSTOMER role, if any (dict-based)."""
    if not user_id_mapping:
        return None
    items = user_id_mapping if isinstance(user_id_mapping, list) else [user_id_mapping]
    customer_headers_mappings = []
    for item in items:
        if not isinstance(item, dict):
            continue
        role = item.get("litellm_user_role")
        header_name = item.get("header_name")
        if role is None or not header_name:
            continue
        if str(role).lower() == str(LitellmUserRoles.CUSTOMER).lower():
            customer_headers_mappings.append(header_name.lower())

    if customer_headers_mappings:
        return customer_headers_mappings

    return None

