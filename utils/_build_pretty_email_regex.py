
def _build_pretty_email_regex() -> re.Pattern[str]:
    name_chars = r'[\w!#$%&\'*+\-/=?^_`{|}~]'
    unquoted_name_group = rf'((?:{name_chars}+\s+)*{name_chars}+)'
    quoted_name_group = r'"((?:[^"]|\")+)"'
    email_group = r'<(.+)>'
    return re.compile(rf'\s*(?:{unquoted_name_group}|{quoted_name_group})?\s*{email_group}\s*')

