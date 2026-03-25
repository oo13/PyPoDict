#!/usr/bin/python3
'''Test white spaces.'''
import sys

from .utils import *

from podict import parse

def test(msgout=sys.stdout, verbose=True):
    tests = Tests()

    @add_test(tests)
    def test_newline():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"newline error
next line"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 15, 'The text may not contain a newline', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_newline_EOF():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"newline error
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 15, 'The text may not contain a newline', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_EOF():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"\\''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 3, 'Invalid escape sequence', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_a():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\a2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\a2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_b():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\b2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\b2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_f():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\f2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\f2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_n():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\n2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\n2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_r():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\r2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\r2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_t():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\t2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\t2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_v():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\v2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\v2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_backslash():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\\\2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\\2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_single_quote():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\'2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1\'2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_double_quote():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\"2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1"2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_double_question():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\?2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ '1?2' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_invalid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"1\\c2"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Invalid escape sequence', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_octal_1():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\7y"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'x\x07y' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_octal_2():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\17y"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'x\x0Fy' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_octal_3():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\117y"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'x\x4Fy' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_octal_4():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\1171y"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'x\x4F' + '1y' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_octal_EOF_1():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\1''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 5, 'Closing double quotation mark is expected', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_octal_EOF_2():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\11''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 6, 'Closing double quotation mark is expected', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_octal_EOF_3():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\111''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 7, 'Closing double quotation mark is expected', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_octal_EOF_4():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\1111''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 8, 'Closing double quotation mark is expected', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_0_1():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\xy"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 5, 'Invalid escape sequence', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_0_2():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\x"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 5, 'Invalid escape sequence', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_1():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\xay"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'x\x0Ay' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_2():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\x7by"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'x\x7By' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_3():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\xa6Cy"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'x\x6Cy' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_4():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\x0123456789ABCDEFabcdef76y"

msgid "c"
msgstr "C"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'x\x76y' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_EOF_0():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\x''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 5, 'Invalid escape sequence', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_EOF_1():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\xA''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 6, 'Closing double quotation mark is expected', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_EOF_2():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\xAB''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 7, 'Closing double quotation mark is expected', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_EOF_3():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\xAbC''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 8, 'Closing double quotation mark is expected', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_EOF_4():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr ""
"x\\x0123456789ABCDEFabcdef''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 27, 'Closing double quotation mark is expected', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_oct_utf_8_encoding():
        po_entries, obsolete_entries, error_messages = parse('''
#| msgctxt "\\xe3\\x81\\x82"
#| msgid "\\343\\201\\204"
#| msgid_plural "\\xe3\\x81\\x86"
msgctxt "\\xe3\\x81\\x88"
msgid "\\xe3\\x81\\x8A"
msgid_plural "\\xe3\\x81\\x8B"
msgstr[0] "\\xe3\\x81\\x8D"

msgid "b"
msgstr "\\xe3\\x81\\x8F"
''')
        good = True
        good &= po_entries == {
            'え' + '\x04' + 'お' : {
                'msgctxt': 'え',
                'msgid': 'お',
                'msgid_plural': 'か',
                'msgstr': [ 'き' ],
                'line': 5,
                'column': 1,
                'prev_msgctxt': 'あ',
                'prev_msgid': 'い',
                'prev_msgid_plural': 'う',
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'く' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_concat_and_escape_hex_oct_utf_8_encoding():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "\\xe3" "\\x81" "\\x82" "0\\xe3" "\\x81" "\\x84"
msgid_plural "\\xe3" "\\x81" "\\x86Z" "X\\xe3\\x81\\x88"
msgstr[0] ""
"Z\\xe3" "\\x81\\x8A"
msgstr[1] ""
"Z\\xe3\\x81\\x8B" "X\\xe3\\x81\\x8D"
msgstr[2] ""
"Z" "\\xe3\\x81\\x8FX"
msgstr[3] ""
"Z\\xe3\\x81\\x91" ""
msgstr[4] ""
"Z\\xe3\\x81\\x93" "\\xe3\\x81\\x95"
msgstr[5] ""
"Z" "\\xe3\\x81\\x97"
''')
        good = True
        good &= po_entries == {
            'あ0い': {
                'msgid': 'あ0い',
                'msgid_plural': 'うZXえ',
                'msgstr': [ 'Zお', 'ZかXき', 'ZくX', 'Zけ', 'Zこさ', 'Zし' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_escape_hex_oct_invalid_utf_8_encoding():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "\\xe3" "\\x81" "\\xE2" "0\\xe3" "\\xF1" "\\x84"
msgid_plural "\\xe3" "\\xF1" "\\x86Z" "X\\xe3\\xF1\\x88"
msgstr[0] ""
"Z\\xe3" "\\x81\\x4A"
msgstr[1] ""
"Z\\x43\\x81\\x8B" "X\\xe3\\xF1\\x8D"
msgstr[2] ""
"Z" "\\x43\\x81\\x8FX"
msgstr[3] ""
"Z\\xe3\\xE1\\x91" ""
msgstr[4] ""
"Z\\xe3\\x81\\xE3" "\\xe3\\xF1\\x95"
msgstr[5] ""
"Z" "\\xe3\\xD1\\x97"
''')
        good = True
        good &= po_entries == {
            '�0�': {
                'msgid': '�0�',
                'msgid_plural': '�ZX�',
                'msgstr': [ 'Z�', 'Z�X�', 'Z�X', 'Z�', 'Z�', 'Z�' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        if len(error_messages) == 8:
            good &= error_messages[0][0:2] == (2, 8, )
            good &= error_messages[1][0:2] == (3, 15, )
            good &= error_messages[2][0:2] == (5, 3, )
            good &= error_messages[3][0:2] == (7, 3, )
            good &= error_messages[4][0:2] == (9, 6, )
            good &= error_messages[5][0:2] == (11, 3, )
            good &= error_messages[6][0:2] == (13, 3, )
            good &= error_messages[7][0:2] == (15, 6, )
        else:
            good = False
        return 'Some errors are detected' if not good else None

    return run_test(tests, msgout, verbose)
