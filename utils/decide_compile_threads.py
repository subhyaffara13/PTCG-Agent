import os
import sys

def decide_compile_threads() -> int:
    """
    Here are the precedence to decide compile_threads
    1. User can override it by TORCHINDUCTOR_COMPILE_THREADS.  One may want to disable async compiling by
       setting this to 1 to make pdb happy.
    2. Set to 1 if it's win32 platform
    3. decide by the number of CPU cores
    """
    import logging

    # Defined locally so install_config_module doesn't try to parse
    # as a config option.
    log = logging.getLogger(__name__)

    if "TORCHINDUCTOR_COMPILE_THREADS" in os.environ:
        compile_threads = int(os.environ["TORCHINDUCTOR_COMPILE_THREADS"])
        log.info("compile_threads set to %d via env", compile_threads)
    elif sys.platform == "win32":
        compile_threads = 1
        log.info("compile_threads set to 1 for win32")
    elif is_fbcode() and not parallel_compile_enabled_internally():
        compile_threads = 1
        log.info("compile_threads set to 1 in fbcode")
    else:
        cpu_count = torch._utils.cpu_count()
        assert cpu_count
        compile_threads = min(32, cpu_count)
        log.info("compile_threads set to %d", compile_threads)

    return compile_threads

