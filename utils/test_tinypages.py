
def test_tinypages(tmp_path):
    shutil.copytree(tinypages, tmp_path, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('_build', 'doctrees',
                                                   'plot_directive'))
    html_dir = tmp_path / '_build' / 'html'
    img_dir = html_dir / '_images'
    doctree_dir = tmp_path / 'doctrees'

    # Build the pages with warnings turned into errors
    build_sphinx_html(tmp_path, doctree_dir, html_dir)

    def plot_file(num):
        return img_dir / f'some_plots-{num}.png'

    def plot_directive_file(num):
        # This is always next to the doctree dir.
        return doctree_dir.parent / 'plot_directive' / f'some_plots-{num}.png'

    range_10, range_6, range_4 = (plot_file(i) for i in range(1, 4))
    # Plot 5 is range(6) plot
    assert filecmp.cmp(range_6, plot_file(5))
    # Plot 7 is range(4) plot
    assert filecmp.cmp(range_4, plot_file(7))
    # Plot 11 is range(10) plot
    assert filecmp.cmp(range_10, plot_file(11))
    # Plot 12 uses the old range(10) figure and the new range(6) figure
    assert filecmp.cmp(range_10, plot_file('12_00'))
    assert filecmp.cmp(range_6, plot_file('12_01'))
    # Plot 13 shows close-figs in action
    assert filecmp.cmp(range_4, plot_file(13))
    # Plot 14 has included source
    html_contents = (html_dir / 'some_plots.html').read_text(encoding='utf-8')

    assert '# Only a comment' in html_contents
    # check plot defined in external file.
    assert filecmp.cmp(range_4, img_dir / 'range4.png')
    assert filecmp.cmp(range_6, img_dir / 'range6_range6.png')
    # check if figure caption made it into html file
    assert 'This is the caption for plot 15.' in html_contents
    # check if figure caption using :caption: made it into html file (because this plot
    # doesn't use srcset, the caption preserves newlines in the output.)
    assert 'Plot 17 uses the caption option,\nwith multi-line input.' in html_contents
    # check if figure alt text using :alt: made it into html file
    assert 'Plot 17 uses the alt option, with multi-line input.' in html_contents
    # check if figure caption made it into html file
    assert 'This is the caption for plot 18.' in html_contents
    # check if the custom classes made it into the html file
    assert 'plot-directive my-class my-other-class' in html_contents
    # check that the multi-image caption is applied twice
    assert html_contents.count('This caption applies to both plots.') == 2
    # Plot 21 is range(6) plot via an include directive. But because some of
    # the previous plots are repeated, the argument to plot_file() is only 17.
    assert filecmp.cmp(range_6, plot_file(17))
    # plot 22 is from the range6.py file again, but a different function
    assert filecmp.cmp(range_10, img_dir / 'range6_range10.png')
    # plots 23--25 use a custom basename
    assert filecmp.cmp(range_6, img_dir / 'custom-basename-6.png')
    assert filecmp.cmp(range_4, img_dir / 'custom-basename-4.png')
    assert filecmp.cmp(range_4, img_dir / 'custom-basename-4-6_00.png')
    assert filecmp.cmp(range_6, img_dir / 'custom-basename-4-6_01.png')

    # Modify the included plot
    contents = (tmp_path / 'included_plot_21.rst').read_bytes()
    contents = contents.replace(b'plt.plot(range(6))', b'plt.plot(range(4))')
    (tmp_path / 'included_plot_21.rst').write_bytes(contents)
    # Build the pages again and check that the modified file was updated
    modification_times = [plot_directive_file(i).stat().st_mtime
                          for i in (1, 2, 3, 5)]
    build_sphinx_html(tmp_path, doctree_dir, html_dir)
    assert filecmp.cmp(range_4, plot_file(17))
    # Check that the plots in the plot_directive folder weren't changed.
    # (plot_directive_file(1) won't be modified, but it will be copied to html/
    # upon compilation, so plot_file(1) will be modified)
    assert plot_directive_file(1).stat().st_mtime == modification_times[0]
    assert plot_directive_file(2).stat().st_mtime == modification_times[1]
    assert plot_directive_file(3).stat().st_mtime == modification_times[2]
    assert filecmp.cmp(range_10, plot_file(1))
    assert filecmp.cmp(range_6, plot_file(2))
    assert filecmp.cmp(range_4, plot_file(3))
    # Make sure that figures marked with context are re-created (but that the
    # contents are the same)
    assert plot_directive_file(5).stat().st_mtime > modification_times[3]
    assert filecmp.cmp(range_6, plot_file(5))

