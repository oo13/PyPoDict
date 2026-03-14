#!/usr/bin/python3
'''PO dumper

The format option, such as width, is not supported. Use msgcat of GNU gettext tools.
'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import io

_escape_map = {
    '\a': '\\a',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
    '\v': '\\v',
    '\\': '\\\\',
    '"': '\\"',
}

def to_quote_text(text, joiner=None):
    '''escape characters, split lines, and quote the text.

    if joiner is None:
        Return a list of some double quoted texts.
    else:
        Retrun a txts joined by joiner.
    '''
    result = []
    s = '"'
    has_lf = False
    for c in text:
        c2 = c
        if c in _escape_map:
            c2 = _escape_map[c]
        s += c2
        if c == '\n':
            has_lf = True
            s += '"'
            result.append(s)
            s = '"'
    if len(result) == 0 or len(s) > 1:
        s += '"'
        result.append(s)
    if has_lf:
        result.insert(0, '""')
    if joiner is None:
        return result
    else:
        return joiner.join(result)

def _dump_reference(ref_data):
    ''' dump reference data'''
    out = '#:'
    for ref in ref_data:
        if ' ' in ref[0] or '\t' in ref[0]:
            out += f' \u2068{ref[0]}\u2069'
        else:
            out += f' {ref[0]}'
        if ref[1] is not None:
            out += f':{ref[1]}'
    return out

def _dump_flag(flag_data):
    ''' dump flag data'''
    out = '#'
    for flag in flag_data:
        out += ', ' + flag
    return out

def _dump_an_entry(out, po_ent, wrap_width=None):
    '''dump an entry'''
    msg_head = '#~ ' if 'obsolete' in po_ent else ''
    jo = f'\n{msg_head}'
    jo2 = f'\n{msg_head}#| '
    if 'comment' in po_ent:
        for comment in po_ent['comment']:
            out.write(comment)
            out.write('\n')
    if 'reference' in po_ent:
        out.write(_dump_reference(po_ent['reference']) + '\n')
    if 'flag' in po_ent:
        out.write(_dump_flag(po_ent['flag']) + '\n')
    if 'prev_msgctxt' in po_ent:
        prev_msgctxt = to_quote_text(po_ent['prev_msgctxt'], jo2)
        out.write(f'{msg_head}#| msgctxt {prev_msgctxt}\n')
    if 'prev_msgid' in po_ent:
        prev_msgid = to_quote_text(po_ent['prev_msgid'], jo2)
        out.write(f'{msg_head}#| msgid {prev_msgid}\n')
    if 'prev_msgid_plural' in po_ent:
        prev_msgid_plural = to_quote_text(po_ent['prev_msgid_plural'], jo2)
        out.write(f'{msg_head}#| msgid_plural {prev_msgid_plural}\n')
    if 'msgctxt' in po_ent:
        msgctxt = to_quote_text(po_ent['msgctxt'], jo)
        out.write(f'{msg_head}msgctxt {msgctxt}\n')
    msgid = to_quote_text(po_ent['msgid'], jo)
    out.write(f'{msg_head}msgid {msgid}\n')
    if 'msgid_plural' in po_ent:
        msgid_plural = to_quote_text(po_ent['msgid_plural'], jo)
        out.write(f'{msg_head}msgid_plural {msgid_plural}\n')
        for i, msgstr in enumerate(po_ent['msgstr']):
            msgstr = to_quote_text(msgstr, jo)
            out.write(f'{msg_head}msgstr[{i}] {msgstr}\n')
    else:
        msgstr = to_quote_text(po_ent['msgstr'][0], jo)
        out.write(f'{msg_head}msgstr {msgstr}\n')

def dump(out, po_entries):
    '''dump PO entries to a file

    The order to output the entry is the same as the order that they are inserted.
    '''
    first_entry = True
    for entry in po_entries.values():
        if first_entry:
            first_entry = False
        else:
            out.write('\n')
        _dump_an_entry(out, entry)

def dumps(po_entries):
    '''dump PO entries to a string'''
    s = io.StringIO()
    dump(s, po_entries)
    return s.getvalue()

if __name__ == "__main__":
    import fileinput
    import sys
    import parse
    f = parse.CharIterFileInput(fileinput.input(encoding='utf-8'))
    po_entries, obsolete_entries, error_messages = parse.parse(f)
    if len(error_messages) > 0:
        print("Error message:")
        for err in error_messages:
            print(f'{err[0]},{err[1]}: {err[2]}.')
        sys.exit(1)
    else:
        po_entries.update(obsolete_entries)
        dump(sys.stdout, po_entries)
        # s = dumps(po_entries)
        # print(s, end='')
        sys.exit(0)
