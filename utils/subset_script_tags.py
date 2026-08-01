
def subset_script_tags(self, tags):
    langsys = {}
    script_tags = set()
    for tag in tags:
        script_tag, lang_tag = tag.split(".") if "." in tag else (tag, "*")
        script_tags.add(script_tag.ljust(4))
        langsys.setdefault(script_tag, set()).add(lang_tag.ljust(4))

    if self.table.ScriptList:
        self.table.ScriptList.ScriptRecord = [
            s for s in self.table.ScriptList.ScriptRecord if s.ScriptTag in script_tags
        ]
        self.table.ScriptList.ScriptCount = len(self.table.ScriptList.ScriptRecord)

        for record in self.table.ScriptList.ScriptRecord:
            if record.ScriptTag in langsys and "*   " not in langsys[record.ScriptTag]:
                record.Script.LangSysRecord = [
                    l
                    for l in record.Script.LangSysRecord
                    if l.LangSysTag in langsys[record.ScriptTag]
                ]
                record.Script.LangSysCount = len(record.Script.LangSysRecord)
                if "dflt" not in langsys[record.ScriptTag]:
                    record.Script.DefaultLangSys = None

