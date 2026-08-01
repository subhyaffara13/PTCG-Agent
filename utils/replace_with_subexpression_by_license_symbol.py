
def replace_with_subexpression_by_license_symbol(tokens, strict=False):
    """
    Given a ``tokens`` iterable of Token, yield updated Token(s) replacing any
    "XXX WITH ZZZ" subexpression by a LicenseWithExceptionSymbol symbol.

    Check validity of WITH subexpessions and raise ParseError on errors.

    If ``strict`` is True also raise ParseError if the left hand side
    LicenseSymbol has `is_exception` True or if the right hand side
    LicenseSymbol has `is_exception` False.
    """
    token_groups = build_token_groups_for_with_subexpression(tokens)

    for token_group in token_groups:
        len_group = len(token_group)

        if not len_group:
            # This should never happen
            continue

        if len_group == 1:
            # a single token
            token = token_group[0]
            tval = token.value

            if isinstance(tval, Keyword):
                if tval.type == TOKEN_WITH:
                    # keyword
                    # a single group cannot be a single 'WITH' keyword:
                    # this is an error that we catch and raise here.
                    raise ParseError(
                        token_type=TOKEN_WITH,
                        token_string=token.string,
                        position=token.start,
                        error_code=PARSE_INVALID_EXPRESSION,
                    )

            elif isinstance(tval, LicenseSymbol):
                if strict and tval.is_exception:
                    raise ParseError(
                        token_type=TOKEN_SYMBOL,
                        token_string=token.string,
                        position=token.start,
                        error_code=PARSE_INVALID_EXCEPTION,
                    )

            else:
                # this should not be possible by design
                raise Exception(f"Licensing.tokenize is internally confused...: {tval!r}")

            yield token
            continue

        if len_group != 3:
            # this should never happen
            string = " ".join([tok.string for tok in token_group])
            start = token_group[0].start
            raise ParseError(
                token_type=TOKEN_SYMBOL,
                token_string=string,
                position=start,
                error_code=PARSE_INVALID_EXPRESSION,
            )

        # from now on we have a tripple of tokens: a WITH sub-expression such as
        # "A with B" seq of three tokens
        lic_token, WITH, exc_token = token_group

        lic = lic_token.string
        exc = exc_token.string
        WITH = WITH.string.strip()
        token_string = f"{lic} {WITH} {exc}"

        # the left hand side license symbol
        lic_sym = lic_token.value

        # this should not happen
        if not isinstance(lic_sym, LicenseSymbol):
            raise ParseError(
                token_type=TOKEN_SYMBOL,
                token_string=lic_token.string,
                position=lic_token.start,
                error_code=PARSE_INVALID_SYMBOL,
            )

        if strict and lic_sym.is_exception:
            raise ParseError(
                token_type=TOKEN_SYMBOL,
                token_string=lic_token.string,
                position=lic_token.start,
                error_code=PARSE_INVALID_EXCEPTION,
            )

        # the right hand side exception symbol
        exc_sym = exc_token.value

        if not isinstance(exc_sym, LicenseSymbol):
            raise ParseError(
                token_type=TOKEN_SYMBOL,
                token_string=lic_sym.string,
                position=lic_sym.start,
                error_code=PARSE_INVALID_SYMBOL,
            )

        if strict and not exc_sym.is_exception:
            raise ParseError(
                token_type=TOKEN_SYMBOL,
                token_string=exc_token.string,
                position=exc_token.start,
                error_code=PARSE_INVALID_SYMBOL_AS_EXCEPTION,
            )

        lic_exc_sym = LicenseWithExceptionSymbol(
            license_symbol=lic_sym,
            exception_symbol=exc_sym,
            strict=strict,
        )

        token = Token(
            start=lic_token.start,
            end=exc_token.end,
            string=token_string,
            value=lic_exc_sym,
        )
        yield token

