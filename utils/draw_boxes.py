
def draw_boxes(disp_image, boxes, labels=None):
    # xyxy format
    num_boxes = boxes.shape[0]
    list_gt = range(num_boxes)
    for i in list_gt:
        disp_image = _draw_single_box(
            disp_image,
            boxes[i, 0],
            boxes[i, 1],
            boxes[i, 2],
            boxes[i, 3],
            display_str=None if labels is None else labels[i],
            color="Red",
        )
    return disp_image

