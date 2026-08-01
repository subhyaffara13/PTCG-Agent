
def show_all_images(left_images, right_images, suffix=""):
    # Show images in two rows since display screen is horizontal in most cases.
    fig, axes = plt.subplots(nrows=2, ncols=len(left_images), figsize=(19.20, 10.80))
    for i, (left_img_path, right_img_path) in enumerate(zip(left_images, right_images, strict=False)):
        left_img = mpimg.imread(left_img_path)
        right_img = mpimg.imread(right_img_path)

        axes[0, i].imshow(left_img)
        axes[0, i].set_title(left_img_path.replace("sam2_demo_", "").replace(".png", ""), fontsize=10)
        axes[0, i].axis("off")
        axes[0, i].set_aspect(left_img.shape[1] / left_img.shape[0])

        axes[1, i].imshow(right_img)
        axes[1, i].set_title(right_img_path.replace("sam2_demo_", "").replace(".png", ""), fontsize=10)
        axes[1, i].axis("off")
        axes[1, i].set_aspect(right_img.shape[1] / right_img.shape[0])

    plt.tight_layout()
    plt.savefig(f"sam2_demo{suffix}.png", format="png", bbox_inches="tight", dpi=1000)
    plt.show()

