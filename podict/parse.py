#!/usr/bin/python3
'''PO parser'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import enum
import functools
import io
import string

class _CharFeeder:
    '''char iterator, tracking the source line and column number and allowing to ungetc'''
    def __init__(self, char_iter):
        self._iter = char_iter
        self._line = None
        self._column = None
        self._next_line = 1
        self._next_column = 1
        self._next_c = None
        self._checked = False
    def __iter__(self):
        return self
    def __next__(self):
        if self._next_c is None:
            c = next(self._iter, None)
        else:
            c = self._next_c
            self._next_c = None
        self._line = self._next_line
        self._column = self._next_column
        if c == '\n':
            self._next_line += 1
            self._next_column = 1
        elif c is not None:
            self._next_column += 1
        if c is None:
            raise StopIteration
        return c
    def line_number(self):
        return self._line
    def column_number(self):
        return self._column
    def ungetc(self, c):
        '''self.__next__() will return c

        line_number() and column_number() return invalid value until calling __next__().
        '''
        if self._next_c is not None:
            raise OverflowError
        if c is None:
            # None should come from __next__() raised StopIteration
            return
        self._next_line = self._line
        self._next_column = self._column
        self._next_c = c

def _startswith(char_feeder, word):
    '''compare word with the string comes from the feeder.

    Stop the iteration when making the decision. (short circuit evaluation)
    '''
    matched = True
    for c in word:
        if next(char_feeder, None) != c:
            matched = False
            break
    return matched


class _Token(enum.IntEnum):
    OBSOLETE = enum.auto() # handled by _TokenFeeder, parse() doesn't get it.
    PREV = enum.auto() # same as above
    OBSOLETE_PREV = enum.auto() # same as above
    NEWLINE = enum.auto() # same as above
    COMMENT = enum.auto()
    MSGCTXT = enum.auto()
    MSGID = enum.auto()
    MSGID_PLURAL = enum.auto()
    MSGSTR = enum.auto()
    MSGSTR_PLURAL = enum.auto()
    TEXT = enum.auto()
    ERROR = enum.auto()
    EOF = enum.auto()
    PREV_MSGCTXT = enum.auto() # Special Token; _lex() doesn't generate it.
    PREV_MSGID = enum.auto() # same as above
    PREV_MSGID_PLURAL = enum.auto() # same as above
    PREV_TEXT = enum.auto() # same as above
    TOTAL = enum.auto()

_token_str = (
    '???', # 0
    '#~',
    '#|',
    '#~|',
    '\\n',
    'comment',
    'msgctxt',
    'msgid',
    'msgid_plural',
    'msgstr',
    'msgstr[n]',
    'quoted text',
    '???', # ERROR
    'EOF',
    '#| msgctxt',
    '#| msgid',
    '#| msgid_plural',
    '#| quoted text',
    '???', # TOTAL
)

def _parse_msg_keyword(char_feeder):
    '''parse msgctxt, msgid, msgid_plural, msgstr, and msgstr[n]

    The input char_feeder should point to the first 'm'.

    The output char_feeder will point to the next of the keyword, including '[n]' if it's msgstr[n].

    return token, value, error line, error column

    The value for the token MSGSTR_PLURAL is n (integer) of '[n]'.
    The value for the token ERROR is the error message.

    line and column are the first character of the keyword or the position detecting the error.
    '''
    token = _Token.ERROR
    value = None
    line = char_feeder.line_number()
    column = char_feeder.column_number()
    if _startswith(char_feeder, 'sg'):
        c = next(char_feeder, None)
        if c == 'c' and _startswith(char_feeder, 'txt'):
            token = _Token.MSGCTXT
        elif c == 'i' and _startswith(char_feeder, 'd'):
            c = next(char_feeder, None)
            if c != '_':
                char_feeder.ungetc(c)
                token = _Token.MSGID
            else:
                if _startswith(char_feeder, 'plural'):
                    token = _Token.MSGID_PLURAL
        elif c == 's' and _startswith(char_feeder, 'tr'):
            for c in char_feeder:
                if c not in string.whitespace:
                    break
            else:
                # EOF
                c = None
            if c != '[':
                char_feeder.ungetc(c)
                token = _Token.MSGSTR
            else:
                for c in char_feeder:
                    if c not in string.whitespace:
                        char_feeder.ungetc(c)
                        break
                n_str = ''
                for c in char_feeder:
                    if c in string.digits:
                        n_str += c
                    else:
                        char_feeder.ungetc(c)
                        break
                c = None
                for c in char_feeder:
                    if c not in string.whitespace:
                        break
                if len(n_str) == 0:
                    line = char_feeder.line_number()
                    column = char_feeder.column_number()
                    return _Token.ERROR, "'0'..'9' is expected", line, column
                elif c != ']':
                    line = char_feeder.line_number()
                    column = char_feeder.column_number()
                    return _Token.ERROR, "'0'..'9' or ']' is expected", line, column
                value = int(n_str)
                token = _Token.MSGSTR_PLURAL
    if token == _Token.ERROR:
        value = 'Unknown keyword'
    return token, value, line, column

_escape_map = {
    'a': '\a',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
    'v': '\v',
    '\\': '\\',
    "'": "'",
    '"': '"',
    '?': '?',
}

def _parse_text(char_feeder):
    '''parse "text"

    The input char_feeder should point to the opening '"'.

    The output char_feeder will point to the next of the closing '"'.

    return token, value, error line, error column

    The value for the token TEXT is the text.
    The value for the token ERROR is the error message.

    line and column are the position of the opening '"' or the position detecting the error.
    '''
    text = ''
    err_msg = None
    line = char_feeder.line_number()
    column = char_feeder.column_number()
    closed = False
    for c in char_feeder:
        if c == '\n':
            # Don't consume the newline
            char_feeder.ungetc(c)
            if err_msg is None:
                err_msg = 'The text may not contain a newline'
                line = char_feeder.line_number()
                column = char_feeder.column_number()
            break
        elif c == '"':
            closed = True
            break
        elif c == '\\':
            error = False
            c = next(char_feeder, None)
            if c is None:
                error = True
            elif c in _escape_map:
                text += _escape_map[c]
            elif c in string.octdigits:
                oct_str = c
                for i in range(2):
                    c = next(char_feeder, None)
                    if c is None:
                        break
                    elif c in string.octdigits:
                        oct_str += c
                    else:
                        char_feeder.ungetc(c)
                        break;
                text += chr(int(oct_str, base=8) & 0xFF)
            elif c == 'x':
                c = next(char_feeder, None)
                if c is None or c not in string.hexdigits:
                    error = True
                else:
                    hex_str = c
                    for c in char_feeder:
                        if c in string.hexdigits:
                            hex_str += c
                        else:
                            char_feeder.ungetc(c)
                            break
                    text += chr(int(hex_str, base=16) & 0xFF)
            else:
                error = True
            if error and err_msg is None:
                err_msg = "Invalid escape sequence"
                line = char_feeder.line_number()
                column = char_feeder.column_number()
                # consume input characters until '"' is found.
        else:
            text += c
    if not closed and err_msg is None:
        err_msg = 'Closing double quotation mark is expected'
        line = char_feeder.line_number()
        column = char_feeder.column_number()
    if err_msg is None:
        return _Token.TEXT, text, line, column
    else:
        return _Token.ERROR, err_msg, line, column

def _lex(char_feeder):
    '''lexical analyzer

    return token, value, line, column

    side effect: char_feeder points the next position of the last fed character.

    The value for the token COMMENT is the comment text (whole line without newline).
    The value for the token MSGSTR_PLURAL is n (integer) of '[n]'.
    The value for the token TEXT is the text.
    The value for the token ERROR is the error message.

    Don't care the line and column if token is NEWLINE, OBSOLETE, PREV, or OBSOLETE_PREV.
    '''
    is_eof = True
    for c in char_feeder:
        if c == '\n':
            return _Token.NEWLINE, None, None, None
        elif c not in string.whitespace:
            is_eof = False
            break
    if is_eof:
        return _Token.EOF, None, char_feeder.line_number(), char_feeder.column_number()
    elif c == '#':
        comment_body = c # comment_body contains the first '#'.
        line = char_feeder.line_number()
        column = char_feeder.column_number()
        c = next(char_feeder, None)
        if c == '~':
            c = next(char_feeder, None)
            if c == '|':
                return _Token.OBSOLETE_PREV, None, None, None
            else:
                char_feeder.ungetc(c)
                return _Token.OBSOLETE, None, None, None
        elif c == '|':
            return _Token.PREV, None, None, None
        char_feeder.ungetc(c)
        for c in char_feeder:
            if c is None or c == '\n':
                char_feeder.ungetc(c)
                break
            else:
                comment_body += c
        return _Token.COMMENT, comment_body, line, column
    elif c == 'm':
        return _parse_msg_keyword(char_feeder)
    elif c == '"':
        return _parse_text(char_feeder)
    else:
        # Unkonwn token
        return _Token.ERROR, 'Unknown token', char_feeder.line_number(), char_feeder.column_number()

def _parse_range_flag_parameter(param):
    '''Is 'param' the parameter of the 'range' flag?'''
    idx = 0
    while idx < len(param) and param[idx] in string.digits:
        idx += 1
    if idx > 0 and param[idx:idx+2] == '..':
        idx += 2
        m_idx = idx
        good = False
        while idx < len(param) and param[idx] in string.digits:
            good = True
            idx += 1
        if good:
            return param # GNU gettext discards trailing characters, but this library keeps the information.
        else:
            return False
    return False

def _parse_flag_comment(flag_comment):
    '''parse flag comment

    return [flags, ...]

    The flags are separated by some white spaces and commas, but 'range: n..m' flag may contain some separators.
    '''
    flags = []
    flag = ''
    for i in range(len(flag_comment)):
        c = flag_comment[i]
        is_separator = c in string.whitespace or c == ','
        if not is_separator:
            flag += c
        if is_separator or i == len(flag_comment) - 1:
            if len(flag) > 0:
                if len(flags) > 0 and flags[-1] == 'range:' and (param := _parse_range_flag_parameter(flag)):
                    flags[-1] += ' ' + param
                else:
                    flags.append(flag)
                flag = ''
    return flags

def _is_ascii_digits(s):
    '''if s contains only ASCII digits'''
    return len(s) > 0 and all(( x in string.digits for x in s ))

def _parse_reference_comment(ref_comment):
    '''parse referenece comment

    return [ (ref_file, ref_line,), (ref_file, None,), ... ]

    ref_file is a string, and ref_line is a string or None.

    ref_file may be an empty string. The quotation '\u2068' and '\u2069' are removed.
    ref_line isn't empty and consists of '0'..'9' if it's a string.

    The format of a reference text:
    ( '\u2068', [^\u2069]*, '\u2069' | [^ \t]* ) [ \t]* ( ':', [ \t]*, [0-9]* )?
    It means that only the last ':' before a string formed by '0'..'9' separates the filename and the line number, and the filename can contain ':'.
    '''
    # split by elim
    undetermined = []
    tokens = []
    quoting = False
    delim = ' \t' # ref_comment doesn't have '\n'
    token = ''
    for c in ref_comment:
        if quoting:
            if c == '\u2069':
                # Closing quotation '\u2069' has meaning as a delimiter.
                tokens.append(token)
                # The quoted token must be the filename.
                undetermined.append(False)
                token = ''
                quoting = False
            else:
                token += c
        else:
            if c in delim:
                if len(token) > 0:
                    tokens.append(token)
                    undetermined.append(True)
                    token = ''
            elif len(token) == 0 and c == '\u2068':
                # '\u2068' has no special meaning if it's not the first character.
                quoting = True
            else:
                token += c
    if len(token) > 0:
        tokens.append(token)
        # Closing quoting '\u2069' is an option at the end of the line.
        undetermined.append(not quoting)
    # determine the filename and the line number.
    i = 0
    result = []
    while i < len(tokens):
        if i+2 < len(tokens) and undetermined[i+1] and tokens[i+1] == ':':
            if undetermined[i+2] and _is_ascii_digits(tokens[i+2]):
                result.append(( tokens[i], tokens[i+2], ))
                i += 3
                continue
        if i+1 < len(tokens):
            if undetermined[i+1] and tokens[i+1][0] == ':' and _is_ascii_digits(tokens[i+1][1:]):
                result.append(( tokens[i], tokens[i+1][1:], ))
                i += 2
                continue
            elif undetermined[i] and tokens[i][-1] == ':' and undetermined[i+1] and _is_ascii_digits(tokens[i+1]):
                result.append(( tokens[i][0:-1], tokens[i+1], ))
                i += 2
                continue
        if undetermined[i] and tokens[i][-1] != ':' and (idx := tokens[i].rfind(':')) >= 0:
            if _is_ascii_digits(tokens[i][idx+1:]):
                result.append(( tokens[i][0:idx], tokens[i][idx+1:], ))
                i += 1
                continue
        result.append(( tokens[i], None, ))
        i += 1
    return result

class _TokenFeeder:
    '''Token feeder to handle the lexical state'''
    def __init__(self, char_feeder):
        self._char_feeder = char_feeder
        self._obsolete = False
        self._prev = False
        self._eof = False
    def __iter__(self):
        return self
    def __next__(self):
        if self._eof:
            raise StopIteration
        while True:
            token, value, line, column = _lex(self._char_feeder)
            if token == _Token.OBSOLETE:
                self._obsolete = True
            elif token == _Token.PREV:
                self._prev = True
            elif token == _Token.OBSOLETE_PREV:
                self._obsolete = True
                self._prev = True
            elif token == _Token.NEWLINE:
                self._obsolete = False
                self._prev = False
            else:
                break
        self._eof = token == _Token.EOF
        if self._prev:
            if token == _Token.MSGCTXT:
                token = _Token.PREV_MSGCTXT
            elif token == _Token.MSGID:
                token = _Token.PREV_MSGID
            elif token == _Token.MSGID_PLURAL:
                token = _Token.PREV_MSGID_PLURAL
            elif token == _Token.TEXT:
                token = _Token.PREV_TEXT
        return token, self._obsolete, value, line, column

# In a PO entry: PREV_MSGCTXT <= x <= MSGSTR_PLURAL_TEXT
# In a text except for msgstr: PREV_MSGCTXT_TEXT <= x <= MSGID_PLURAL_TEXT
# In a msgstr text: MSGSTR_TEXT <= x <= MSGSTR_PLURAL_TEXT
class _State(enum.IntEnum):
    END_OF_ENTRY = enum.auto() # Special state, don't consume the token.
    ERROR_BEFORE_MSGID = enum.auto() # The next msgid should be dropped.
    COMMENT = enum.auto()
    PREV_MSGCTXT = enum.auto()
    PREV_MSGID = enum.auto()
    PREV_MSGID_PLURAL = enum.auto()
    MSGCTXT = enum.auto()
    MSGID = enum.auto()
    MSGID_PLURAL = enum.auto()
    MSGSTR = enum.auto()
    MSGSTR_PLURAL = enum.auto()
    PREV_MSGCTXT_TEXT = enum.auto()
    PREV_MSGID_TEXT = enum.auto()
    PREV_MSGID_PLURAL_TEXT = enum.auto()
    MSGCTXT_TEXT = enum.auto()
    MSGID_TEXT = enum.auto()
    MSGID_PLURAL_TEXT = enum.auto()
    MSGSTR_TEXT = enum.auto()
    MSGSTR_PLURAL_TEXT = enum.auto()
    ERROR = enum.auto()
    EOF = enum.auto()
    TOTAL = enum.auto()

_state_trans_def = (
    # Current state -> received Token -> New State
    ( _State.COMMENT, _Token.COMMENT, _State.COMMENT, ),
    ( _State.COMMENT, _Token.PREV_MSGCTXT, _State.PREV_MSGCTXT, ),
    ( _State.COMMENT, _Token.PREV_MSGID, _State.PREV_MSGID, ),
    ( _State.COMMENT, _Token.MSGCTXT, _State.MSGCTXT, ),
    ( _State.COMMENT, _Token.MSGID, _State.MSGID, ),
    ( _State.PREV_MSGCTXT, _Token.PREV_TEXT, _State.PREV_MSGCTXT_TEXT, ),
    ( _State.PREV_MSGCTXT_TEXT, _Token.PREV_TEXT, _State.PREV_MSGCTXT_TEXT, ),
    ( _State.PREV_MSGCTXT_TEXT, _Token.PREV_MSGID, _State.PREV_MSGID, ),
    ( _State.PREV_MSGID, _Token.PREV_TEXT, _State.PREV_MSGID_TEXT, ),
    ( _State.PREV_MSGID_TEXT, _Token.PREV_TEXT, _State.PREV_MSGID_TEXT, ),
    ( _State.PREV_MSGID_TEXT, _Token.PREV_MSGID_PLURAL, _State.PREV_MSGID_PLURAL, ),
    ( _State.PREV_MSGID_TEXT, _Token.MSGCTXT, _State.MSGCTXT, ),
    ( _State.PREV_MSGID_TEXT, _Token.MSGID, _State.MSGID, ),
    ( _State.PREV_MSGID_PLURAL, _Token.PREV_TEXT, _State.PREV_MSGID_PLURAL_TEXT, ),
    ( _State.PREV_MSGID_PLURAL_TEXT, _Token.PREV_TEXT, _State.PREV_MSGID_PLURAL_TEXT, ),
    ( _State.PREV_MSGID_PLURAL_TEXT, _Token.MSGCTXT, _State.MSGCTXT, ),
    ( _State.PREV_MSGID_PLURAL_TEXT, _Token.MSGID, _State.MSGID, ),
    ( _State.MSGCTXT, _Token.TEXT, _State.MSGCTXT_TEXT, ),
    ( _State.MSGCTXT_TEXT, _Token.TEXT, _State.MSGCTXT_TEXT, ),
    ( _State.MSGCTXT_TEXT, _Token.MSGID, _State.MSGID, ),
    ( _State.MSGID, _Token.TEXT, _State.MSGID_TEXT, ),
    ( _State.MSGID_TEXT, _Token.TEXT, _State.MSGID_TEXT, ),
    ( _State.MSGID_TEXT, _Token.MSGID_PLURAL, _State.MSGID_PLURAL, ),
    ( _State.MSGID_TEXT, _Token.MSGSTR, _State.MSGSTR, ),
    ( _State.MSGID_TEXT, _Token.ERROR, _State.ERROR, ),
    ( _State.MSGID_PLURAL, _Token.TEXT, _State.MSGID_PLURAL_TEXT, ),
    ( _State.MSGID_PLURAL_TEXT, _Token.TEXT, _State.MSGID_PLURAL_TEXT, ),
    ( _State.MSGID_PLURAL_TEXT, _Token.MSGSTR_PLURAL, _State.MSGSTR_PLURAL, ),
    ( _State.MSGID_PLURAL_TEXT, _Token.ERROR, _State.ERROR, ),
    ( _State.MSGSTR, _Token.TEXT, _State.MSGSTR_TEXT, ),
    ( _State.MSGSTR_TEXT, _Token.TEXT, _State.MSGSTR_TEXT, ),
    ( _State.MSGSTR_TEXT, _Token.COMMENT, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_TEXT, _Token.PREV_MSGCTXT, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_TEXT, _Token.PREV_MSGID, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_TEXT, _Token.PREV_MSGID_PLURAL, _State.END_OF_ENTRY, ), # register the entry, and then error
    ( _State.MSGSTR_TEXT, _Token.PREV_TEXT, _State.END_OF_ENTRY, ), # register the entry, and then error
    ( _State.MSGSTR_TEXT, _Token.MSGCTXT, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_TEXT, _Token.MSGID, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_TEXT, _Token.EOF, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_TEXT, _Token.ERROR, _State.ERROR, ),
    ( _State.MSGSTR_PLURAL, _Token.TEXT, _State.MSGSTR_PLURAL_TEXT, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.TEXT, _State.MSGSTR_PLURAL_TEXT, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.MSGSTR_PLURAL, _State.MSGSTR_PLURAL, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.COMMENT, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.PREV_MSGCTXT, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.PREV_MSGID, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.PREV_MSGID_PLURAL, _State.END_OF_ENTRY, ), # register the entry, and then error
    ( _State.MSGSTR_PLURAL_TEXT, _Token.PREV_TEXT, _State.END_OF_ENTRY, ), # register the entry, and then error
    ( _State.MSGSTR_PLURAL_TEXT, _Token.MSGCTXT, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.MSGID, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.EOF, _State.END_OF_ENTRY, ),
    ( _State.MSGSTR_PLURAL_TEXT, _Token.ERROR, _State.ERROR, ),
    ( _State.END_OF_ENTRY, _Token.COMMENT, _State.COMMENT, ),
    ( _State.END_OF_ENTRY, _Token.PREV_MSGCTXT, _State.PREV_MSGCTXT, ),
    ( _State.END_OF_ENTRY, _Token.PREV_MSGID, _State.PREV_MSGID, ),
    ( _State.END_OF_ENTRY, _Token.MSGCTXT, _State.MSGCTXT, ),
    ( _State.END_OF_ENTRY, _Token.MSGID, _State.MSGID, ),
    ( _State.END_OF_ENTRY, _Token.EOF, _State.EOF, ),
    ( _State.ERROR, _Token.COMMENT, _State.END_OF_ENTRY, ),
    ( _State.ERROR, _Token.PREV_MSGCTXT, _State.END_OF_ENTRY, ),
    ( _State.ERROR, _Token.PREV_MSGID, _State.END_OF_ENTRY, ),
    ( _State.ERROR, _Token.PREV_MSGID_PLURAL, _State.ERROR_BEFORE_MSGID, ),
    ( _State.ERROR, _Token.PREV_TEXT, _State.ERROR_BEFORE_MSGID, ),
    ( _State.ERROR, _Token.MSGCTXT, _State.END_OF_ENTRY, ),
    ( _State.ERROR, _Token.MSGID, _State.END_OF_ENTRY, ),
    ( _State.ERROR, _Token.EOF, _State.END_OF_ENTRY, ),
)
# Other tokens cause the transition to an error state, which makes parse() skip until a msgid, msgid_plural, msgstr, or msgid_plural is appeared, and then find the start position of the next entry to recover.
_state_trans_table = [ [ _State.ERROR_BEFORE_MSGID ] * _Token.TOTAL for i in range(_State.TOTAL) ]
for i in range(_State.TOTAL):
    for j in range(_Token.TOTAL):
        if i == _State.ERROR or j == _Token.MSGID or j == _Token.MSGID_PLURAL or j == _Token.MSGSTR or j == _Token.MSGSTR_PLURAL:
            _state_trans_table[i][j] = _State.ERROR
for d in _state_trans_def:
    _state_trans_table[d[0]][d[1]] = d[2]

def parse(textfile_or_char_iter):
    '''parse a PO text comes from a text file, a string, or an iterable that returns a character.

    textfile must be an io.TextIOBase, so fileinput.input is not acceptable.

    The parser returns (1) PO entries (dict), (2) PO obsolete entries (dict), and (3) error messages.

    (1) and (2) extract the entries as the following form:
    {
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
            "column": column_number 1 origin),
        },
        ...
    }

    - "msgctxt + msgid" means "msgctxt string" + '\x04' + "msgid string" if msgctxt is specified, otherwise "msgid string".
    - The key doesn't exist if the entry doesn't have it, so the values of "fuzzy" and "obsolete" always are True.
    - "comment" doesn't contain the flag, reference, and previous untranslated string.

    (3) The error messages:
    [
        [ line_number, column_number, message ],
        ...
    ]
    Technically speaking, column_number is the position of the code point. It doesn't care about east asian width, combining character, or something.

    If there are error messages, the (1) and (2) may not contain some entries around the errors.
    '''
    if isinstance(textfile_or_char_iter, io.TextIOBase):
        c_itr = iter(functools.partial(textfile_or_char_iter.read, 1), '')
    else:
        c_itr = iter(textfile_or_char_iter)
    char_feeder = _CharFeeder(c_itr)
    token_feeder = _TokenFeeder(char_feeder)
    state = _State.END_OF_ENTRY
    po_entries = {}
    obsolete_entries = {}
    errors = []
    entry_data = {}
    entry_is_obsolete = None
    fuzzy = False
    n = 0
    keyword = None
    errors = []
    for token, obsolete, value, line, column in token_feeder:
        new_state = _state_trans_table[state][token]
        if new_state == _State.END_OF_ENTRY:
            if state != _State.ERROR:
                # register the current entry
                if 'flag' in entry_data and 'fuzzy' in entry_data['flag']:
                    entry_data['fuzzy'] = True
                msgid = entry_data['msgid']
                id = entry_data['msgctxt'] + '\x04' + msgid if 'msgctxt' in entry_data else msgid
                prev_line = None
                if id in po_entries:
                    prev_line = po_entries[id]['line']
                    prev_column = po_entries[id]['column']
                elif id in obsolete_entries:
                    prev_line = obsolete_entries[id]['line']
                    prev_column = obsolete_entries[id]['column']
                if prev_line is not None:
                    errors.append( ( entry_data['line'], entry_data['column'], f'Duplicate entry is found (the position of the previous entry is {prev_line},{prev_column})' ), )
                elif entry_is_obsolete:
                    entry_data['obsolete'] = True
                    obsolete_entries[id] = entry_data
                else:
                    po_entries[id] = entry_data
            # initialize the new entry
            entry_data = {}
            entry_is_obsolete = None
            fuzzy = False
            n = 0
            keyword = None
            new_state = _state_trans_table[new_state][token]
        if new_state == _State.ERROR or new_state == _State.ERROR_BEFORE_MSGID:
            if state != _State.ERROR and state != _State.ERROR_BEFORE_MSGID:
                # Report only the error that causes the transition to ERROR.
                if token == _Token.ERROR:
                    errors.append( ( line, column, value, ) )
                else:
                    kw_str = _token_str[token]
                    err_msg = f'Unexpected {kw_str}'
                    if token == _Token.EOF and ('comment' in entry_data or 'flag' in entry_data or 'reference' in entry_data) and 'line' not in entry_data:
                        # make the message more understandable.
                        err_msg += ' (orphaned comment is detected)'
                    elif _State.PREV_MSGCTXT <= state and state <= _State.PREV_MSGID_PLURAL:
                        err_msg += ' (#| quoted text is expected)'
                    elif _State.MSGCTXT <= state and state <= _State.MSGSTR_PLURAL:
                        err_msg += ' (quoted text is expected)'
                    errors.append( ( line, column, err_msg, ) )
        if token == _Token.ERROR:
            # Try to recover lexical error
            for c in char_feeder:
                if c == '\n':
                    char_feeder.ungetc(c)
                    break
        state = new_state
        # check obsolete status
        if entry_is_obsolete is not None:
            if _State.PREV_MSGCTXT <= state and state <= _State.MSGSTR_PLURAL_TEXT:
                if entry_is_obsolete != obsolete:
                    errors.append( ( line, column, f'Inconsistent #~ entry', ) )
                    state = _state_trans_table[_State.ERROR_BEFORE_MSGID][token]
        # handle state and token
        if state == _State.ERROR or state == _State.ERROR_BEFORE_MSGID:
            continue
        elif state == _State.EOF:
            break
        if state == _State.COMMENT:
            comment_to_add = True
            if len(value) >= 2:
                if value[1] == ',' or value[1] == '=':
                    flags = _parse_flag_comment(value[2:])
                    entry_data.setdefault('flag', [])
                    entry_data['flag'] += flags
                    comment_to_add = False
                elif value[1] == ':':
                    refs = _parse_reference_comment(value[2:])
                    entry_data.setdefault('reference', [])
                    entry_data['reference'] += refs
                    comment_to_add = False
            if comment_to_add:
                entry_data.setdefault('comment', []).append(value)
        elif state == _State.PREV_MSGCTXT:
            entry_is_obsolete = obsolete
            keyword = 'prev_msgctxt'
            entry_data[keyword] = ''
        elif state == _State.PREV_MSGID:
            entry_is_obsolete = obsolete
            keyword = 'prev_msgid'
            entry_data[keyword] = ''
        elif state == _State.PREV_MSGID_PLURAL:
            keyword = 'prev_msgid_plural'
            entry_data[keyword] = ''
        elif state == _State.MSGCTXT:
            entry_data.setdefault('line', line)
            entry_data.setdefault('column', column)
            entry_is_obsolete = obsolete
            keyword = 'msgctxt'
            entry_data[keyword] = ''
        elif state == _State.MSGID:
            entry_data.setdefault('line', line)
            entry_data.setdefault('column', column)
            entry_is_obsolete = obsolete
            keyword = 'msgid'
            entry_data[keyword] = ''
        elif state == _State.MSGID_PLURAL:
            keyword = 'msgid_plural'
            entry_data[keyword] = ''
        elif _State.PREV_MSGCTXT_TEXT <= state and state <= _State.MSGID_PLURAL_TEXT:
            entry_data[keyword] += value
        elif state == _State.MSGSTR:
            entry_data['msgstr'] = [ "" ]
        elif state == _State.MSGSTR_PLURAL:
            keyword = None
            if n == value:
                if n == 0:
                    entry_data['msgstr'] = [ "" ]
                else:
                    entry_data['msgstr'].append("")
                n += 1
            else:
                errors.append( ( line, column, f'Invalid n in msgstr[n]; n should be {n} but {value}', ) )
                state = _State.ERROR
        elif state == _State.MSGSTR_TEXT or state == _State.MSGSTR_PLURAL_TEXT:
            entry_data['msgstr'][-1] += value
    return po_entries, obsolete_entries, errors

if __name__ == "__main__":
    import fileinput
    import sys

    class CharIterFileInput:
        '''Iterator adaptor for fileinput.FileInput

        fileinput.FileInput doesn't have read() so this adaptor uses readline().

        This can use for the TextIOBase.
        '''
        def __init__(self, f):
            self._f = f
            self._line_buffer = ''
            self._index = 0
            self._eof = False
        def __iter__(self):
            return self
        def __next__(self):
            if len(self._line_buffer) <= self._index:
                self._line_buffer = self._f.readline()
                self._index = 0
                self._eof = len(self._line_buffer) == 0
            if self._eof:
                raise StopIteration
            c = self._line_buffer[self._index]
            self._index += 1
            return c

    f = CharIterFileInput(fileinput.input(encoding='utf-8'))
    po_entries, obsolete_entries, error_messages = parse(f)
    if len(error_messages) > 0:
        print("Error message:")
        for err in error_messages:
            print(f'{err[0]},{err[1]}: {err[2]}.')
    if len(po_entries) > 0:
        print("PO Entry:")
        for key, value in po_entries.items():
            print(f'"{key}": {value}')
    if len(obsolete_entries) > 0:
        print("Obsolete PO Entry:")
        for key, value in obsolete_entries.items():
            print(f'"{key}": {value}')
    sys.exit(0 if len(error_messages) == 0 else 1)
