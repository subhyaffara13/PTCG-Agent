
def _generate_crop_images(
    crop_boxes, image, points_grid, layer_idxs, target_size, original_size, input_data_format=None
):
    """
    Takes as an input bounding boxes that are used to crop the image. Based in the crops, the corresponding points are
    also passed.
    """
    cropped_images = []
    total_points_per_crop = []
    for i, crop_box in enumerate(crop_boxes):
        left, top, right, bottom = crop_box
        cropped_im = image[:, top:bottom, left:right]

        cropped_images.append(cropped_im)

        cropped_im_size = cropped_im.shape[-2:]
        points_scale = np.array(cropped_im_size)[None, ::-1]

        points = points_grid[layer_idxs[i]] * points_scale
        normalized_points = _normalize_coordinates(target_size, points, original_size)
        total_points_per_crop.append(normalized_points)

    return cropped_images, total_points_per_crop


def _generate_crop_images(
    crop_boxes, image, points_grid, layer_idxs, target_size, original_size, input_data_format=None
):
    """
    Takes as an input bounding boxes that are used to crop the image. Based in the crops, the corresponding points are
    also passed.
    """
    cropped_images = []
    total_points_per_crop = []
    for i, crop_box in enumerate(crop_boxes):
        left, top, right, bottom = crop_box
        cropped_im = image[:, top:bottom, left:right]

        cropped_images.append(cropped_im)

        cropped_im_size = cropped_im.shape[-2:]
        points_scale = torch.tensor(cropped_im_size).flip(dims=(0,)).unsqueeze(0)

        points = points_grid[layer_idxs[i]] * points_scale
        normalized_points = _normalize_coordinates(target_size, points, original_size)
        total_points_per_crop.append(normalized_points)

    return cropped_images, total_points_per_crop


def _generate_crop_images(
    crop_boxes, image, points_grid, layer_idxs, target_size, original_size, input_data_format=None
):
    """
    Takes as an input bounding boxes that are used to crop the image. Based in the crops, the corresponding points are
    also passed.
    """
    cropped_images = []
    total_points_per_crop = []
    for i, crop_box in enumerate(crop_boxes):
        left, top, right, bottom = crop_box
        cropped_im = image[:, top:bottom, left:right]

        cropped_images.append(cropped_im)

        cropped_im_size = cropped_im.shape[-2:]
        points_scale = torch.tensor(cropped_im_size).flip(dims=(0,)).unsqueeze(0)

        points = points_grid[layer_idxs[i]] * points_scale
        normalized_points = _normalize_coordinates(target_size, points, original_size)
        total_points_per_crop.append(normalized_points)

    return cropped_images, total_points_per_crop


def _generate_crop_images(
    crop_boxes, image, points_grid, layer_idxs, target_size, original_size, input_data_format=None
):
    """
    Takes as an input bounding boxes that are used to crop the image. Based in the crops, the corresponding points are
    also passed.
    """
    cropped_images = []
    total_points_per_crop = []
    for i, crop_box in enumerate(crop_boxes):
        left, top, right, bottom = crop_box
        cropped_im = image[:, top:bottom, left:right]

        cropped_images.append(cropped_im)

        cropped_im_size = cropped_im.shape[-2:]
        points_scale = torch.tensor(cropped_im_size).flip(dims=(0,)).unsqueeze(0)

        points = points_grid[layer_idxs[i]] * points_scale
        normalized_points = _normalize_coordinates(target_size, points, original_size)
        total_points_per_crop.append(normalized_points)

    return cropped_images, total_points_per_crop

