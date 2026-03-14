#!/usr/bin/python3
'''Test flag comment.'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import sys

from .utils import *

from podict import parse

def test(msgout=sys.stdout, verbose=True):
    tests = Tests()

    @add_test(tests)
    def test_empty_1():
        po_entries, obsolete_entries, error_messages = parse('#,')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 3, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_empty_2():
        po_entries, obsolete_entries, error_messages = parse('#=')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 3, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_empty_3():
        po_entries, obsolete_entries, error_messages = parse('''#,
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_empty_4():
        po_entries, obsolete_entries, error_messages = parse('''#=
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_comma_separator_1():
        po_entries, obsolete_entries, error_messages = parse('''#,a,b,c,d
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'b', 'c', 'd' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_comma_separator_2():
        po_entries, obsolete_entries, error_messages = parse('''#=a,b,c,d
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'b', 'c', 'd' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_space_separator():
        po_entries, obsolete_entries, error_messages = parse('''#, a b\tc d
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'b', 'c', 'd' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_duplicate_flag():
        po_entries, obsolete_entries, error_messages = parse('''#, a b a b
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'b', 'a', 'b' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_multi_line():
        po_entries, obsolete_entries, error_messages = parse('''#, a b c d
#, e f g h
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' ],
                'line': 3,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_1():
        po_entries, obsolete_entries, error_messages = parse('''#, a range: 1..10 b
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range: 1..10', 'b' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_2():
        po_entries, obsolete_entries, error_messages = parse('''#, a range: 1..10x b
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range: 1..10x', 'b' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_3():
        po_entries, obsolete_entries, error_messages = parse('''#, a range: 1x..10 b
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range:', '1x..10', 'b' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_4():
        po_entries, obsolete_entries, error_messages = parse('''#, a range: 1x b
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range:', '1x', 'b' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_5():
        po_entries, obsolete_entries, error_messages = parse('''#, a range: 1.2 b
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range:', '1.2', 'b' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_6():
        po_entries, obsolete_entries, error_messages = parse('''#, a range: 1...2 b
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range:', '1...2', 'b' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_7():
        po_entries, obsolete_entries, error_messages = parse('''#, a range: a1...2 b
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range:', 'a1...2', 'b' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_8():
        po_entries, obsolete_entries, error_messages = parse('''#, a range:
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range:' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_ignore_separators():
        po_entries, obsolete_entries, error_messages = parse('''#, a range:, , 0..1
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'range: 0..1' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_eof_1():
        po_entries, obsolete_entries, error_messages = parse('#, a range:')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 12, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_eof_2():
        po_entries, obsolete_entries, error_messages = parse('#, a range: ')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 13, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_eof_3():
        po_entries, obsolete_entries, error_messages = parse('#, a range: 0')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 14, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_eof_3():
        po_entries, obsolete_entries, error_messages = parse('#, a range: 0.')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 15, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_eof_4():
        po_entries, obsolete_entries, error_messages = parse('#, a range: 0..')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 16, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_eof_5():
        po_entries, obsolete_entries, error_messages = parse('#, a range: 0..1')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 17, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_range_eof_6():
        po_entries, obsolete_entries, error_messages = parse('#, a range: 0..1 ')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 18, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_fuzzy_1():
        po_entries, obsolete_entries, error_messages = parse('''#, fuzzy
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'fuzzy' ],
                'fuzzy': True,
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_fuzzy_2():
        po_entries, obsolete_entries, error_messages = parse('''#, a, fuzzy
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'flag': [ 'a', 'fuzzy' ],
                'fuzzy': True,
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    return run_test(tests, msgout, verbose)
