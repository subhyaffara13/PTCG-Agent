from pathlib import Path


def create_os_error_message(
    error: OSError, show_traceback: bool, using_user_site: bool
) -> str:
    """Format an error message for an OSError

    It may occur anytime during the execution of the install command.
    """
    parts = []

    # Mention the error if we are not going to show a traceback
    parts.append("Could not install packages due to an OSError")
    if not show_traceback:
        parts.append(": ")
        parts.append(str(error))
    else:
        parts.append(".")

    # Spilt the error indication from a helper message (if any)
    parts[-1] += "\n"

    # Suggest useful actions to the user:
    #  (1) using user site-packages or (2) verifying the permissions
    if error.errno == errno.EACCES:
        user_option_part = "Consider using the `--user` option"
        permissions_part = "Check the permissions"

        if not running_under_virtualenv() and not using_user_site:
            parts.extend(
                [
                    user_option_part,
                    " or ",
                    permissions_part.lower(),
                ]
            )
        else:
            parts.append(permissions_part)
        parts.append(".\n")

    # Suggest to check "pip config debug" in case of invalid proxy
    if type(error) is InvalidProxyURL:
        parts.append(
            'Consider checking your local proxy configuration with "pip config debug"'
        )
        parts.append(".\n")

    # On Windows, errors like EINVAL or ENOENT may occur
    # if a file or folder name exceeds 255 characters,
    # or if the full path exceeds 260 characters and long path support isn't enabled.
    # This condition checks for such cases and adds a hint to the error output.

    if WINDOWS and error.errno in (errno.EINVAL, errno.ENOENT) and error.filename:
        if any(len(part) > 255 for part in Path(error.filename).parts):
            parts.append(
                "HINT: This error might be caused by a file or folder name exceeding "
                "255 characters, which is a Windows limitation even if long paths "
                "are enabled.\n "
            )
        if len(error.filename) > 260:
            parts.append(
                "HINT: This error might have occurred since "
                "this system does not have Windows Long Path "
                "support enabled. You can find information on "
                "how to enable this at "
                "https://pip.pypa.io/warnings/enable-long-paths\n"
            )
    return "".join(parts).strip() + "\n"

