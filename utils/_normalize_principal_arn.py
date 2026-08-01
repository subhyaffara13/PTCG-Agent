
def _normalize_principal_arn(caller_arn: str, account_id: str) -> str:
    """
    Normalize a caller ARN to the format required by OpenSearch data access policies.

    OpenSearch Serverless data access policies require:
    - IAM users: arn:aws:iam::account-id:user/user-name
    - IAM roles: arn:aws:iam::account-id:role/role-name

    But get_caller_identity() returns for assumed roles:
    - arn:aws:sts::account-id:assumed-role/role-name/session-name

    This function converts assumed-role ARNs to the proper IAM role ARN format.
    """
    if ":assumed-role/" in caller_arn:
        # Extract role name from assumed-role ARN
        # Format: arn:aws:sts::ACCOUNT:assumed-role/ROLE-NAME/SESSION-NAME
        parts = caller_arn.split("/")
        if len(parts) >= 2:
            role_name = parts[1]
            return f"arn:aws:iam::{account_id}:role/{role_name}"
    return caller_arn

