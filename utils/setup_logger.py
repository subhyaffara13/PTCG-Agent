import logging
import os

def setup_logger(verbose=True):
    if verbose:
        logging.basicConfig(
            format="[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s",
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
        logging.getLogger("transformers").setLevel(logging.WARNING)


def setup_logger(verbose=True):
    if verbose:
        logging.basicConfig(format="[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s")
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.basicConfig(format="[%(message)s")
        logging.getLogger().setLevel(logging.WARNING)


def setup_logger(output_dir, base_name):
    """
    Sets up a logger to output to both the console and a log file.

    Args:
        output_dir (str): The directory where the log file will be saved.
        base_name (str): The base name for the log file.
    """
    log_file = os.path.join(output_dir, f"{base_name}.log")
    os.makedirs(output_dir, exist_ok=True)
    handlers = [logging.StreamHandler(), logging.FileHandler(log_file, mode="w")]
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )

