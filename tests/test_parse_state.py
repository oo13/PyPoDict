#!/usr/bin/python3
'''Test parse.'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import sys

from .utils import *

from podict import parse

def test(msgout=sys.stdout, verbose=True):
    tests = Tests()

    # Initial
    @add_test(tests)
    def test_initial_comment():
        po_entries, obsolete_entries, error_messages = parse('''# comment
msgid "a"
msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'comment': [ '# comment' ],
                'line': 2,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 5,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''#| msgctxt "pca"
#| msgid "pa"
msgid "a"
msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 3,
                'column': 1,
                'prev_msgctxt': 'pca',
                'prev_msgid': 'pa',
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 6,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''#| msgid "pa"
msgid "a"
msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 1,
                'prev_msgid': 'pa',
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 5,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''#| msgid_plural "pap"
msgid "a"
msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 5,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''msgctxt "ac"
msgid "a"
msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'ac' + '\x04' + 'a': {
                'msgctxt': 'ac',
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 1,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 5,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_msgid():
        po_entries, obsolete_entries, error_messages = parse('''msgid "a"
msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 1,
                'column': 1,
            },
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 4,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''msgid_plural "ap"
msgstr[0] "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 4,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 3,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''msgstr[0] "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 3,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unexpected msgstr[n]', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_EOF():
        po_entries, obsolete_entries, error_messages = parse('')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_obsolete():
        po_entries, obsolete_entries, error_messages = parse('''#~ msgctxt "ac"
#~ msgid "a"
#~ msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 5,
                'column': 1,
            },
        }
        good &= obsolete_entries == {
            'ac' + '\x04' + 'a': {
                'msgctxt': 'ac',
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'obsolete': True,
                'line': 1,
                'column': 4,
            },
        }
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_obsolete_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''#~ #| msgctxt "pca"
#~ #| msgid "pa"
#~ msgid "a"
#~ msgstr "A"

msgid "b"
msgstr "B"
''')
        good = True
        good &= po_entries == {
            'b': {
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 6,
                'column': 1,
            },
        }
        good &= obsolete_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'obsolete': True,
                'line': 3,
                'column': 4,
                'prev_msgctxt': 'pca',
                'prev_msgid': 'pa',
            },
        }
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_text():
        po_entries, obsolete_entries, error_messages = parse('''"a"

