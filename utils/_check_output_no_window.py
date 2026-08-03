import os

def _check_output_no_window(*args, **kwargs):
    # Avoid showing a cmd.exe window when running this
    # on Windows
    if os.name == 'nt':
        creation_flag = 0x08000000 # CREATE_NO_WINDOW
    else:
        creation_flag = 0 # Default value
    return check_output(*args, creationflags=creation_flag, **kwargs)

