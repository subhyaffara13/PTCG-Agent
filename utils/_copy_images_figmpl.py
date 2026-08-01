
def _copy_images_figmpl(self, node):

    # these will be the temporary place the plot-directive put the images eg:
    # ../../../build/html/plot_directive/users/explain/artists/index-1.png
    if node['srcset']:
        srcset = _parse_srcsetNodes(node['srcset'])
    else:
        srcset = None

    # the rst file's location:  eg /Users/username/matplotlib/doc/users/explain/artists
    docsource = PurePath(self.document['source']).parent

    # get the relpath relative to root:
    srctop = self.builder.srcdir
    rel = relpath(docsource, srctop).replace('.', '').replace(os.sep, '-')
    if len(rel):
        rel += '-'
    # eg: users/explain/artists

    imagedir = PurePath(self.builder.outdir, self.builder.imagedir)
    # eg: /Users/username/matplotlib/doc/build/html/_images/users/explain/artists

    Path(imagedir).mkdir(parents=True, exist_ok=True)

    # copy all the sources to the imagedir:
    if srcset:
        for src in srcset.values():
            # the entries in srcset are relative to docsource's directory
            abspath = PurePath(docsource, src)
            name = rel + abspath.name
            shutil.copyfile(abspath, imagedir / name)
    else:
        abspath = PurePath(docsource, node['uri'])
        name = rel + abspath.name
        shutil.copyfile(abspath, imagedir / name)

    return imagedir, srcset, rel