msgid "b"
msgstr "B"
''')
        good = True
        good &= len(po_entries) == 0
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 1, 1, 'Unexpected quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_initial_newline():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "B"
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
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    # State ERROR_BEFORE_MSGID
    @add_test(tests)
    def test_input_comment_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
# comment
msgid "b"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
msgctxt "cb"
msgid "b"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
msgid_plural "bp"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
"text"
msgid "b"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
error_token
msgid "b"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
#| msgctxt "pcbp"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
#| msgid "pb"
msgid "b"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
#| msgid_plural "pbp2"
msgid "b"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_error_before_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid_plural "pbp"
#| "text"
msgid "b"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    # State COMMENT
    @add_test(tests)
    def test_input_comment_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
# comment
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'comment': [ '# comment state', '# comment' ],
                'line': 7,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
msgctxt "cb"
msgid "b"
msgstr "B"

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
            'cb' + '\x04' + 'b': {
                'msgctxt': 'cb',
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'comment': [ '# comment state' ],
                'line': 6,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'comment': [ '# comment state' ],
                'line': 6,
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
    def test_input_msgid_plural_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
msgid_plural "bp"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n]', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
"text"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
error_token
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
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
            ( 6, 1, 'Unexpected EOF (orphaned comment is detected)', )
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
#| msgctxt "pcbp"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'comment': [ '# comment state' ],
                'line': 8,
                'column': 1,
                'prev_msgctxt': 'pcbp',
                'prev_msgid': 'pb',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'comment': [ '# comment state' ],
                'line': 7,
                'column': 1,
                'prev_msgid': 'pb',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_comment():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

# comment state
#| "text"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    # State PREV_MSGCTXT
    @add_test(tests)
    def test_input_comment_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
# comment
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected comment (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
msgctxt "cb"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgctxt (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
msgid_plural "bp"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid_plural (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n] (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
"text"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected quoted text (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
error_token
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
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
            ( 6, 1, 'Unexpected EOF (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
#| msgctxt "pcb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgctxt (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
#| msgid "pb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid_plural (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_prev_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt
#| "text"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 8,
                'column': 1,
                'prev_msgctxt': 'text',
                'prev_msgid': 'pb',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    # State PREV_MSGID
    @add_test(tests)
    def test_input_comment_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
# comment
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected comment (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
msgctxt "cb"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgctxt (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
msgid_plural "bp"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid_plural (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n] (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
"text"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected quoted text (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
error_token
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
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
            ( 6, 1, 'Unexpected EOF (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
#| msgctxt "pcb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgctxt (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
#| msgid "pb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid_plural (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_prev_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid
#| "text"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 7,
                'column': 1,
                'prev_msgid': 'text',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    # State PREV_MSGID_PLURAL
    @add_test(tests)
    def test_input_comment_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
# comment
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 1, 'Unexpected comment (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
msgctxt "cb"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 1, 'Unexpected msgctxt (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
msgid "b"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgid (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
msgid_plural "bp"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgid_plural (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
msgstr "B"

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
            ( 7, 1, 'Unexpected msgstr (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgstr[n] (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
"text"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 1, 'Unexpected quoted text (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
error_token
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
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
            ( 7, 1, 'Unexpected EOF (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
#| msgctxt "pcb"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgctxt (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
#| msgid "pb2"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgid (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgid_plural (#| quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_prev_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural
#| "text"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 8,
                'column': 1,
                'prev_msgid': 'pb',
                'prev_msgid_plural': 'text',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    # State MSGCTXT
    @add_test(tests)
    def test_input_comment_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
# comment
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected comment (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
msgctxt "cb"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
msgid_plural "bp"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n] (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
"text"
msgid "b"
msgstr "B"

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
            'text' + '\x04' + 'b': {
                'msgctxt': 'text',
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 5,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
error_token
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
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
            ( 6, 1, 'Unexpected EOF (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
#| msgctxt "pcb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
#| msgid "pb2"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgctxt():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt
#| "text"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| quoted text (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    # State MSGID
    @add_test(tests)
    def test_input_comment_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
# comment
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected comment (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
msgctxt "cb"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
msgid_plural "bp"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n] (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
"text"
msgstr "B"

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
            'text': {
                'msgid': 'text',
                'msgstr': [ 'B' ],
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
    def test_input_error_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
error_token
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
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
            ( 6, 1, 'Unexpected EOF (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
#| msgctxt "pcb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
#| msgid "pb2"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgid():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid
#| "text"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| quoted text (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    # State MSGID_PLURAL
    @add_test(tests)
    def test_input_comment_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
# comment
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected comment (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
msgctxt "cb"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
msgid "b2"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
msgid_plural "bp"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
msgstr "B"

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
            ( 7, 1, 'Unexpected msgstr (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgstr[n] (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
"text"
msgstr[0] "B"

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
                'msgid_plural': 'text',
                'msgstr': [ 'B' ],
                'line': 5,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
error_token
msgstr[0] "B"

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
            ( 7, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
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
            ( 7, 1, 'Unexpected EOF (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
#| msgctxt "pcb"
msgstr[0] "B"

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
            ( 7, 4, 'Unexpected #| msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
#| msgid "pb2"
msgstr[0] "B"

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
            ( 7, 4, 'Unexpected #| msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
#| msgid_plural "pbp"
msgstr[0] "B"

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
            ( 7, 4, 'Unexpected #| msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgid_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural
#| "text"
msgstr[0] "B"

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
            ( 7, 4, 'Unexpected #| quoted text (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    # State MSGSTR
    @add_test(tests)
    def test_input_comment_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
# comment
msgstr "B"

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
            ( 7, 1, 'Unexpected comment (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
msgctxt "cb"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
msgid "b2"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
msgid_plural "bp"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
msgstr "B"

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
            ( 7, 1, 'Unexpected msgstr (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgstr[n] (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
"text"

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
                'msgstr': [ 'text' ],
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
    def test_input_error_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
error_token
msgid "b2"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
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
            ( 7, 1, 'Unexpected EOF (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
#| msgctxt "pcb"
msgid "b2"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
#| msgid "pb2"
msgid "b2"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
#| msgid_plural "pbp"
msgid "b2"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgstr():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr
#| "text"
msgid "b2"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| quoted text (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    # State MSGSTR_PLURAL
    @add_test(tests)
    def test_input_comment_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
# comment
msgstr[0] "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 1, 'Unexpected comment (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
msgctxt "cb"
msgstr[0] "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 1, 'Unexpected msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
msgid "b2"
msgstr[0] "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 1, 'Unexpected msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
msgid_plural "bp"
msgstr[0] "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 1, 'Unexpected msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
msgstr "B"

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
            ( 8, 1, 'Unexpected msgstr (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
msgstr[0] "B"

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
            ( 8, 1, 'Unexpected msgstr[n] (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
"text"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'text' ],
                'line': 5,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
error_token
msgid "b2"
msgstr "B"

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
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
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
            ( 8, 1, 'Unexpected EOF (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
#| msgctxt "pcb"
msgid "b2"
msgstr "B"

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
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 4, 'Unexpected #| msgctxt (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
#| msgid "pb2"
msgid "b2"
msgstr "B"

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
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 4, 'Unexpected #| msgid (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
#| msgid_plural "pbp"
msgid "b2"
msgstr "B"

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
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 4, 'Unexpected #| msgid_plural (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgstr_plural():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0]
#| "text"
msgid "b2"
msgstr "B"

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
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 4, 'Unexpected #| quoted text (quoted text is expected)', ),
        ]
        return 'Some errors are detected' if not good else None

    # State PREV_MSGCTXT_TEXT
    @add_test(tests)
    def test_input_comment_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev msgctxt text state"
# comment
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected comment', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
msgctxt "cb"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
msgid_plural "bp"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n]', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
"text"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
error_token
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
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
            ( 6, 1, 'Unexpected EOF', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
#| msgctxt "pcb"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 4, 'Unexpected #| msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 7,
                'column': 1,
                'prev_msgctxt': 'prev_msgctxt text state',
                'prev_msgid': 'pb',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_prev_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgctxt "prev_msgctxt text state"
#| "text"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 8,
                'column': 1,
                'prev_msgctxt': 'prev_msgctxt text statetext',
                'prev_msgid': 'pb',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    # State PREV_MSGID_TEXT
    @add_test(tests)
    def test_input_comment_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
# comment
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected comment', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
msgctxt "cb"
msgid "b"
msgstr "B"

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
            'cb' + '\x04' + 'b': {
                'msgctxt': 'cb',
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 6,
                'column': 1,
                'prev_msgid': 'prev_msgid text state',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 6,
                'column': 1,
                'prev_msgid': 'prev_msgid text state',
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
    def test_input_msgid_plural_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
msgid_plural "bp"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n]', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
"text"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
error_token
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
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
            ( 6, 1, 'Unexpected EOF', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
#| msgctxt "pcb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
#| msgid "pb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 7,
                'column': 1,
                'prev_msgid': 'prev_msgid text state',
                'prev_msgid_plural': 'pbp',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_prev_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "prev_msgid text state"
#| "text"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 7,
                'column': 1,
                'prev_msgid': 'prev_msgid text statetext',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    # State PREV_MSGID_PLURAL_TEXT
    @add_test(tests)
    def test_input_comment_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
# comment
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 1, 'Unexpected comment', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
msgctxt "cb"
msgid "b"
msgstr "B"

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
            'cb' + '\x04' + 'b': {
                'msgctxt': 'cb',
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 7,
                'column': 1,
                'prev_msgid': 'pb',
                'prev_msgid_plural': 'prev msgid_plural text state',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 7,
                'column': 1,
                'prev_msgid': 'pb',
                'prev_msgid_plural': 'prev msgid_plural text state',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
msgid_plural "bp"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgstr[n]', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
"text"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 1, 'Unexpected quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
error_token
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
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
            ( 7, 1, 'Unexpected EOF', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
#| msgctxt "pcb"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_prev_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| msgid "pb"
#| msgid_plural "prev msgid_plural text state"
#| "text"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 8,
                'column': 1,
                'prev_msgid': 'pb',
                'prev_msgid_plural': 'prev msgid_plural text statetext',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    # State MSGCTXT_TEXT
    @add_test(tests)
    def test_input_comment_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
# comment
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected comment', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
msgctxt "cb"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
msgid "b"
msgstr "B"

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
            'msgctxt text state' + '\x04' + 'b': {
                'msgctxt': 'msgctxt text state',
                'msgid': 'b',
                'msgstr': [ 'B' ],
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
    def test_input_msgid_plural_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
msgid_plural "bp"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
msgstr "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n]', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
"text"
msgid "b"
msgstr "B"

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
            'msgctxt text statetext' + '\x04' + 'b': {
                'msgctxt': 'msgctxt text statetext',
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 5,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
error_token
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
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
            ( 6, 1, 'Unexpected EOF', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
#| msgctxt "pcb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
#| msgid "pb"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgctxt_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgctxt "msgctxt text state"
#| "text"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    # State MSGID_TEXT
    @add_test(tests)
    def test_input_comment_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
# comment
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected comment', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
msgctxt "cb"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
msgid "b"
msgstr "B"

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
            ( 6, 1, 'Unexpected msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
msgid_plural "bp"
msgstr[0] "B"

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
            'msgid text state': {
                'msgid': 'msgid text state',
                'msgid_plural': 'bp',
                'msgstr': [ 'B' ],
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
    def test_input_msgstr_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
msgstr "B"

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
            'msgid text state': {
                'msgid': 'msgid text state',
                'msgstr': [ 'B' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
msgstr[0] "B"

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
                'line': 8,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 6, 1, 'Unexpected msgstr[n]', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
"text"
msgstr "B"

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
            'msgid text statetext': {
                'msgid': 'msgid text statetext',
                'msgstr': [ 'B' ],
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
    def test_input_error_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
error_token
msgstr "B"

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
            ( 6, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
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
            ( 6, 1, 'Unexpected EOF', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
#| msgctxt "pcb"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
#| msgid "pb"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
#| msgid_plural "pbp"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgid_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "msgid text state"
#| "text"
msgid "b"
msgstr "B"

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
            ( 6, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    # State MSGID_PLURAL_TEXT
    @add_test(tests)
    def test_input_comment_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
# comment
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected comment', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
msgctxt "cb"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
msgid "b"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
msgid_plural "bp"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
msgstr[0] "B"

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
                'msgid_plural': 'msgid_plural_text state',
                'msgstr': [ 'B' ],
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
    def test_input_text_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
"text"
msgstr[0] "B"

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
                'msgid_plural': 'msgid_plural_text statetext',
                'msgstr': [ 'B' ],
                'line': 5,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
error_token
msgstr[0] "B"

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
            ( 7, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
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
            ( 7, 1, 'Unexpected EOF', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
#| msgctxt "pcb"
msgstr[0] "B"

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
            ( 7, 4, 'Unexpected #| msgctxt', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
#| msgid "pb"
msgstr[0] "B"

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
            ( 7, 4, 'Unexpected #| msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
#| msgid_plural "pbp"
msgstr[0] "B"

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
            ( 7, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgid_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "msgid_plural_text state"
#| "text"
msgstr[0] "B"

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
            ( 7, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    # State MSGSTR_TEXT
    @add_test(tests)
    def test_input_comment_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
# comment

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
                'msgstr': [ 'msgstr_text state' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'comment': [ '# comment' ],
                'line': 9,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
msgctxt "cb"
msgid "b2"
msgstr "B"

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
                'msgstr': [ 'msgstr_text state' ],
                'line': 5,
                'column': 1,
            },
            'cb' + '\x04' + 'b2': {
                'msgctxt': 'cb',
                'msgid': 'b2',
                'msgstr': [ 'B' ],
                'line': 7,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
msgid "b2"
msgstr "B"

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
                'msgstr': [ 'msgstr_text state' ],
                'line': 5,
                'column': 1,
            },
            'b2': {
                'msgid': 'b2',
                'msgstr': [ 'B' ],
                'line': 7,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
msgid_plural "bp"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
msgstr "B"

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
            ( 7, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
msgstr[0] "B"

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
            ( 7, 1, 'Unexpected msgstr[n]', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
"text"

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
                'msgstr': [ 'msgstr_text statetext' ],
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
    def test_input_error_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
error_token

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
            ( 7, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
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
                'msgstr': [ 'msgstr_text state' ],
                'line': 5,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
#| msgctxt "pcb"
msgid "b2"
msgstr "B"

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
                'msgstr': [ 'msgstr_text state' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 1, 'Unexpected msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
#| msgid "pb"
msgid "b2"
msgstr "B"

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
                'msgstr': [ 'msgstr_text state' ],
                'line': 5,
                'column': 1,
            },
            'b2': {
                'msgid': 'b2',
                'msgstr': [ 'B' ],
                'prev_msgid': 'pb',
                'line': 8,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
#| msgid_plural "pbp"
msgid "b2"
msgstr "B"

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
                'msgstr': [ 'msgstr_text state' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgstr_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgstr "msgstr_text state"
#| "text"
msgid "b2"
msgstr "B"

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
                'msgstr': [ 'msgstr_text state' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 7, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    # State MSGSTR_PLURAL_TEXT
    @add_test(tests)
    def test_input_comment_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
# comment

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'comment': [ '# comment' ],
                'line': 10,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
msgctxt "cb"
msgid "b2"
msgstr "B"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state' ],
                'line': 5,
                'column': 1,
            },
            'cb' + '\x04' + 'b2': {
                'msgctxt': 'cb',
                'msgid': 'b2',
                'msgstr': [ 'B' ],
                'line': 8,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
msgid "b2"
msgstr "B"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state' ],
                'line': 5,
                'column': 1,
            },
            'b2': {
                'msgid': 'b2',
                'msgstr': [ 'B' ],
                'line': 8,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
msgid_plural "bp2"
msgstr[0] "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 1, 'Unexpected msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
msgstr "B"

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
            ( 8, 1, 'Unexpected msgstr', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
msgstr[1] "B"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state', 'B' ],
                'line': 5,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
"text"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text statetext' ],
                'line': 5,
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
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
error_token

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
            ( 8, 1, 'Unknown token', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state' ],
                'line': 5,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
#| msgctxt "pcb"
msgid "b2"
msgstr "B"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 9, 1, 'Unexpected msgid', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
#| msgid "pb"
msgid "b2"
msgstr "B"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state' ],
                'line': 5,
                'column': 1,
            },
            'b2': {
                'msgid': 'b2',
                'msgstr': [ 'B' ],
                'prev_msgid': 'pb',
                'line': 9,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
#| msgid_plural "pbp"
msgid "b2"
msgstr "B"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 4, 'Unexpected #| msgid_plural', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_msgstr_plural_text():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

msgid "b"
msgid_plural "bp"
msgstr[0] "msgstr_plural_text state"
#| "text"
msgid "b2"
msgstr "B"

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
                'msgid_plural': 'bp',
                'msgstr': [ 'msgstr_plural_text state' ],
                'line': 5,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 8, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    # State ERROR
    @add_test(tests)
    def test_input_comment_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
# comment
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'comment': [ '# comment' ],
                'line': 8,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgctxt_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
msgctxt "cb"
msgid "b"
msgstr "B"

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
            'cb' + '\x04' + 'b': {
                'msgctxt': 'cb',
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'line': 7,
                'column': 1,
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 7,
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
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgid_plural_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
msgid_plural "bp"
msgstr[0] "B"

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
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_msgstr_plural_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
msgstr[0] "B"

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
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_text_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
"text"
msgstr "B"

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
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_error_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
error_token
msgstr "B"

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
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_EOF_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
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
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgctxt_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
#| msgctxt "pcb"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 9,
                'column': 1,
                'prev_msgctxt': 'pcb',
                'prev_msgid': 'pb',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 12,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
#| msgid "pb"
msgid "b"
msgstr "B"

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
                'msgstr': [ 'B' ],
                'line': 8,
                'column': 1,
                'prev_msgid': 'pb',
            },
            'c': {
                'msgid': 'c',
                'msgstr': [ 'C' ],
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_msgid_plural_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
#| msgid_plural "pbp"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_input_prev_text_in_state_error():
        po_entries, obsolete_entries, error_messages = parse('''
msgid "a"
msgstr "A"

#| "error_before_msgid"
msgid "error state"
#| "text"
msgid "b"
msgstr "B"

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
                'line': 11,
                'column': 1,
            },
        }
        good &= len(obsolete_entries) == 0
        good &= error_messages == [
            ( 5, 4, 'Unexpected #| quoted text', ),
        ]
        return 'Some errors are detected' if not good else None

    return run_test(tests, msgout, verbose)
