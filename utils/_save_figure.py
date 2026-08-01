
def _save_figure(objects='mhip', fmt="pdf", usetex=False):
    mpl.use(fmt)
    mpl.rcParams.update({'svg.hashsalt': 'asdf', 'text.usetex': usetex})

    def plot_markers(fig):
        # use different markers...
        ax = fig.add_subplot()
        x = range(10)
        ax.plot(x, [1] * 10, marker='D')
        ax.plot(x, [2] * 10, marker='x')
        ax.plot(x, [3] * 10, marker='^')
        ax.plot(x, [4] * 10, marker='H')
        ax.plot(x, [5] * 10, marker='v')

    def plot_hatch(fig):
        # also use different hatch patterns
        ax2 = fig.add_subplot()
        bars = (ax2.bar(range(1, 5), range(1, 5)) +
                ax2.bar(range(1, 5), [6] * 4, bottom=range(1, 5)))
        ax2.set_xticks([1.5, 2.5, 3.5, 4.5])

        patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
        for bar, pattern in zip(bars, patterns):
            bar.set_hatch(pattern)

    def plot_image(fig):
        axs = fig.subplots(1, 3, sharex=True, sharey=True)
        # also use different images
        A = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        axs[0].imshow(A, interpolation='nearest')
        A = [[1, 3, 2], [1, 2, 3], [3, 1, 2]]
        axs[1].imshow(A, interpolation='bilinear')
        A = [[2, 3, 1], [1, 2, 3], [2, 1, 3]]
        axs[2].imshow(A, interpolation='bicubic')

    def plot_paths(fig):
        # clipping support class, copied from demo_text_path.py gallery example
        class PathClippedImagePatch(PathPatch):
            """
            The given image is used to draw the face of the patch. Internally,
            it uses BboxImage whose clippath set to the path of the patch.

            FIXME : The result is currently dpi dependent.
            """

            def __init__(self, path, bbox_image, **kwargs):
                super().__init__(path, **kwargs)
                self.bbox_image = BboxImage(
                    self.get_window_extent, norm=None, origin=None)
                self.bbox_image.set_data(bbox_image)

            def set_facecolor(self, color):
                """Simply ignore facecolor."""
                super().set_facecolor("none")

            def draw(self, renderer=None):
                # the clip path must be updated every draw. any solution? -JJ
                self.bbox_image.set_clip_path(self._path, self.get_transform())
                self.bbox_image.draw(renderer)
                super().draw(renderer)

        subfigs = fig.subfigures(1, 3)

        # add a polar projection
        px = subfigs[0].add_subplot(projection="polar")
        pimg = px.imshow([[2]])
        pimg.set_clip_path(Circle((0, 1), radius=0.3333))

        # add a text-based clipping path (origin: demo_text_path.py)
        ax = subfigs[1].add_subplot()
        arr = plt.imread(get_sample_data("grace_hopper.jpg"))
        text_path = TextPath((0, 0), "!?", size=150)
        p = PathClippedImagePatch(text_path, arr, ec="k")
        offsetbox = AuxTransformBox(IdentityTransform())
        offsetbox.add_artist(p)
        ao = AnchoredOffsetbox(loc='upper left', child=offsetbox, frameon=True,
                               borderpad=0.2)
        ax.add_artist(ao)

        # add a 2x2 grid of path-clipped axes (origin: test_artist.py)
        exterior = Path.unit_rectangle().deepcopy()
        exterior.vertices *= 4
        exterior.vertices -= 2
        interior = Path.unit_circle().deepcopy()
        interior.vertices = interior.vertices[::-1]
        clip_path = Path.make_compound_path(exterior, interior)

        star = Path.unit_regular_star(6).deepcopy()
        star.vertices *= 2.6

        (row1, row2) = subfigs[2].subplots(2, 2, sharex=True, sharey=True,
                                           gridspec_kw=dict(hspace=0, wspace=0))
        for row in (row1, row2):
            ax1, ax2 = row
            collection = PathCollection([star], lw=5, edgecolor='blue',
                                        facecolor='red', alpha=0.7, hatch='*')
            collection.set_clip_path(clip_path, ax1.transData)
            ax1.add_collection(collection)

            patch = PathPatch(star, lw=5, edgecolor='blue', facecolor='red',
                              alpha=0.7, hatch='*')
            patch.set_clip_path(clip_path, ax2.transData)
            ax2.add_patch(patch)

            ax1.set_xlim([-3, 3])
            ax1.set_ylim([-3, 3])

    nfigs = len(objects) + 1
    fig = plt.figure(figsize=(7, 3 * nfigs))
    subfigs = iter(fig.subfigures(nfigs, squeeze=False).flat)
    fig.subplots_adjust(bottom=0.15)

    if 'm' in objects:
        plot_markers(next(subfigs))
    if 'h' in objects:
        plot_hatch(next(subfigs))
    if 'i' in objects:
        plot_image(next(subfigs))
    if 'p' in objects:
        plot_paths(next(subfigs))

    x = range(5)
    ax = next(subfigs).add_subplot()
    ax.plot(x, x)
    ax.set_title('A string $1+2+\\sigma$')
    ax.set_xlabel('A string $1+2+\\sigma$')
    ax.set_ylabel('A string $1+2+\\sigma$')

    stdout = getattr(sys.stdout, 'buffer', sys.stdout)
    fig.savefig(stdout, format=fmt)


def _save_figure(fig: "go.Figure", output_path: Union[str, List[str], None], width=None, height=None):
    """Saves a Plotly figure to one or multiple files.

    Args:
        fig: The Plotly Figure object.
        output_path: A single filename (str) or a list of filenames (List[str]).
        width: Width of the output image.
        height: Height of the output image.
    """
    if not output_path:
        return

    # Handle multiple paths (recursion)
    if isinstance(output_path, (list, tuple)):
        for path in output_path:
            _save_figure(fig, path, width, height)
        return

    # Handle single path
    ext = os.path.splitext(output_path)[1].lower()
    try:
        if ext == ".html":
            fig.write_html(output_path)
        elif ext in [".png", ".jpg", ".jpeg"]:
            # scale=3 ensures high DPI (Retina quality)
            fig.write_image(output_path, width=width, height=height, scale=3)
        elif ext in [".pdf", ".svg"]:
            fig.write_image(output_path, width=width, height=height)
        else:
            print(f"Unknown format {ext}, defaulting to HTML.")
            fig.write_html(output_path + ".html")
        print(f"Saved chart to {output_path}")
    except ValueError as e:
        print(f"Error saving to {output_path} (did you install 'kaleido'?): {e}")

