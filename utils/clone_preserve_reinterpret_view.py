
def clone_preserve_reinterpret_view(x):
    reinterpret_view_layouts = []
    if isinstance(x, TensorBox) and isinstance(x.data, ir.ReinterpretView):
        x = x.data  # unwrap TensorBox
        # pyrefly: ignore [bad-assignment]
        while isinstance(x, ir.ReinterpretView):
            reinterpret_view_layouts.append(x.get_layout())
            x = x.data
        x = TensorBox(x)

    x = clone(x)

    if reinterpret_view_layouts:
        x = x.data  # unwrap TensorBox
        for layout in reinterpret_view_layouts[::-1]:
            x = ir.ReinterpretView(data=x, layout=layout)
        x = TensorBox(x)

    return x

