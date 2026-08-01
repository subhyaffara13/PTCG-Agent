
def gen_blacklist():
    """Generate a list of items to blacklist.

    Methods of this type, "bandit.blacklist" plugins, are used to build a list
    of items that bandit's built in blacklisting tests will use to trigger
    issues. They replace the older blacklist* test plugins and allow
    blacklisted items to have a unique bandit ID for filtering and profile
    usage.

    :return: a dictionary mapping node types to a list of blacklist data
    """
    sets = []
    sets.append(
        utils.build_conf_dict(
            "pickle",
            "B301",
            issue.Cwe.DESERIALIZATION_OF_UNTRUSTED_DATA,
            [
                "pickle.loads",
                "pickle.load",
                "pickle.Unpickler",
                "dill.loads",
                "dill.load",
                "dill.Unpickler",
                "shelve.open",
                "shelve.DbfilenameShelf",
                "jsonpickle.decode",
                "jsonpickle.unpickler.decode",
                "jsonpickle.unpickler.Unpickler",
                "pandas.read_pickle",
            ],
            "Pickle and modules that wrap it can be unsafe when used to "
            "deserialize untrusted data, possible security issue.",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "marshal",
            "B302",
            issue.Cwe.DESERIALIZATION_OF_UNTRUSTED_DATA,
            ["marshal.load", "marshal.loads"],
            "Deserialization with the marshal module is possibly dangerous.",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "md5",
            "B303",
            issue.Cwe.BROKEN_CRYPTO,
            [
                "Crypto.Hash.MD2.new",
                "Crypto.Hash.MD4.new",
                "Crypto.Hash.MD5.new",
                "Crypto.Hash.SHA.new",
                "Cryptodome.Hash.MD2.new",
                "Cryptodome.Hash.MD4.new",
                "Cryptodome.Hash.MD5.new",
                "Cryptodome.Hash.SHA.new",
                "cryptography.hazmat.primitives.hashes.MD5",
                "cryptography.hazmat.primitives.hashes.SHA1",
            ],
            "Use of insecure MD2, MD4, MD5, or SHA1 hash function.",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "ciphers",
            "B304",
            issue.Cwe.BROKEN_CRYPTO,
            [
                "Crypto.Cipher.ARC2.new",
                "Crypto.Cipher.ARC4.new",
                "Crypto.Cipher.Blowfish.new",
                "Crypto.Cipher.DES.new",
                "Crypto.Cipher.XOR.new",
                "Cryptodome.Cipher.ARC2.new",
                "Cryptodome.Cipher.ARC4.new",
                "Cryptodome.Cipher.Blowfish.new",
                "Cryptodome.Cipher.DES.new",
                "Cryptodome.Cipher.XOR.new",
                "cryptography.hazmat.primitives.ciphers.algorithms.ARC4",
                "cryptography.hazmat.primitives.ciphers.algorithms.Blowfish",
                "cryptography.hazmat.primitives.ciphers.algorithms.CAST5",
                "cryptography.hazmat.primitives.ciphers.algorithms.IDEA",
                "cryptography.hazmat.primitives.ciphers.algorithms.SEED",
                "cryptography.hazmat.primitives.ciphers.algorithms.TripleDES",
            ],
            "Use of insecure cipher {name}. Replace with a known secure"
            " cipher such as AES.",
            "HIGH",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "cipher_modes",
            "B305",
            issue.Cwe.BROKEN_CRYPTO,
            ["cryptography.hazmat.primitives.ciphers.modes.ECB"],
            "Use of insecure cipher mode {name}.",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "mktemp_q",
            "B306",
            issue.Cwe.INSECURE_TEMP_FILE,
            ["tempfile.mktemp"],
            "Use of insecure and deprecated function (mktemp).",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "eval",
            "B307",
            issue.Cwe.OS_COMMAND_INJECTION,
            ["eval"],
            "Use of possibly insecure function - consider using safer "
            "ast.literal_eval.",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "mark_safe",
            "B308",
            issue.Cwe.XSS,
            ["django.utils.safestring.mark_safe"],
            "Use of mark_safe() may expose cross-site scripting "
            "vulnerabilities and should be reviewed.",
        )
    )

    # skipped B309 as the check for a call to httpsconnection has been removed

    sets.append(
        utils.build_conf_dict(
            "urllib_urlopen",
            "B310",
            issue.Cwe.PATH_TRAVERSAL,
            [
                "urllib.request.urlopen",
                "urllib.request.urlretrieve",
                "urllib.request.URLopener",
                "urllib.request.FancyURLopener",
                "six.moves.urllib.request.urlopen",
                "six.moves.urllib.request.urlretrieve",
                "six.moves.urllib.request.URLopener",
                "six.moves.urllib.request.FancyURLopener",
            ],
            "Audit url open for permitted schemes. Allowing use of file:/ or "
            "custom schemes is often unexpected.",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "random",
            "B311",
            issue.Cwe.INSUFFICIENT_RANDOM_VALUES,
            [
                "random.Random",
                "random.random",
                "random.randrange",
                "random.randint",
                "random.choice",
                "random.choices",
                "random.uniform",
                "random.triangular",
                "random.randbytes",
                "random.sample",
                "random.randrange",
                "random.getrandbits",
            ],
            "Standard pseudo-random generators are not suitable for "
            "security/cryptographic purposes.",
            "LOW",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "telnetlib",
            "B312",
            issue.Cwe.CLEARTEXT_TRANSMISSION,
            ["telnetlib.Telnet"],
            "Telnet-related functions are being called. Telnet is considered "
            "insecure. Use SSH or some other encrypted protocol.",
            "HIGH",
        )
    )

    # Most of this is based off of Christian Heimes' work on defusedxml:
    #   https://pypi.org/project/defusedxml/#defusedxml-sax

    xml_msg = (
        "Using {name} to parse untrusted XML data is known to be "
        "vulnerable to XML attacks. Replace {name} with its "
        "defusedxml equivalent function or make sure "
        "defusedxml.defuse_stdlib() is called"
    )

    sets.append(
        utils.build_conf_dict(
            "xml_bad_cElementTree",
            "B313",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            [
                "xml.etree.cElementTree.parse",
                "xml.etree.cElementTree.iterparse",
                "xml.etree.cElementTree.fromstring",
                "xml.etree.cElementTree.XMLParser",
            ],
            xml_msg,
        )
    )

    sets.append(
        utils.build_conf_dict(
            "xml_bad_ElementTree",
            "B314",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            [
                "xml.etree.ElementTree.parse",
                "xml.etree.ElementTree.iterparse",
                "xml.etree.ElementTree.fromstring",
                "xml.etree.ElementTree.XMLParser",
            ],
            xml_msg,
        )
    )

    sets.append(
        utils.build_conf_dict(
            "xml_bad_expatreader",
            "B315",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.sax.expatreader.create_parser"],
            xml_msg,
        )
    )

    sets.append(
        utils.build_conf_dict(
            "xml_bad_expatbuilder",
            "B316",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.dom.expatbuilder.parse", "xml.dom.expatbuilder.parseString"],
            xml_msg,
        )
    )

    sets.append(
        utils.build_conf_dict(
            "xml_bad_sax",
            "B317",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.sax.parse", "xml.sax.parseString", "xml.sax.make_parser"],
            xml_msg,
        )
    )

    sets.append(
        utils.build_conf_dict(
            "xml_bad_minidom",
            "B318",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.dom.minidom.parse", "xml.dom.minidom.parseString"],
            xml_msg,
        )
    )

    sets.append(
        utils.build_conf_dict(
            "xml_bad_pulldom",
            "B319",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.dom.pulldom.parse", "xml.dom.pulldom.parseString"],
            xml_msg,
        )
    )

    # skipped B320 as the check for a call to lxml.etree has been removed

    # end of XML tests

    sets.append(
        utils.build_conf_dict(
            "ftplib",
            "B321",
            issue.Cwe.CLEARTEXT_TRANSMISSION,
            ["ftplib.FTP"],
            "FTP-related functions are being called. FTP is considered "
            "insecure. Use SSH/SFTP/SCP or some other encrypted protocol.",
            "HIGH",
        )
    )

    # skipped B322 as the check for a call to input() has been removed

    sets.append(
        utils.build_conf_dict(
            "unverified_context",
            "B323",
            issue.Cwe.IMPROPER_CERT_VALIDATION,
            ["ssl._create_unverified_context"],
            "By default, Python will create a secure, verified ssl context for"
            " use in such classes as HTTPSConnection. However, it still allows"
            " using an insecure context via the _create_unverified_context "
            "that  reverts to the previous behavior that does not validate "
            "certificates or perform hostname checks.",
        )
    )

    # skipped B324 (used in bandit/plugins/hashlib_new_insecure_functions.py)

    # skipped B325 as the check for a call to os.tempnam and os.tmpnam have
    # been removed

    return {"Call": sets}


