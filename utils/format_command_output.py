
def format_command_output(returncode, stdout, stderr):
    msg = f"**Command Exit Code:** `{returncode}`\n"
    if stdout:
        msg += f"**Output:**\n```\n{stdout.decode(errors='replace')[-1500:]}\n```"
    if stderr:
        msg += f"**Errors:**\n```\n{stderr.decode(errors='replace')[-1500:]}\n```"
    if len(msg) > 2000:
        msg = msg[:1990] + "\n...(truncated)"
    return msg

