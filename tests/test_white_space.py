#!/usr/bin/python3
'''Test white spaces.'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import sys

from .utils import *

from podict import parse

def test(msgout=sys.stdout, verbose=True):
    tests = Tests()

    @add_test(tests)
    def test_no_white_space():
        po_entries, obsolete_entries, error_messages = parse('''msgid"a"msgstr"A"#comment
#:a:10 b:20
#,c-format
#|msgctxt"c""p""b"msgid"p""b"
msgctxt"c""b"msgid"b"msgstr"B"#|msgctxt"c""p""c"msgid"p""c"msgid_plural"p""c""p"
msgctxt"c""c"msgid"c"msgid_plural"c""p"msgstr[0]"C""0"msgstr[1]"C""1"#~#|msgid"pd"
#~msgid"d"msgstr"D"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 1,
                'column': 1,
            },
            'cb' + '\x04' + 'b': {
                'msgctxt': 'cb',
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'comment': [ '#comment', ],
                'reference': [ ( 'a', '10', ), ( 'b', '20', ), ],
                'flag': [ 'c-format', ],
                'line': 5,
                'column': 1,
                'prev_msgctxt': 'cpb',
                'prev_msgid': 'pb',
            },
            'cc' + '\x04' + 'c': {
                'msgctxt': 'cc',
                'msgid': 'c',
                'msgid_plural': 'cp',
                'msgstr': [ 'C0', 'C1', ],
                'line': 6,
                'column': 1,
                'prev_msgctxt': 'cpc',
                'prev_msgid': 'pc',
                'prev_msgid_plural': 'pcp',
            },
        }
        good &= obsolete_entries == {
            'd': {
                'msgid': 'd',
                'msgstr': [ 'D', ],
                'obsolete': True,
                'line': 7,
                'column': 3,
                'prev_msgid': 'pd',
            },
        }
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    @add_test(tests)
    def test_too_many_white_spaces():
        po_entries, obsolete_entries, error_messages = parse('''   \t
        \t msgid       "a"
\t        msgstr    "A"




        #  comment



                 \t#:   \ta:10 \tb:20

        #,   c-format


        #|   msgctxt"c" \t


        \t#| "p"

        #|\t"b"

    #|\tmsgid


        #| "p"

        #| "b" \t





        \t\tmsgctxt

        "c"\t

        \t"b"


        msgid

        "b"

        msgstr


        "B"

        #|     msgctxt
        #| \t"c" \t "p"\t

        #|\t"c"




        #| msgid\t"p"


        #|\t"c"
        #|\t\t\tmsgid_plural
        #|
        #|
        #|
        #| \t"p"

        #| "c"
        #|\t\t"p"



        msgctxt\t\t\t"c"
        "c"

        msgid
        \t"c"

        \t\t\tmsgid_plural\t"c"\t"p"


        msgstr \t  [    \t0  \t]
        "C"\t"0"

        msgstr
  \t      
        [
    \t    
        1
        \t
        ]
        "C"


        "1"

        #~\t\t#|\tmsgid\t"pd"\t



   #~   msgid
        #~  "d"        \tmsgstr
        #~ \t\t\t"D"
''')
        good = True
        good &= po_entries == {
            'a': {
                'msgid': 'a',
                'msgstr': [ 'A' ],
                'line': 2,
                'column': 11,
            },
            'cb' + '\x04' + 'b': {
                'msgctxt': 'cb',
                'msgid': 'b',
                'msgstr': [ 'B' ],
                'comment': [ '#  comment', ],
                'reference': [ ( 'a', '10', ), ( 'b', '20', ), ],
                'flag': [ 'c-format', ],
                'line': 35,
                'column': 11,
                'prev_msgctxt': 'cpb',
                'prev_msgid': 'pb',
            },
            'cc' + '\x04' + 'c': {
                'msgctxt': 'cc',
                'msgid': 'c',
                'msgid_plural': 'cp',
                'msgstr': [ 'C0', 'C1', ],
                'line': 74,
                'column': 9,
                'prev_msgctxt': 'cpc',
                'prev_msgid': 'pc',
                'prev_msgid_plural': 'pcp',
            },
        }
        good &= obsolete_entries == {
            'd': {
                'msgid': 'd',
                'msgstr': [ 'D', ],
                'obsolete': True,
                'line': 102,
                'column': 9,
                'prev_msgid': 'pd',
            },
        }
        good &= len(error_messages) == 0
        return 'Some errors are detected' if not good else None

    return run_test(tests, msgout, verbose)
