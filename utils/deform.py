
def deform(
    image: Image.Image,
    deformer: SupportsGetMesh,
    resample: int = Image.Resampling.BILINEAR,
) -> Image.Image:
    """
    Deform the image.

    :param image: The image to deform.
    :param deformer: A deformer object.  Any object that implements a
                    ``getmesh`` method can be used.
    :param resample: An optional resampling filter. Same values possible as
       in the PIL.Image.transform function.
    :return: An image.
    """
    return image.transform(
        image.size, Image.Transform.MESH, deformer.getmesh(image), resample
    )

