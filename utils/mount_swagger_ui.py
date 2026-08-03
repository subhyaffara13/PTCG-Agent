import json
import os

def mount_swagger_ui():
    swagger_directory = os.path.join(current_dir, "swagger")
    swagger_path = "/" if server_root_path is None else server_root_path
    if not swagger_path.endswith("/"):
        swagger_path = swagger_path + "/"
    custom_root_path_swagger_path = swagger_path + "swagger"

    app.mount("/swagger", StaticFiles(directory=swagger_directory), name="swagger")

    # On dropdown expand: one-time fetch to the prefix (triggers lazy load),
    # then spec re-download so real routes replace the stub. Raw JS (no
    # <script> tag) since it's injected inside the existing inline script.
    from fastapi.responses import HTMLResponse

    from litellm.proxy._lazy_features import lazy_tag_to_prefix

    _lazy_plugin_js = (
        "const TAG_TO_PREFIX = " + json.dumps(lazy_tag_to_prefix()) + ";"
        "const warmedTags = new Set();"
        "const LAZY_TAGS = new Set(Object.keys(TAG_TO_PREFIX));"
        "const hideStubRows = () => {"
        "document.querySelectorAll('.opblock').forEach(op => {"
        "const d = op.querySelector('.opblock-summary-description');"
        "if (d && LAZY_TAGS.has(d.textContent.trim())) op.style.display = 'none';"
        "});};"
        "const annotateLazyHeaders = () => {"
        "document.querySelectorAll('.opblock-tag').forEach(tagEl => {"
        "const m = (tagEl.id || '').match(/^operations-tag-(.+)$/);"
        "if (!m || !LAZY_TAGS.has(m[1])) return;"
        "const existing = tagEl.querySelector('.lazy-load-hint');"
        "if (warmedTags.has(m[1])) { if (existing) existing.remove(); return; }"
        "if (existing) return;"
        "const hint = document.createElement('small');"
        "hint.className = 'lazy-load-hint';"
        "hint.textContent = ' (expand to load routes)';"
        "hint.style.opacity = '0.6';"
        "hint.style.marginLeft = '6px';"
        "const target = tagEl.querySelector('a span') || tagEl.querySelector('span') || tagEl;"
        "target.appendChild(hint);"
        "});};"
        "setInterval(() => { hideStubRows(); annotateLazyHeaders(); }, 200);"
        "const LazyLoadPlugin = () => ({"
        "afterLoad:function(system){setTimeout(()=>{"
        "for(const tag of LAZY_TAGS)system.layoutActions.show(['operations-tag',tag],false);"
        "},200);},"
        "statePlugins:{layout:{wrapActions:{show:(ori,sys)=>(...args)=>{"
        "const thing=args[0];const shown=args[1];let tag=null;"
        "if(Array.isArray(thing)){for(const t of thing)if(TAG_TO_PREFIX[t])tag=t;}"
        "if(shown!==false&&tag&&!warmedTags.has(tag)){warmedTags.add(tag);"
        "fetch('/lazy/warm/'+tag,{method:'POST',credentials:'include'}).then(r=>r.json()).then(d=>{"
        "if(!d.paths||Object.keys(d.paths).length===0)return;"
        "const cur=sys.specSelectors.specJson().toJS();"
        "const merged={};let inserted=false;"
        "for(const k in (cur.paths||{})){"
        "if(k===d.stub_path){for(const nk in d.paths)merged[nk]=d.paths[nk];inserted=true;}"
        "else{merged[k]=cur.paths[k];}}"
        "if(!inserted)Object.assign(merged,d.paths);"
        "cur.paths=merged;"
        "cur.components=cur.components||{};"
        "cur.components.schemas=Object.assign(cur.components.schemas||{},(d.components||{}).schemas||{});"
        "sys.specActions.updateSpec(JSON.stringify(cur));"
        "}).catch(()=>{});}"
        "return ori(...args);}}}}});"
    )

    def swagger_monkey_patch(*args, **kwargs):
        response = get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_js_url=f"{custom_root_path_swagger_path}/swagger-ui-bundle.js",
            swagger_css_url=f"{custom_root_path_swagger_path}/swagger-ui.css",
            swagger_favicon_url=f"{custom_root_path_swagger_path}/favicon.png",
        )
        body = response.body.decode("utf-8")
        body = body.replace(
            "const ui = SwaggerUIBundle({",
            _lazy_plugin_js
            + 'const ui = SwaggerUIBundle({plugins:[LazyLoadPlugin],tagsSorter:"alpha",',
            1,
        )
        return HTMLResponse(content=body)

    applications.get_swagger_ui_html = swagger_monkey_patch

