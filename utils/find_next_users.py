
def find_next_users(split_node: torch.fx.Node) -> list[torch.fx.Node]:
    next_users = []
    for getitem_node in split_node.users:
        for getitem_user in getitem_node.users:
            if getitem_user not in next_users:
                next_users.append(getitem_user)
    return next_users

