#!/usr/bin/python3
'''Test normal entries.'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import sys

from .utils import *

from podict import parse
from podict.dump import dumps

def test(msgout=sys.stdout, verbose=True):
    tests = Tests()

    @add_test(tests)
    def test_a_normal_entry():
        po_entries, obsolete_entries, error_messages = parse('''msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            '1': {
                'msgid': '1',
                'msgstr': [ '2' ],
                'line': 1,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''msgctxt "c"
msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'line': 1,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''msgctxt "c"
msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''msgctxt "c"
msgid "1"
msgid_plural "2"
msgstr[0] "3"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgid_plural': '2',
                'msgstr': [ '3' ],
                'line': 1,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''msgctxt "c"
msgid "1"
msgid_plural "2"
msgstr[0] "3"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_msgid_plural2():
        po_entries, obsolete_entries, error_messages = parse('''msgctxt "c"
msgid "1"
msgid_plural "2"
msgstr[0] "3"
msgstr[1] "4"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgid_plural': '2',
                'msgstr': [ '3', '4' ],
                'line': 1,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''msgctxt "c"
msgid "1"
msgid_plural "2"
msgstr[0] "3"
msgstr[1] "4"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_comments():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
# comment 2
#. comment 3
#. comment 4
msgctxt "c"
msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'comment': [
                    '# comment 1',
                    '# comment 2',
                    '#. comment 3',
                    '#. comment 4'
                ],
                'line': 5,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''# comment 1
# comment 2
#. comment 3
#. comment 4
msgctxt "c"
msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_ref_comments():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
msgctxt "c"
msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'reference': [ ( 'aaa', '10', ), ( 'bbb', '20', ) ],
                'comment': [
                    '# comment 1',
                    '# comment 2',
                    '#. comment 3',
                    '#. comment 4'
                ],
                'line': 6,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
msgctxt "c"
msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_flag_comments():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format rust-format, lua-format
#= a b c, d,e, a
msgctxt "c"
msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'reference': [ ( 'aaa', '10', ), ( 'bbb', '20', ) ],
                'flag': [ 'c-format', 'rust-format', 'lua-format', 'a', 'b', 'c', 'd', 'e', 'a' ],
                'comment': [
                    '# comment 1',
                    '# comment 2',
                    '#. comment 3',
                    '#. comment 4'
                ],
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format, rust-format, lua-format, a, b, c, d, e, a
msgctxt "c"
msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_fuzzy_entry():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format rust-format, lua-format
#= a b c, d,e,
#, fuzzy
msgctxt "c"
msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'reference': [ ( 'aaa', '10', ), ( 'bbb', '20', ) ],
                'flag': [ 'c-format', 'rust-format', 'lua-format', 'a', 'b', 'c', 'd', 'e', 'fuzzy' ],
                'fuzzy': True,
                'comment': [
                    '# comment 1',
                    '# comment 2',
                    '#. comment 3',
                    '#. comment 4'
                ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format, rust-format, lua-format, a, b, c, d, e, fuzzy
msgctxt "c"
msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_previous_msgid_entry():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format rust-format, lua-format
#= a b c, d,e,
#, fuzzy
#| msgid "10"
msgctxt "c"
msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'reference': [ ( 'aaa', '10', ), ( 'bbb', '20', ) ],
                'flag': [ 'c-format', 'rust-format', 'lua-format', 'a', 'b', 'c', 'd', 'e', 'fuzzy' ],
                'fuzzy': True,
                'comment': [
                    '# comment 1',
                    '# comment 2',
                    '#. comment 3',
                    '#. comment 4'
                ],
                'prev_msgid': '10',
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format, rust-format, lua-format, a, b, c, d, e, fuzzy
#| msgid "10"
msgctxt "c"
msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_previous_msgid_plural_entry():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format rust-format, lua-format
#= a b c, d,e,
#, fuzzy
#| msgid "10"
#| msgid_plural "11"
msgctxt "c"
msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'reference': [ ( 'aaa', '10', ), ( 'bbb', '20', ) ],
                'flag': [ 'c-format', 'rust-format', 'lua-format', 'a', 'b', 'c', 'd', 'e', 'fuzzy' ],
                'fuzzy': True,
                'comment': [
                    '# comment 1',
                    '# comment 2',
                    '#. comment 3',
                    '#. comment 4'
                ],
                'prev_msgid': '10',
                'prev_msgid_plural': '11',
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format, rust-format, lua-format, a, b, c, d, e, fuzzy
#| msgid "10"
#| msgid_plural "11"
msgctxt "c"
msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_previous_msgctxt_entry():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format rust-format, lua-format
#= a b c, d,e,
#, fuzzy
#| msgctxt "1c"
#| msgid "10"
#| msgid_plural "11"
msgctxt "c"
msgid "1"
msgstr "2"
''')
        good = True
        good &= po_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'reference': [ ( 'aaa', '10', ), ( 'bbb', '20', ) ],
                'flag': [ 'c-format', 'rust-format', 'lua-format', 'a', 'b', 'c', 'd', 'e', 'fuzzy' ],
                'fuzzy': True,
                'comment': [
                    '# comment 1',
                    '# comment 2',
                    '#. comment 3',
                    '#. comment 4'
                ],
                'prev_msgctxt': '1c',
                'prev_msgid': '10',
                'prev_msgid_plural': '11',
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        s = dumps(po_entries)
        good &= s == '''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format, rust-format, lua-format, a, b, c, d, e, fuzzy
#| msgctxt "1c"
#| msgid "10"
#| msgid_plural "11"
msgctxt "c"
msgid "1"
msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_obsolete_entry():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format rust-format, lua-format
#= a b c, d,e,
#, fuzzy
#~ #| msgctxt "1c"
#~ #| msgid "10"
#~ #| msgid_plural "11"
#~ msgctxt "c"
#~ msgid "1"
#~ msgstr "2"
''')
        good = True
        good &= len(po_entries) == 0
        good &= obsolete_entries == {
            'c' + '\x04' + '1': {
                'msgctxt': 'c',
                'msgid': '1',
                'msgstr': [ '2' ],
                'reference': [ ( 'aaa', '10', ), ( 'bbb', '20', ) ],
                'flag': [ 'c-format', 'rust-format', 'lua-format', 'a', 'b', 'c', 'd', 'e', 'fuzzy' ],
                'fuzzy': True,
                'obsolete': True,
                'comment': [
                    '# comment 1',
                    '# comment 2',
                    '#. comment 3',
                    '#. comment 4'
                ],
                'prev_msgctxt': '1c',
                'prev_msgid': '10',
                'prev_msgid_plural': '11',
                'line': 12,
                'column': 4,
            },
        }
        good &= len(error_messages) == 0
        s = dumps(obsolete_entries)
        good &= s == '''# comment 1
# comment 2
#. comment 3
#. comment 4
#: aaa:10 bbb:20
#, c-format, rust-format, lua-format, a, b, c, d, e, fuzzy
#~ #| msgctxt "1c"
#~ #| msgid "10"
#~ #| msgid_plural "11"
#~ msgctxt "c"
#~ msgid "1"
#~ msgstr "2"
'''
        return 'Not match' if not good else None

    @add_test(tests)
    def test_multi_entries():
        po_entries, obsolete_entries, error_messages = parse('''# comment 1
#: a:10
#, flag1
#| msgid "1x"
msgid "1-1"
msgstr "1-2"

# comment 2
#: a:20
#, fuzzy
#~ #| msgid "2x"
#~ #| msgid_plural "2xp"
#~ msgctxt "2-0"
#~ msgid "2-1"
#~ msgid_plural "2-1p"
#~ msgstr[0] "2-2"
#~ msgstr[1] "2-3"

# comment 3
#: a:30
#, fuzzy
#| msgid "3x"
#| msgid_plural "3xp"
msgctxt "3-0"
msgid "3-1"
msgid_plural "3-1p"
msgstr[0] "3-2"
msgstr[1] "3-3"

# comment 4
#: a:40
#= flag4
#~ #| msgid "4x"
#~ #| msgid_plural "4xp"
#~ msgctxt "4-0"
#~ msgid "4-1"
#~ msgstr "4-2"
''')
        good = True
        good &= po_entries == {
            '1-1': {
                'msgid': '1-1',
                'msgstr': [ '1-2' ],
                'reference': [ ( 'a', '10', ) ],
                'flag': [ 'flag1' ],
                'comment': [
                    '# comment 1',
                ],
                'prev_msgid': '1x',
                'line': 5,
                'column': 1,
            },
            '3-0' + '\x04' + '3-1': {
                'msgctxt': '3-0',
                'msgid': '3-1',
                'msgid_plural': '3-1p',
                'msgstr': [ '3-2', '3-3' ],
                'reference': [ ( 'a', '30', ) ],
                'flag': [ 'fuzzy' ],
                'fuzzy': True,
                'comment': [
                    '# comment 3',
                ],
                'prev_msgid': '3x',
                'prev_msgid_plural': '3xp',
                'line': 24,
                'column': 1,
            },
        }
        good &= obsolete_entries == {
            '2-0' + '\x04' + '2-1': {
                'msgctxt': '2-0',
                'msgid': '2-1',
                'msgid_plural': '2-1p',
                'msgstr': [ '2-2', '2-3' ],
                'reference': [ ( 'a', '20', ) ],
                'flag': [ 'fuzzy' ],
                'fuzzy': True,
                'obsolete': True,
                'comment': [
                    '# comment 2',
                ],
                'prev_msgid': '2x',
                'prev_msgid_plural': '2xp',
                'line': 13,
                'column': 4,
            },
            '4-0' + '\x04' + '4-1': {
                'msgctxt': '4-0',
                'msgid': '4-1',
                'msgstr': [ '4-2' ],
                'reference': [ ( 'a', '40', ) ],
                'flag': [ 'flag4' ],
                'obsolete': True,
                'comment': [
                    '# comment 4',
                ],
                'prev_msgid': '4x',
                'prev_msgid_plural': '4xp',
                'line': 35,
                'column': 4,
            },
        }
        good &= len(error_messages) == 0
        po_entries.update(obsolete_entries)
        s = dumps(po_entries)
        good &= s == '''# comment 1
#: a:10
#, flag1
#| msgid "1x"
msgid "1-1"
msgstr "1-2"

# comment 3
#: a:30
#, fuzzy
#| msgid "3x"
#| msgid_plural "3xp"
msgctxt "3-0"
msgid "3-1"
msgid_plural "3-1p"
msgstr[0] "3-2"
msgstr[1] "3-3"

# comment 2
#: a:20
#, fuzzy
#~ #| msgid "2x"
#~ #| msgid_plural "2xp"
#~ msgctxt "2-0"
#~ msgid "2-1"
#~ msgid_plural "2-1p"
#~ msgstr[0] "2-2"
#~ msgstr[1] "2-3"

# comment 4
#: a:40
#, flag4
#~ #| msgid "4x"
#~ #| msgid_plural "4xp"
#~ msgctxt "4-0"
#~ msgid "4-1"
#~ msgstr "4-2"
'''
        return 'Not match' if not good else None

    return run_test(tests, msgout, verbose)
