
def check_output_base_name(env, output_base):
    docname = env.docname

    if '.' in output_base or '/' in output_base or '\\' in output_base:
        raise PlotError(
            f"The filename-prefix '{output_base}' is invalid. "
            f"It must not contain dots or slashes.")

    for d in env.mpl_plot_image_basenames:
        if output_base in env.mpl_plot_image_basenames[d]:
            if d == docname:
                raise PlotError(
                    f"The filename-prefix {output_base!r} is used multiple times.")
            raise PlotError(f"The filename-prefix {output_base!r} is used multiple"
                            f"times (it is also used in {env.doc2path(d)}).")

    env.mpl_plot_image_basenames[docname].add(output_base)

