
def _email_rule(state: StateInline, silent: bool) -> bool:
    if state.linkLevel > 0:
        return False

    pos = state.pos
    if pos >= state.posMax or state.src[pos] != "@":
        return False
    # Need at least one character after '@'.
    if pos + 1 >= state.posMax:
        return False

    # Back-scan pending text for the local part of the email.
    local_rev: list[str] = []
    for ch in reversed(state.pending):
        if ch.isascii() and (ch.isalnum() or ch in ".+-_"):
            local_rev.append(ch)
        else:
            break

    if not local_rev:
        return False

    local_len = len(local_rev)
    if not _preceding_ok(state, local_len):
        return False

    # Forward-scan for the domain part.
    after_at = state.src[pos + 1 : state.posMax]
    domain_len = 0
    num_period = 0
    for i, ch in enumerate(after_at):
        if ch.isascii() and ch.isalnum():
            pass
        elif ch == "@":
            return False
        elif (
            ch == "."
            and i + 1 < len(after_at)
            and after_at[i + 1].isascii()
            and after_at[i + 1].isalnum()
        ):
            num_period += 1
        elif ch != "-" and ch != "_":
            break
        domain_len += 1

    if domain_len == 0 or num_period == 0:
        return False

    last_ch = after_at[domain_len - 1]
    if not (last_ch.isascii() and last_ch.isalnum()) and last_ch != ".":
        return False

    local_part = "".join(reversed(local_rev))
    email_text = local_part + state.src[pos : pos + 1 + domain_len]
    total_len = local_len + 1 + domain_len
    url = "mailto:" + email_text

    if silent:
        return True
    return _create_autolink(state, local_len, total_len, url, email_text)