def gen_blacklist():
    """Generate a list of items to blacklist.

    Methods of this type, "bandit.blacklist" plugins, are used to build a list
    of items that bandit's built in blacklisting tests will use to trigger
    issues. They replace the older blacklist* test plugins and allow
    blacklisted items to have a unique bandit ID for filtering and profile
    usage.

    :return: a dictionary mapping node types to a list of blacklist data
    """
    sets = []
    sets.append(
        utils.build_conf_dict(
            "import_telnetlib",
            "B401",
            issue.Cwe.CLEARTEXT_TRANSMISSION,
            ["telnetlib"],
            "A telnet-related module is being imported.  Telnet is "
            "considered insecure. Use SSH or some other encrypted protocol.",
            "HIGH",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_ftplib",
            "B402",
            issue.Cwe.CLEARTEXT_TRANSMISSION,
            ["ftplib"],
            "A FTP-related module is being imported.  FTP is considered "
            "insecure. Use SSH/SFTP/SCP or some other encrypted protocol.",
            "HIGH",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_pickle",
            "B403",
            issue.Cwe.DESERIALIZATION_OF_UNTRUSTED_DATA,
            ["pickle", "cPickle", "dill", "shelve"],
            "Consider possible security implications associated with "
            "{name} module.",
            "LOW",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_subprocess",
            "B404",
            issue.Cwe.OS_COMMAND_INJECTION,
            ["subprocess"],
            "Consider possible security implications associated with the "
            "subprocess module.",
            "LOW",
        )
    )

    # Most of this is based off of Christian Heimes' work on defusedxml:
    #   https://pypi.org/project/defusedxml/#defusedxml-sax

    xml_msg = (
        "Using {name} to parse untrusted XML data is known to be "
        "vulnerable to XML attacks. Replace {name} with the equivalent "
        "defusedxml package, or make sure defusedxml.defuse_stdlib() "
        "is called."
    )

    sets.append(
        utils.build_conf_dict(
            "import_xml_etree",
            "B405",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.etree.cElementTree", "xml.etree.ElementTree"],
            xml_msg,
            "LOW",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_xml_sax",
            "B406",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.sax"],
            xml_msg,
            "LOW",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_xml_expat",
            "B407",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.dom.expatbuilder"],
            xml_msg,
            "LOW",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_xml_minidom",
            "B408",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.dom.minidom"],
            xml_msg,
            "LOW",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_xml_pulldom",
            "B409",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xml.dom.pulldom"],
            xml_msg,
            "LOW",
        )
    )

    # skipped B410 as the check for import_lxml has been removed

    sets.append(
        utils.build_conf_dict(
            "import_xmlrpclib",
            "B411",
            issue.Cwe.IMPROPER_INPUT_VALIDATION,
            ["xmlrpc"],
            "Using {name} to parse untrusted XML data is known to be "
            "vulnerable to XML attacks. Use defusedxml.xmlrpc.monkey_patch() "
            "function to monkey-patch xmlrpclib and mitigate XML "
            "vulnerabilities.",
            "HIGH",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_httpoxy",
            "B412",
            issue.Cwe.IMPROPER_ACCESS_CONTROL,
            [
                "wsgiref.handlers.CGIHandler",
                "twisted.web.twcgi.CGIScript",
                "twisted.web.twcgi.CGIDirectory",
            ],
            "Consider possible security implications associated with "
            "{name} module.",
            "HIGH",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_pycrypto",
            "B413",
            issue.Cwe.BROKEN_CRYPTO,
            [
                "Crypto.Cipher",
                "Crypto.Hash",
                "Crypto.IO",
                "Crypto.Protocol",
                "Crypto.PublicKey",
                "Crypto.Random",
                "Crypto.Signature",
                "Crypto.Util",
            ],
            "The pyCrypto library and its module {name} are no longer actively"
            " maintained and have been deprecated. "
            "Consider using pyca/cryptography library.",
            "HIGH",
        )
    )

    sets.append(
        utils.build_conf_dict(
            "import_pyghmi",
            "B415",
            issue.Cwe.CLEARTEXT_TRANSMISSION,
            ["pyghmi"],
            "An IPMI-related module is being imported. IPMI is considered "
            "insecure. Use an encrypted protocol.",
            "HIGH",
        )
    )

    return {"Import": sets, "ImportFrom": sets, "Call": sets}

