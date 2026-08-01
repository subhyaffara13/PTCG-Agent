
def test_scatter_offaxis_colored_pdf_size():
    """
    Test that off-axis scatter plots with per-point colors don't bloat PDFs.

    Regression test for issue #2488. When scatter points with per-point colors
    are completely outside the visible axes, the PDF backend should skip
    writing those markers to significantly reduce file size.
    """
    # Use John Hunter's birthday as random seed for reproducibility
    rng = np.random.default_rng(19680801)

    n_points = 1000
    x = rng.random(n_points) * 10
    y = rng.random(n_points) * 10
    c = rng.random(n_points)

    # Test 1: Scatter with per-point colors, all points OFF-AXIS
    fig1, ax1 = plt.subplots()
    ax1.scatter(x, y, c=c)
    ax1.set_xlim(20, 30)  # Move view completely away from data (x is 0-10)
    ax1.set_ylim(20, 30)  # Move view completely away from data (y is 0-10)

    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='pdf')
    size_offaxis_colored = buf1.tell()
    plt.close(fig1)

    # Test 2: Empty scatter (baseline - accounts for scatter call overhead)
    fig2, ax2 = plt.subplots()
    ax2.scatter([], [])  # Empty scatter to match the axes structure
    ax2.set_xlim(20, 30)
    ax2.set_ylim(20, 30)

    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='pdf')
    size_empty = buf2.tell()
    plt.close(fig2)

    # Test 3: Scatter with visible markers (should be much larger)
    fig3, ax3 = plt.subplots()
    ax3.scatter(x + 20, y + 20, c=c)  # Shift points to be visible
    ax3.set_xlim(20, 30)
    ax3.set_ylim(20, 30)

    buf3 = io.BytesIO()
    fig3.savefig(buf3, format='pdf')
    size_visible = buf3.tell()
    plt.close(fig3)

    # The off-axis colored scatter should be close to empty size.
    # Since the axes are identical, the difference should be minimal
    # (just the scatter collection setup, no actual marker data).
    # Use a tight tolerance since axes output is identical.
    assert size_offaxis_colored < size_empty + 5_000, (
        f"Off-axis colored scatter PDF ({size_offaxis_colored} bytes) is too large. "
        f"Expected close to empty scatter size ({size_empty} bytes). "
        f"Markers may not be properly skipped."
    )

    # The visible scatter should be significantly larger than both empty and
    # off-axis, demonstrating the optimization is working.
    assert size_visible > size_empty + 15_000, (
        f"Visible scatter PDF ({size_visible} bytes) should be much larger "
        f"than empty ({size_empty} bytes) to validate the test."
    )
    assert size_visible > size_offaxis_colored + 15_000, (
        f"Visible scatter PDF ({size_visible} bytes) should be much larger "
        f"than off-axis ({size_offaxis_colored} bytes) to validate optimization."
    )

