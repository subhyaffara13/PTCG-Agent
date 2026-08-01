
def _check_team_member_admin_add(
    member: Union[Member, List[Member]],
    premium_user: bool,
):
    if isinstance(member, Member) and member.role == "admin":
        if premium_user is not True:
            raise ValueError(
                f"Assigning team admins is a premium feature. {CommonProxyErrors.not_premium_user.value}"
            )
    elif isinstance(member, List):
        for m in member:
            if m.role == "admin":
                if premium_user is not True:
                    raise ValueError(
                        f"Assigning team admins is a premium feature. Got={m}. {CommonProxyErrors.not_premium_user.value}. "
                    )

