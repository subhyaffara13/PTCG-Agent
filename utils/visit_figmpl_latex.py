
def visit_figmpl_latex(self, node):

    if node['srcset'] is not None:
        imagedir, srcset = _copy_images_figmpl(self, node)
        maxmult = -1
        # choose the highest res version for latex:
        maxmult = max(srcset, default=-1)
        node['uri'] = PurePath(srcset[maxmult]).name

    self.visit_figure(node)

