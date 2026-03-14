'''A package to convert a gettext PO text to/from a dict.

# Dict format
The dict has some entries in following form:
```
"msgctxt + msgid": {
    "msgctxt": "msgctxt string",
    "msgid": "msgid string",
    "msgid_plural": "msgid_plural string",
    "msgstr": [ "msgstr[0] string", ... ],
    "fuzzy": True,
    "obsolete": True,
    "flag": [ "flag", ... ],
    "reference": [ ( "file", "line" or None, ), ... ],
    "comment": [ "whole-line-wo-nl", ... ],
    "prev_msgctxt": "previous msgctxt string",
    "prev_msgid": "previous msgid string",
    "prev_msgid_plural": "previous msgid_plural string",
    "line": line_number (1 origin),
    "column": column_number (1 origin),
},
```

Note:
1. "msgctxt + msgid" means "msgctxt string" + '\x04' + "msgid string" if msgctxt is specified, otherwise "msgid string".
2. The key doesn't exist if the entry doesn't have it, so the values of "fuzzy" and "obsolete" always are True.
3. "comment" doesn't contain the flag, reference, and previous untranslated string.

# public functions
- parse()
- dump.dump()
- dump.dumps()
- dump.escape_and_split_text()
- metadata.parse()
- metadata.dumps()
- metadata.get_charset()
- metadata.get_plural()
'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

from .parse import parse
