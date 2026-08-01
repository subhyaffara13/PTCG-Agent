
def get_rbac_role(jwt_handler: JWTHandler, scopes: List[str]) -> str:
    is_admin = jwt_handler.is_admin(scopes=scopes)
    if is_admin:
        return LitellmUserRoles.PROXY_ADMIN
    else:
        return LitellmUserRoles.TEAM

