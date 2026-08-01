
def cleanup_dimensions():
    global dimension_process
    if dimension_process is not None:
        dimension_process.kill()

