
def _apply_quota_project_id(credentials, quota_project_id):
    if quota_project_id:
        credentials = credentials.with_quota_project(quota_project_id)
    else:
        credentials = credentials.with_quota_project_from_environment()

    from google.oauth2 import credentials as authorized_user_credentials

    if isinstance(credentials, authorized_user_credentials.Credentials) and (
        not credentials.quota_project_id
    ):
        _warn_about_problematic_credentials(credentials)
    return credentials

