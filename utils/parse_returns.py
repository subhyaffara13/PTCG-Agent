
def parse_returns(return_decl: str) -> tuple[Return, ...]:
    """
    Input: '()'
    Output: []
    """
    if return_decl == "()":
        return ()
    if return_decl[0] == "(" and return_decl[-1] == ")":
        return_decl = return_decl[1:-1]
    return tuple(Return.parse(arg) for arg in return_decl.split(", "))

