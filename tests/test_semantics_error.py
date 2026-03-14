#!/usr/bin/python3
'''Test semantics errors.'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import sys

from .utils import *

from podict import parse

def test(msgout=sys.stdout, verbose=True):
    tests = Tests()

    @add_test(tests)
    def test_duplicated_entry_1():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "B"

msgctxt "context"
msgid "a"
msgstr "cA"

msgid "b"
msgstr "B2"

msgctxt ""
msgid "b"
msgstr "B3"
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
                'msgstr': [ 'B' ],
                'line': 5,
                'column': 1,
            },
            'context' + '\x04' + 'a': {
                'msgctxt': 'context',
                'msgid': 'a',
                'msgstr': [ 'cA' ],
                'line': 8,
                'column': 1,
            },
            '' + '\x04' + 'b': {
                'msgctxt': '',
                'msgid': 'b',
                'msgstr': [ 'B3' ],
                'line': 15,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 12, 1, 'Duplicate entry is found (the position of the previous entry is 5,1)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_duplicated_entry_2():
        po_entries, obsolete_entries, error_messages = parse('''
msgctxt "context"
msgid "a"
msgstr "A"

#~ msgid "b"
#~ msgstr "B"

#~ msgctxt "context"
#~ msgid "a"
#~ msgstr "cA"

