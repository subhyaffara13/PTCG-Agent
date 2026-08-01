
def _font_to_quadratic(input_path, output_path=None, **kwargs):
    ufo = open_ufo(input_path)
    logger.info("Converting curves for %s", input_path)
    if font_to_quadratic(ufo, **kwargs):
        logger.info("Saving %s", output_path)
        if output_path:
            ufo.save(output_path)
        else:
            ufo.save()  # save in-place
    elif output_path:
        _copytree(input_path, output_path)

