
def add_controlnet_arguments(parser, is_xl: bool = False):
    """
    Add control net related arguments.
    """
    group = parser.add_argument_group("Options for ControlNet (supports 1.5, sd-turbo, xl-turbo, xl-1.0).")

    group.add_argument(
        "-ci",
        "--controlnet-image",
        nargs="*",
        type=str,
        default=[],
        help="Path to the input regular RGB image/images for controlnet",
    )
    group.add_argument(
        "-ct",
        "--controlnet-type",
        nargs="*",
        type=str,
        default=[],
        choices=list(PipelineInfo.supported_controlnet("xl-1.0" if is_xl else "1.5").keys()),
        help="A list of controlnet type",
    )
    group.add_argument(
        "-cs",
        "--controlnet-scale",
        nargs="*",
        type=float,
        default=[],
        help="The outputs of the controlnet are multiplied by `controlnet_scale` before they are added to the residual in the original unet. Default is 0.5 for SDXL, or 1.0 for SD 1.5",
    )

