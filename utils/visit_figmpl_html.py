
def visit_figmpl_html(self, node):

    imagedir, srcset, rel = _copy_images_figmpl(self, node)

    # /doc/examples/subd/plot_1.rst
    docsource = PurePath(self.document['source'])
    # /doc/
    # make sure to add the trailing slash:
    srctop = PurePath(self.builder.srcdir, '')
    # examples/subd/plot_1.rst
    relsource = relpath(docsource, srctop)
    # /doc/build/html
    desttop = PurePath(self.builder.outdir, '')
    # /doc/build/html/examples/subd
    dest = desttop / relsource

    # ../../_images/ for dirhtml and ../_images/ for html
    imagerel = PurePath(relpath(imagedir, dest.parent)).as_posix()
    if self.builder.name == "dirhtml":
        imagerel = f'..{imagerel}'

    # make uri also be relative...
    nm = PurePath(node['uri'][1:]).name
    uri = f'{imagerel}/{rel}{nm}'
    img_attrs = {'src': uri, 'alt': node['alt']}

    # make srcset str.  Need to change all the prefixes!
    maxsrc = uri
    if srcset:
        maxmult = -1
        srcsetst = ''
        for mult, src in srcset.items():
            nm = PurePath(src[1:]).name
            # ../../_images/plot_1_2_0x.png
            path = f'{imagerel}/{rel}{nm}'
            srcsetst += path
            if mult == 0:
                srcsetst += ', '
            else:
                srcsetst += f' {mult:1.2f}x, '

            if mult > maxmult:
                maxmult = mult
                maxsrc = path

        # trim trailing comma and space...
        img_attrs['srcset'] = srcsetst[:-2]

    if node['class'] is not None:
        img_attrs['class'] = ' '.join(node['class'])
    for style in ['width', 'height', 'scale']:
        if node[style]:
            if 'style' not in img_attrs:
                img_attrs['style'] = f'{style}: {node[style]};'
            else:
                img_attrs['style'] += f'{style}: {node[style]};'

    # <figure class="align-default" id="id1">
    # <a class="reference internal image-reference" href="_images/index-1.2x.png">
    # <img alt="_images/index-1.2x.png"
    #  src="_images/index-1.2x.png" style="width: 53%;" />
    # </a>
    # <figcaption>
    # <p><span class="caption-text">Figure caption is here....</span>
    # <a class="headerlink" href="#id1" title="Permalink to this image">#</a></p>
    # </figcaption>
    # </figure>
    self.body.append(
        self.starttag(
            node, 'figure',
            CLASS=f'align-{node["align"]}' if node['align'] else 'align-center'))
    self.body.append(
        self.starttag(node, 'a', CLASS='reference internal image-reference',
                      href=maxsrc) +
        self.emptytag(node, 'img', **img_attrs) +
        '</a>\n')
    if node['caption']:
        self.body.append(self.starttag(node, 'figcaption'))
        self.body.append(self.starttag(node, 'p'))
        self.body.append(self.starttag(node, 'span', CLASS='caption-text'))
        self.body.append(node['caption'])
        self.body.append('</span></p></figcaption>\n')
    self.body.append('</figure>\n')

