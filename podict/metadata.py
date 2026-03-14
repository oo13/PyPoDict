#!/usr/bin/python3
'''PO metadata parser/dumper'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import enum
import string

class _State(enum.Enum):
    NAME = enum.auto()
    WSP = enum.auto()
    BODY = enum.auto()
    ERROR = enum.auto()

_wsp = ' \t'

def parse(metadata_str):
    '''convert the string form to the dict form

    return dict, error_messages

    error_messages:
    [
        ( line_number, column_number, message, ),
        ...
    ]

    Some data are lost if len(error_messages) > 0.

    Assumed format of a line in the metadata:
    field_name, [ ":", (' ' | '\t')*, field_body ], '\n'

    field_name accepts any characters other than ':' and '\n'; folding is not supported.
    The value for field_name is None if ':' is omitted.

    Someone says the format of the metadata is RFC822, but I don't find the evidence. In fact, GNU gettext tools just search the keywords "charset=", "nplurals=", and "plural=".
    '''
    if not isinstance(metadata_str, str):
        # Reject a common error where setting entries['']['msgstr'] to the parameter.
        raise TypeError("The argument must be a string")
    metadata = {}
    error_messages = []
    state = _State.NAME
    name = ''
    body = None
    line = 1
    column = 1
    for c in metadata_str:
        if state == _State.NAME:
            if c == ':' or c == '\n':
                if name in metadata:
                    error_messages.append( ( line, 1, f'Duplicate field name "{name}" is found', ) )
                    name = ''
                    if c == ':':
                        state = _State.ERROR
                elif c == ':':
                    body = ''
                    state = _State.WSP
                else:
                    metadata[name] = None
                    name = ''
            else:
                name += c
        elif state == _State.WSP or state == _State.BODY:
            if c in _wsp and state == _State.WSP:
                pass
            elif c == '\n':
                metadata[name] = body
                name = ''
                state = _State.NAME
            else:
                body += c
                state = _State.BODY
        elif state == _State.ERROR:
            name = ''
            if c == '\n':
                state = _State.NAME
        else: 
           raise AssertionError('Unknown state')
        if c == '\n':
            line += 1
            column = 1
        else:
            column += 1
    if not (state == _State.NAME and name == ''):
        error_messages.append( ( line, column, 'Unterminated field is found (Missing the last \\n)', ) )
    return metadata, error_messages

def dumps(metadata):
    '''convert the dict form to the string form.'''
    s = ''
    for name, body in metadata.items():
        if body is None:
            s = ''.join( ( s, name, '\n', ) )
        else:
            s = ''.join( ( s, name, ': ', body, '\n', ) )
    return s

_charset_delim = ' \t\n'
def get_charset(metadata_str):
    '''Get the value for "charset" from the metadata.

    Extract the value for "charset" in a way that is compatible with GNU gettext tools.

    Return None or a string.

    Note: This library supports only UTF-8.
    '''
    if not isinstance(metadata_str, str):
        # Reject a common error where setting entries['']['msgstr'] to the parameter.
        raise TypeError("The argument must be a string")
    keyword = 'charset='
    i = metadata_str.find(keyword)
    if i < 0:
        return None
    i += len(keyword)
    value = ''
    for c in metadata_str[i:]:
        if c in _charset_delim:
            break
        else:
            value += c
    return value

_plural_delim = ';\n'
def get_plural(metadata_str):
    '''Get the values for "nplurals" and "plural" from the metadata.

    Extract the value for "nplurals" and "plural" in a way that is compatible with GNU gettext tools.

    Return A tuple of two elements, and the element is None or a string.
    '''
    if not isinstance(metadata_str, str):
        # Reject a common error where setting entries['']['msgstr'] to the parameter.
        raise TypeError("The argument must be a string")
    keyword = 'nplurals='
    i = metadata_str.find(keyword)
    if i < 0:
        nplurals = None
    else:
        i += len(keyword)
        nplurals = ''
        for c in metadata_str[i:]:
            if c not in string.digits:
                break
            else:
                nplurals += c
    keyword = 'plural='
    i = metadata_str.find(keyword)
    if i < 0:
        plural = None
    else:
        i += len(keyword)
        plural = ''
        for c in metadata_str[i:]:
            if c in _plural_delim:
                break
            else:
                plural += c
    return ( nplurals, plural, )