msgid "b"
msgstr "B2"
''')
        good = True
        good &= po_entries == {
            'context' + '\x04' + 'a': {
                'msgctxt': 'context',
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
        }
        good &= obsolete_entries == {
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'obsolete': True,
                'line': 6,
                'column': 4,
            },
        }
        good &= error_messages == [
            ( 9, 4, 'Duplicate entry is found (the position of the previous entry is 2,1)', ),
            ( 13, 1, 'Duplicate entry is found (the position of the previous entry is 6,4)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_inconsistent_obsolete_entry_1():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b1"
#~ msgstr "B1"

#~ msgid "b2"
msgstr "B2"

#~ msgctxt "context"
msgid "c01"
msgid_plural "cp01"
msgstr[0] "C01"

msgctxt "context"
#~ msgid "c02"
msgid_plural "cp02"
msgstr[0] "C02"

#~ msgctxt "context"
#~ msgid "c03"
msgid_plural "cp03"
msgstr[0] "C03"

msgctxt "context"
msgid "c04"
#~ msgid_plural "cp04"
msgstr[0] "C04"

#~ msgctxt "context"
msgid "c05"
#~ msgid_plural "cp05"
msgstr[0] "C05"

msgctxt "context"
#~ msgid "c06"
#~ msgid_plural "cp06"
msgstr[0] "C06"

#~ msgctxt "context"
#~ msgid "c07"
#~ msgid_plural "cp07"
msgstr[0] "C07"

msgctxt "context"
msgid "c08"
msgid_plural "cp08"
#~ msgstr[0] "C08"

#~ msgctxt "context"
msgid "c09"
msgid_plural "cp09"
#~ msgstr[0] "C09"

msgctxt "context"
#~ msgid "c10"
msgid_plural "cp10"
#~ msgstr[0] "C10"

#~ msgctxt "context"
#~ msgid "c11"
msgid_plural "cp11"
#~ msgstr[0] "C11"

msgctxt "context"
msgid "c12"
#~ msgid_plural "cp12"
#~ msgstr[0] "C12"

#~ msgctxt "context"
msgid "c13"
#~ msgid_plural "cp13"
#~ msgstr[0] "C13"

msgctxt "context"
#~ msgid "c14"
#~ msgid_plural "cp14"
#~ msgstr[0] "C14"

msgid "d"
msgid_plural "d"
msgstr[0] "D0"
#~ msgstr[1] "D1"
msgstr[2] "D1"

msgid "d"
msgid_plural "d"
msgstr[0] "D0"
#~ msgstr[1] "D1"
msgstr[2] "D1"

msgid "e"
msgstr "E"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'e': {
                'msgid': 'e',
                'msgstr': [ 'E' ],
                'line': 93,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 4, 'Inconsistent #~ entry', ),
            ( 9, 1, 'Inconsistent #~ entry', ),
            ( 12, 1, 'Inconsistent #~ entry', ),
            ( 17, 4, 'Inconsistent #~ entry', ),
            ( 23, 1, 'Inconsistent #~ entry', ),
            ( 28, 4, 'Inconsistent #~ entry', ),
            ( 32, 1, 'Inconsistent #~ entry', ),
            ( 37, 4, 'Inconsistent #~ entry', ),
            ( 44, 1, 'Inconsistent #~ entry', ),
            ( 49, 4, 'Inconsistent #~ entry', ),
            ( 52, 1, 'Inconsistent #~ entry', ),
            ( 57, 4, 'Inconsistent #~ entry', ),
            ( 63, 1, 'Inconsistent #~ entry', ),
            ( 68, 4, 'Inconsistent #~ entry', ),
            ( 72, 1, 'Inconsistent #~ entry', ),
            ( 77, 4, 'Inconsistent #~ entry', ),
            ( 84, 4, 'Inconsistent #~ entry', ),
            ( 90, 4, 'Inconsistent #~ entry', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_inconsistent_obsolete_entry_2():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
msgid "b1"
#~ msgstr "B1"

#| msgid "pb"
#~ msgid "b2"
msgstr "B2"

#| msgid "pb"
#~ msgid "b3"
#~ msgstr "B3"

#~ #| msgid "pb"
msgid "b4"
msgstr "B4"

#~ #| msgid "pb"
msgid "b5"
#~ msgstr "B5"

#~ #| msgid "pb"
#~ msgid "b6"
msgstr "B6"

#| msgctxt "pcc"
#| msgid "pc"
#| msgid_plural "pcp"
msgctxt "context"
msgid "c01"
msgid_plural "cp01"
msgstr[0] "C010"
msgstr[1] "C011"
#~ msgstr[2] "C012"

#| msgctxt "pcc"
#| msgid "pc"
#| msgid_plural "pcp"
msgctxt "context"
msgid "c02"
msgid_plural "cp02"
msgstr[0] "C020"
#~ msgstr[1] "C021"
msgstr[2] "C022"

#| msgctxt "pcc"
#| msgid "pc"
#| msgid_plural "pcp"
msgctxt "context"
msgid "c03"
msgid_plural "cp03"
#~ msgstr[0] "C030"
msgstr[1] "C031"
msgstr[2] "C032"

#| msgctxt "pcc"
#| msgid "pc"
#| msgid_plural "pcp"
msgctxt "context"
msgid "c04"
#~ msgid_plural "cp04"
msgstr[0] "C040"
msgstr[1] "C041"
msgstr[2] "C042"

#| msgctxt "pcc"
#| msgid "pc"
#| msgid_plural "pcp"
msgctxt "context"
#~ msgid "c05"
msgid_plural "cp05"
msgstr[0] "C050"
msgstr[1] "C051"
msgstr[2] "C052"

#| msgctxt "pcc"
#| msgid "pc"
#| msgid_plural "pcp"
#~ msgctxt "context"
msgid "c06"
msgid_plural "cp06"
msgstr[0] "C060"
msgstr[1] "C061"
msgstr[2] "C062"

#| msgctxt "pcc"
#| msgid "pc"
#~ #| msgid_plural "pcp"
msgctxt "context"
msgid "c07"
msgid_plural "cp07"
msgstr[0] "C070"
msgstr[1] "C071"
msgstr[2] "C072"

#| msgctxt "pcc"
#~ #| msgid "pc"
#| msgid_plural "pcp"
msgctxt "context"
msgid "c08"
msgid_plural "cp08"
msgstr[0] "C080"
msgstr[1] "C081"
msgstr[2] "C082"

#~ #| msgctxt "pcc"
#| msgid "pc"
#| msgid_plural "pcp"
msgctxt "context"
msgid "c09"
msgid_plural "cp09"
msgstr[0] "C090"
msgstr[1] "C091"
msgstr[2] "C092"

#~ #| msgctxt "pcc"
#~ #| msgid "pc"
#~ #| msgid_plural "pcp"
#~ msgctxt "context"
#~ msgid "c10"
#~ msgid_plural "cp10"
#~ msgstr[0] "C100"
#~ msgstr[1] "C101"
msgstr[2] "C102"

#~ #| msgctxt "pcc"
#~ #| msgid "pc"
#~ #| msgid_plural "pcp"
#~ msgctxt "context"
#~ msgid "c11"
#~ msgid_plural "cp11"
#~ msgstr[0] "C110"
msgstr[1] "C111"
#~ msgstr[2] "C112"

#~ #| msgctxt "pcc"
#~ #| msgid "pc"
#~ #| msgid_plural "pcp"
#~ msgctxt "context"
#~ msgid "c12"
#~ msgid_plural "cp12"
msgstr[0] "C120"
#~ msgstr[1] "C121"
#~ msgstr[2] "C122"

#~ #| msgctxt "pcc"
#~ #| msgid "pc"
#~ #| msgid_plural "pcp"
#~ msgctxt "context"
#~ msgid "c13"
msgid_plural "cp13"
#~ msgstr[0] "C130"
#~ msgstr[1] "C131"
#~ msgstr[2] "C132"

#~ #| msgctxt "pcc"
#~ #| msgid "pc"
#~ #| msgid_plural "pcp"
#~ msgctxt "context"
msgid "c14"
#~ msgid_plural "cp14"
#~ msgstr[0] "C140"
#~ msgstr[1] "C141"
#~ msgstr[2] "C142"

#~ #| msgctxt "pcc"
#~ #| msgid "pc"
#~ #| msgid_plural "pcp"
msgctxt "context"
#~ msgid "c15"
#~ msgid_plural "cp15"
#~ msgstr[0] "C150"
#~ msgstr[1] "C151"
#~ msgstr[2] "C152"

#~ #| msgctxt "pcc"
#~ #| msgid "pc"
#| msgid_plural "pcp"
#~ msgctxt "context"
#~ msgid "c16"
#~ msgid_plural "cp16"
#~ msgstr[0] "C160"
#~ msgstr[1] "C161"
#~ msgstr[2] "C162"

#~ #| msgctxt "pcc"
#| msgid "pc"
#~ #| msgid_plural "pcp"
#~ msgctxt "context"
#~ msgid "c17"
#~ msgid_plural "cp17"
#~ msgstr[0] "C170"
#~ msgstr[1] "C171"
#~ msgstr[2] "C172"

#| msgctxt "pcc"
#~ #| msgid "pc"
#~ #| msgid_plural "pcp"
#~ msgctxt "context"
#~ msgid "c18"
#~ msgid_plural "cp18"
#~ msgstr[0] "C180"
#~ msgstr[1] "C181"
#~ msgstr[2] "C182"

msgid "d"
msgstr "D"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'd': {
                'msgid': 'd',
                'msgstr': [ 'D' ],
                'line': 209,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Inconsistent #~ entry', ),
            ( 10, 4, 'Inconsistent #~ entry', ),
            ( 14, 4, 'Inconsistent #~ entry', ),
            ( 18, 1, 'Inconsistent #~ entry', ),
            ( 22, 1, 'Inconsistent #~ entry', ),
            ( 27, 1, 'Inconsistent #~ entry', ),
            ( 37, 4, 'Inconsistent #~ entry', ),
            ( 46, 4, 'Inconsistent #~ entry', ),
            ( 55, 4, 'Inconsistent #~ entry', ),
            ( 64, 4, 'Inconsistent #~ entry', ),
            ( 73, 4, 'Inconsistent #~ entry', ),
            ( 82, 4, 'Inconsistent #~ entry', ),
            ( 91, 7, 'Inconsistent #~ entry', ),
            ( 100, 7, 'Inconsistent #~ entry', ),
            ( 110, 4, 'Inconsistent #~ entry', ),
            ( 127, 1, 'Inconsistent #~ entry', ),
            ( 136, 1, 'Inconsistent #~ entry', ),
            ( 145, 1, 'Inconsistent #~ entry', ),
            ( 154, 1, 'Inconsistent #~ entry', ),
            ( 163, 1, 'Inconsistent #~ entry', ),
            ( 172, 1, 'Inconsistent #~ entry', ),
            ( 181, 4, 'Inconsistent #~ entry', ),
            ( 190, 4, 'Inconsistent #~ entry', ),
            ( 200, 7, 'Inconsistent #~ entry', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_inconsistent_msgstr_n():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b1"
msgid_plural "bp1"
msgstr[0] "B0"
msgstr[1] "B1"
msgstr[2] "B2"

msgid "c1"
msgid_plural "cp1"
msgstr[1] "C1"
msgstr[2] "C2"

msgid "d1"
msgid_plural "dp1"
msgstr[0] "D0"
msgstr[2] "D2"

msgid "e1"
msgid_plural "ep1"
msgstr[0] "E0"
msgstr[0] "E1"

msgid "f"
msgstr "F"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
            },
            'b1': {
                'msgid': 'b1',
                'msgid_plural': 'bp1',
                'msgstr': [ 'B0', 'B1', 'B2', ],
                'line': 5,
                'column': 1,
            },
            'f': {
                'msgid': 'f',
                'msgstr': [ 'F' ],
                'line': 26,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 13, 1, 'Invalid n in msgstr[n]; n should be 0 but 1', ),
            ( 19, 1, 'Invalid n in msgstr[n]; n should be 1 but 2', ),
            ( 24, 1, 'Invalid n in msgstr[n]; n should be 1 but 0', ),
        ]
        return 'Some errors are detected' if not good else None

    return run_test(tests, msgout, verbose)
