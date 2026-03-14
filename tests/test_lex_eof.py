#!/usr/bin/python3
'''Test EOF in lex.'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import sys

from .utils import *

from podict import parse

def test(msgout=sys.stdout, verbose=True):
    tests = Tests()

    @add_test(tests)
    def test_empty_string():
        po_entries, obsolete_entries, error_messages = parse('')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_space():
        po_entries, obsolete_entries, error_messages = parse(' ')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_newline():
        po_entries, obsolete_entries, error_messages = parse('\n')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_newline_and_space():
        po_entries, obsolete_entries, error_messages = parse('\n ')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_comment():
        po_entries, obsolete_entries, error_messages = parse('# aaa')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 6, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_obsolete_comment():
        po_entries, obsolete_entries, error_messages = parse('#~')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_prev_comment():
        po_entries, obsolete_entries, error_messages = parse('#|')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_obosolete_prev_comment():
        po_entries, obsolete_entries, error_messages = parse('#~|')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msg_1():
        po_entries, obsolete_entries, error_messages = parse('m')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msg_2():
        po_entries, obsolete_entries, error_messages = parse('ms')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msg_3():
        po_entries, obsolete_entries, error_messages = parse('msg')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_quoted_text():
        po_entries, obsolete_entries, error_messages = parse('"')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 2, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgctxt_1():
        po_entries, obsolete_entries, error_messages = parse('msgc')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgctxt_2():
        po_entries, obsolete_entries, error_messages = parse('msgct')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgctxt_3():
        po_entries, obsolete_entries, error_messages = parse('msgctx')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgctxt_4():
        po_entries, obsolete_entries, error_messages = parse('msgctxt')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 8, 'Unexpected EOF (quoted text is expected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_1():
        po_entries, obsolete_entries, error_messages = parse('msgi')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_2():
        po_entries, obsolete_entries, error_messages = parse('msgid')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 6, 'Unexpected EOF (quoted text is expected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_plural_1():
        po_entries, obsolete_entries, error_messages = parse('msgid_')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_plural_2():
        po_entries, obsolete_entries, error_messages = parse('msgid_p')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_plural_3():
        po_entries, obsolete_entries, error_messages = parse('msgid_pl')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_plural_4():
        po_entries, obsolete_entries, error_messages = parse('msgid_plu')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_plural_5():
        po_entries, obsolete_entries, error_messages = parse('msgid_plur')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_plural_6():
        po_entries, obsolete_entries, error_messages = parse('msgid_plura')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgid_plural_7():
        po_entries, obsolete_entries, error_messages = parse('msgid_plural')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unexpected msgid_plural', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgstr_1():
        po_entries, obsolete_entries, error_messages = parse('msgs')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgstr_2():
        po_entries, obsolete_entries, error_messages = parse('msgst')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unknown keyword', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgstr_3():
        po_entries, obsolete_entries, error_messages = parse('msgstr')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unexpected msgstr', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgstr_plural_1():
        po_entries, obsolete_entries, error_messages = parse('msgstr[')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 8, "'0'..'9' is expected", )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgstr_plural_2():
        po_entries, obsolete_entries, error_messages = parse('msgstr[0')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 9, "'0'..'9' or ']' is expected", )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_msgstr_plural_3():
        po_entries, obsolete_entries, error_messages = parse('msgstr[0]')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unexpected msgstr[n]', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_text():
        po_entries, obsolete_entries, error_messages = parse('"text')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 6, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_newline_in_text():
        po_entries, obsolete_entries, error_messages = parse('"\n')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 2, 'The text may not contain a newline', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_end_of_quoted_text():
        po_entries, obsolete_entries, error_messages = parse('""')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unexpected quoted text', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_char_in_text():
        po_entries, obsolete_entries, error_messages = parse('"\\')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 3, 'Invalid escape sequence', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_oct_digit_in_text_1():
        po_entries, obsolete_entries, error_messages = parse('"\\1')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 4, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_oct_digit_in_text_2():
        po_entries, obsolete_entries, error_messages = parse('"\\11')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 5, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_oct_digit_in_text_3():
        po_entries, obsolete_entries, error_messages = parse('"\\111')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 6, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_oct_digit_in_text_4():
        po_entries, obsolete_entries, error_messages = parse('"\\1111')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 7, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_hex_digit_in_text_1():
        po_entries, obsolete_entries, error_messages = parse('"\\x')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 4, 'Invalid escape sequence', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_hex_digit_in_text_2():
        po_entries, obsolete_entries, error_messages = parse('"\\xa')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 5, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_hex_digit_in_text_3():
        po_entries, obsolete_entries, error_messages = parse('"\\xab')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 6, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_hex_digit_in_text_4():
        po_entries, obsolete_entries, error_messages = parse('"\\xabc')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 7, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_hex_digit_in_text_5():
        po_entries, obsolete_entries, error_messages = parse('"\\xabcx')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 8, 'Closing double quotation mark is expected', )
        ]
        return 'Some errors are detected' if not good else None

    return run_test(tests, msgout, verbose)
