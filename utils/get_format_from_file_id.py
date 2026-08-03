import re
from typing import Optional

def get_format_from_file_id(file_id: Optional[str]) -> Optional[str]:
    """
    Gets format from file id

    unified_file_id = litellm_proxy:{};unified_id,{}
    If not a unified file id, returns 'file' as default format
    """
    from litellm.proxy.openai_files_endpoints.common_utils import (
        convert_b64_uid_to_unified_uid,
    )

    if not file_id:
        return None
    try:
        transformed_file_id = convert_b64_uid_to_unified_uid(file_id)
        if transformed_file_id.startswith(
            SpecialEnums.LITELM_MANAGED_FILE_ID_PREFIX.value
        ):
            match = re.match(
                f"{SpecialEnums.LITELM_MANAGED_FILE_ID_PREFIX.value}:(.*?);unified_id",
                transformed_file_id,
            )
            if match:
                return match.group(1)

        return None
    except Exception:
        return None

