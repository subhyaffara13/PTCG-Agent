
def arg_parser(description: str):
    return argparse.ArgumentParser(
        description=description,
        formatter_class=RawTextArgumentDefaultsHelpFormatter,
    )

