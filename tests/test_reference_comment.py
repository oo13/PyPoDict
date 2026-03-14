#!/usr/bin/python3
'''Test reference comment.'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import sys

from .utils import *

from podict import parse
from podict.dump import dumps

def test(msgout=sys.stdout, verbose=True):
    tests = Tests()

    @add_test(tests)
    def test_empty_1():
        po_entries, obsolete_entries, error_messages = parse('#:')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 3, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_empty_2():
        po_entries, obsolete_entries, error_messages = parse('''#:
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'reference': [],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_separators():
        po_entries, obsolete_entries, error_messages = parse('''#: f1:1 f2:2 \t f3:3\t \tf4:4
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'reference': [ ( 'f1', '1', ), ( 'f2', '2', ), ( 'f3', '3', ), ( 'f4', '4', ) ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None


    @add_test(tests)
    def test_no_reference_line():
        po_entries, obsolete_entries, error_messages = parse('''#: f1:1 f2: f3:3 f4
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'reference': [ ( 'f1', '1', ), ( 'f2:', None, ), ( 'f3', '3', ), ( 'f4', None, ) ],
                'line': 2,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_multi_lines():
        po_entries, obsolete_entries, error_messages = parse('''#: f1:1 f2:2
#: f3:3 f4:4
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'reference': [ ( 'f1', '1', ), ( 'f2', '2', ), ( 'f3', '3', ), ( 'f4', '4', ) ],
                'line': 3,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_separation_file_and_line():
        po_entries, obsolete_entries, error_messages = parse('''#: f1:1 f2:1:2
#: f3: 0a f4: 01 f5 :0b f6 :12 f7 : 0c f8 : 13 f:9: 1a0 f:10: 10
#: f:11 :1b4 f:12 :15 :f13: 1a0 :f14: 16 :10 :10x
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'reference': [
                    ( 'f1', '1', ),
                    ( 'f2:1', '2', ),
                    ( 'f3:', None, ),
                    ( '0a', None, ),
                    ( 'f4', '01', ),
                    ( 'f5', None, ),
                    ( ':0b', None, ),
                    ( 'f6', '12', ),
                    ( 'f7', None, ),
                    ( ':', None, ),
                    ( '0c', None, ),
                    ( 'f8', '13', ),
                    ( 'f:9:', None, ),
                    ( '1a0', None, ),
                    ( 'f:10', '10', ),
                    ( 'f', '11', ),
                    ( ':1b4', None, ),
                    ( 'f:12', '15', ),
                    ( ':f13:', None, ),
                    ( '1a0', None, ),
                    ( ':f14', '16', ),
                    ( '', '10', ),
                    ( ':10x', None, ),
                ],
                'line': 4,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_independent_colon():
        po_entries, obsolete_entries, error_messages = parse('''#: :
#: : 10
#: : 1x0
#: f:1 :
#: f:2 : 10
#: f:3 : 1x0
#: : :
#: : : :
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'reference': [
                    ( ':', None, ),
                    ( '', '10', ),
                    ( ':', None, ),
                    ( '1x0', None, ),
                    ( 'f', '1', ),
                    ( ':', None, ),
                    ( 'f:2', '10', ),
                    ( 'f', '3', ),
                    ( ':', None, ),
                    ( '1x0', None, ),
                    ( ':', None, ),
                    ( ':', None, ),
                    ( ':', None, ),
                    ( ':', None, ),
                    ( ':', None, ),
                ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_quotation():
        po_entries, obsolete_entries, error_messages = parse('''#: \u2068f 1\u2069: 10
#: \u2068f 2\u2069: \u206811\u2069
#: \u2068f 3\u2069x: 12
#: x\u2068f 4\u2069:13
#: f5 \u2068:\u2069 14
#: \u2068f6:\u2069 15
#: \u2068f7: 16
#: f8\u2069: 17
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'reference': [
                    ( 'f 1', '10', ),
                    ( 'f 2', None, ),
                    ( ':', None, ),
                    ( '11', None, ),
                    ( 'f 3', None, ),
                    ( 'x', '12', ),
                    ( 'x\u2068f', None, ),
                    ( '4\u2069', '13', ),
                    ( 'f5', None, ),
                    ( ':', None, ),
                    ( '14', None, ),
                    ( 'f6:', None, ),
                    ( '15', None, ),
                    ( 'f7: 16', None, ),
                    ( 'f8\u2069', '17', ),
                ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_dump_quotation():
        po_entries, obsolete_entries, error_messages = parse('''#: \u2068f 1\u2069:10
#: \u2068f\t2\u2069:11
#: \u2068f3\u2069:12
msgid "a"
msgstr "b"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'b' ],
                'reference': [ ( 'f 1', '10', ), ( 'f\t2', '11', ), ( 'f3', '12', ), ],
                'line': 4,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''#: \u2068f 1\u2069:10 \u2068f\t2\u2069:11 f3:12
msgid "a"
msgstr "b"
'''
        return 'Some errors are detected' if not good else None

    return run_test(tests, msgout, verbose)
