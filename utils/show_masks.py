
def show_masks(
    image,
    masks,
    scores,
    point_coords=None,
    box_coords=None,
    input_labels=None,
    borders=True,
    output_image_file_prefix=None,
    image_files=None,
):
    for i, (mask, score) in enumerate(zip(masks, scores, strict=False)):
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        show_mask(mask, plt.gca(), borders=borders)
        if point_coords is not None:
            assert input_labels is not None
            show_points(point_coords, input_labels, plt.gca())

        if box_coords is not None:
            show_box(box_coords, plt.gca())

        if len(scores) > 1:
            plt.title(f"Mask {i + 1}, Score: {score:.3f}", fontsize=18)

        plt.axis("off")
        if output_image_file_prefix:
            filename = f"{output_image_file_prefix}_{i}.png"
            if os.path.exists(filename):
                os.remove(filename)
            plt.savefig(filename, format="png", bbox_inches="tight", pad_inches=0)
            if isinstance(image_files, list):
                image_files.append(filename)
        plt.show(block=False)
        plt.close()

