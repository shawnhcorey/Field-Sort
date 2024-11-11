#!/usr/bin/env python3
'''
     Title: Field Sort
 Copyright: Copyright 2023 by Shawn H Corey. Some rights reserved.
     Usage: **/field_sort.py %T %t
            The command for this tool is: `**/field_sort.py %T %t`
            where `**` represents the path to the tool.

            `%T` is the selection with Zim markup.
            The fields are extracted from this.

            `%t` is the selected text without Zim markup.
            This is used for entire line sorting.

   Purpose: Sort Zim Desktop Wiki lines by fields.
   Licence: This file is part of Field Sort.

            Field Sort is free software: you can
            redistribute it and/or modify it under the terms of
            the GNU General Public License as published by the
            Free Software Foundation, either version 3 of the
            License, or (at your option) any later version.

            Field Sort is distributed in the hope that
            it will be useful, but WITHOUT ANY WARRANTY; without
            even the implied warranty of MERCHANTABILITY or
            FITNESS FOR A PARTICULAR PURPOSE. See the GNU
            General Public License for more details.

            You should have received a copy of the GNU General
            Public License along with Field Sort.
            If not, see <https://www.gnu.org/licenses/>.

            See LICENCE.md for details.
'''


# --------------------------------------
# Imports
import sys
import re
import numbers
import functools

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gettext
_ = gettext.gettext

import locale


# --------------------------------------
# constants
SUCCESS                    =  0
EXIT_STATUS_SORT_CANCELLED =  1
EXIT_STATUS_INTERNAL_ERROR = -1

SCROLL_BAR_SIZE   = 17  # needed to adapt to window size
ADDITIONAL_HEIGHT = 36  # needed to adapt to window size

EMPTY_STRING = ''

NUMBER_OF_COLUMNS  = 5
CONTROLS_START_ROW = 2

ENABLE_COLUMN     = 0
SORT_ON_COLUMN    = 1
SORT_AS_COLUMN    = 2
SORT_ORDER_COLUMN = 3
LANGUAGE_COLUMN   = 4

NARROW_MARGIN = 0
SIDE_MARGIN   = 5
WIDE_MARGIN   = 5

# --------------------------------------
# translatable strings
STRING_TITLE = _('Field Sort - Zim Desktop Wiki')

STRING_MSG  = _('No field selected')
STRING_MSG2 = _('No field has been select. This will cancel the sort. Do you wish to cancel?')

STRING_NONE  = _('None')
STRING_SORT_ON     = _('Sort on:')
STRING_THEN_ON     = _('Then on:')
STRING_ENTIRE_LINE = _('entire line')
STRING_SORT_AS     = _('Sort as:')
STRING_ORDER       = _('Order:')
STRING_LANGUAGE    = _('Language:')

STRING_SORT_BY_FIELDS   = _('Sort by fields')
STRING_NO_FIELDS_FOUND  = _('No fields found')
STRING_NUMBER_OF_FIELDS = _('Number of fields: ')
STRING_SORT_BY_LINES    = _('Sort by lines')

# consolidated strings for 'Sort as:'
STRING_TEXT      = _('Text')
STRING_NUMBER    = _('Number')
STRING_DATE      = _('Date')
STRING_TIME      = _('Time')
STRING_CURRENCY  = _('Currency')
STRING_VERSION   = _('Version')  # period is separator, not decimal point

# consolidated strings for 'Order:'
STRING_ASCENDING  = _('Ascending')
STRING_DESCENDING = _('Descending')

# --------------------------------------
# Theses strings are NOT to be translated
ID_TEXT   = 'text'
ID_NUMBER = 'number'

ID_ASCENDING  = 'ascending'
ID_DESCENDING = 'descending'

ID_NONE = 'none'

ID_ENTIRE_LINE = -1

Sort_as_list = {
    ID_TEXT: STRING_TEXT,
    ID_NUMBER: STRING_NUMBER,
}

Sort_order_list = {
    ID_ASCENDING:  STRING_ASCENDING,
    ID_DESCENDING: STRING_DESCENDING,
}

# --------------------------------------
# Globals

# this list is expanded dynamically
Language_list = {
    ID_NONE: STRING_NONE,
}

# These 3 variables are used to determine the locale for strcoll()
AppLocale   = None
AppEncoding = None
AppLanguage = None


# --------------------------------------
# Subroutines

# --------------------------------------
def load_languages():
    '''
          Name: load_languages
         Usage: load_languages()
       Purpose: Load the locals from ICU or system.
    Parameters: (none)
       Returns: (none)
    '''
    global AppLocale, AppLanguage

    # Load the app's locale data from its environment.
    # Note the 2nd call will not do anything if the 1st did.
    # That is, the 2nd call does nothing if the 1st worked.
    locale.setlocale(locale.LC_ALL, '')    # use user's default settings
    locale.setlocale(locale.LC_ALL, None)  # use current setting
    AppLocale, AppEncoding = locale.getlocale()

    if AppLocale:
        AppLanguage = AppLocale
        Language_list[AppLocale] = AppLanguage

    return


# --------------------------------------
def read_text():
    '''
          Name: read_text
         Usage: text, marked = read_text()
       Purpose: Get the text from the command-line.
    Parameters: (none)
       Returns: text   -- from command-line argument
                marked -- text with Zim wiki mark-ups
    '''
    # text is the unmarked selection. It is used for entire line sorts.
    # This tool must be called `**/field_sort.py %T %t`
    marked = sys.argv[1]
    text   = sys.argv[2]
    return text, marked


# --------------------------------------
def get_newline(marked):
    '''
          Name: get_newline
         Usage: frontage, newline, ending = get_newline(marked)
       Purpose: Preserve any multi-line spacing by extracting the
                newline from the first line in text. Also save any
                trailing newline of the text.
    Parameters: marked  -- many lines in one string
       Returns: frontage -- possible newlines ate front of text
                newline  -- may have blank lines
                ending   -- possible newline at end of text
    '''
    # Why do it this way? Why not use splitlines()?
    # Consider the following:
    #    '\n'.join(sorted('x\n\ny\n\na'.splitlines()))
    # gives: '\n\na\nx\ny'
    # and ''.join(sorted('x\n\ny\n\na'.splitlines(keepends=True)))
    # gives: '\n\nax\ny\n'
    # Neither is what the user expects.
    #
    # There are two problems.
    # The first is that the selection may not have a final newline.
    # The second is the lines to sort may be separated by a blank line.
    # The code before solves these problems, for most cases.
    #

    frontage = EMPTY_STRING
    found = re.search('^((?:\r?\n)+)', marked)
    if found:
        frontage = found.group(1)
    marked = re.sub('^(?:\r?\n)+', EMPTY_STRING, marked)   # remove leading blank lines, if any

    ending = EMPTY_STRING
    found = re.search('((?:\r?\n)+)$', marked)
    if found:
        ending = found.group(1)
    marked = re.sub('(?:\r?\n)+$', EMPTY_STRING, marked)   # remove trailing blank lines, if any

    newline = EMPTY_STRING
    found = re.search('((?:\r?\n)+)', marked)
    if found:
        newline = found.group(1)

    return frontage, newline, ending


# --------------------------------------
def get_lines(text):
    '''
          Name: get_lines
         Usage: lines = get_lines(text)
       Purpose: Extract the lines from the text.
    Parameters: (none)
       Returns: (none)
    '''
    # splitlines() does not handle blank lines between the lines to sort.
    # This code does.
    text = re.sub('^(?:\r?\n)+', EMPTY_STRING, text)   # remove leading newline, if any
    text = re.sub('(?:\r?\n)+$', EMPTY_STRING, text)   # remove trailing newline, if any
    lines = re.split('(?:\r?\n)+', text)
    return lines


# --------------------------------------
def get_fields(text, marked):
    '''
          Name: get_fields
         Usage: fields = get_fields(text, marked)
       Purpose: Extract the fields in each line. Fields are
                determined by leading and trailing double
                underscores. Together with the lines from both the
                unmarked and marked text, a tuple is created with the
                fields. This tuple is added to a tuple of tuples.
    Parameters: text   -- lines of unmarked text
                marked -- line of Zim marked text
       Returns: count  -- maximum number of fields
                fields -- a tuple of tuples
    '''
    # fields is a tuple of tuples
    # (
    #     (marked_line, unmarked_line, field_1, field_2, ..., ),
    #     ...,
    # )

    zipped = zip(get_lines(marked), get_lines(text))
    count = 0
    fields = ()
    for item in zipped:
        per_line = (item[0],)
        found = re.findall('__[^_]*(?:(?:_[^_]+))*__', item[0])
        cnt = 0
        for each in found:
            each = re.search(r'__(.*)__', each).group(1)
            per_line += (each, )
            cnt += 1
        per_line += (item[1], )
        fields += (per_line,)
        if count < cnt:
            count = cnt

    return count, fields


# --------------------------------------
def set_margins(widget, left, top=None, right=None, bottom=None):
    '''
          Name: set_margins
         Usage: set_margins(widget, left, top, right, bottom)
       Purpose: Do all margins at once.
    Parameters: widget -- what to modify
                left   -- left margin
                top    -- top margin, default left
                right  -- right margin, default left
                bottom -- bottom margin, default top
       Returns: (none)
    '''
    if top is None:
        top = left
    if right is None:
        right = left
    if bottom is None:
        bottom = top
    widget.set_margin_start(left)
    widget.set_margin_top(top)
    widget.set_margin_end(right)
    widget.set_margin_bottom(bottom)


# --------------------------------------
def sort_controls(grid, row, field, count):
    '''
          Name: sort_controls
         Usage: controls = sort_controls(grid, after_row, field_number, count_of_fields)
       Purpose: Create a set of controls for the sort and insert
                them into the grid after the row.
    Parameters: grid            -- where the controls will be shown
                after_row       -- index after which the controls are
                                   added to the grid
                field_number    -- used as default for SpinButton
                count_of_fields -- maximum for SpinButton
       Returns: controls        -- controls created
    '''
    controls = ()

    # en-/disable control
    if field>0 or count>0:
        ctl = Gtk.CheckButton()
        ctl.set_active(field>0)
        set_margins(ctl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
        grid.attach(ctl, ENABLE_COLUMN, row, 1, 2)
        controls += (ctl,)
    else:
        controls += (None,)

    # field order
    if row == CONTROLS_START_ROW or count == 0:
        lbl = Gtk.Label(label=STRING_SORT_ON)
    else:
        lbl = Gtk.Label(label=STRING_THEN_ON)
    set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, NARROW_MARGIN)
    grid.attach(lbl, SORT_ON_COLUMN, row, 1, 1)
    if field > 0:
        ctl = Gtk.ComboBoxText()
        for idx in range(0, count):
            ctl.append(str(idx+1), str(idx+1))
        ctl.set_active(field-1)
        set_margins(ctl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
        grid.attach(ctl, SORT_ON_COLUMN, row+1, 1, 1)
        controls += (ctl,)
    else:
        lbl = Gtk.Label(label=STRING_ENTIRE_LINE)
        set_margins(lbl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
        grid.attach(lbl, SORT_ON_COLUMN, row+1, 1, 1)
        controls += (None,)

    # datatype
    lbl = Gtk.Label(label=STRING_SORT_AS)
    set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, NARROW_MARGIN)
    grid.attach(lbl, SORT_AS_COLUMN, row, 1, 1)
    ctl = Gtk.ComboBoxText()
    for item in Sort_as_list.items():
        ctl.append(item[0],item[1])
    ctl.set_active_id(ID_TEXT)
    set_margins(ctl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
    grid.attach(ctl, SORT_AS_COLUMN, row+1, 1, 1)
    controls += (ctl,)

    # order
    lbl = Gtk.Label(label=STRING_ORDER)
    set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, NARROW_MARGIN)
    grid.attach(lbl, SORT_ORDER_COLUMN, row, 1, 1)
    ctl = Gtk.ComboBoxText()
    for item in Sort_order_list.items():
        ctl.append(item[0],item[1])
    ctl.set_active_id(ID_ASCENDING)
    set_margins(ctl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
    grid.attach(ctl, SORT_ORDER_COLUMN, row+1, 1, 1)
    controls += (ctl,)

    # language
    lbl = Gtk.Label(label=STRING_LANGUAGE)
    set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, NARROW_MARGIN)
    grid.attach(lbl, LANGUAGE_COLUMN, row, 1, 1)
    ctl = Gtk.ComboBoxText()
    for item in Language_list.items():
        ctl.append(item[0],item[1])
    ctl.set_active_id(AppLanguage)
    set_margins(ctl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
    grid.attach(ctl, LANGUAGE_COLUMN, row+1, 1, 1)
    controls += (ctl,)

    return controls


# --------------------------------------
class SortkeyDialog(Gtk.Dialog):
    '''
          Name: SortkeyDialog
         Usage: dialog = SortkeyDialog(parent)
       Purpose: A dialog that allows the user determine what fields
                are sorted, the manner of the sort, and whether
                sorted in ascending or descending order.
    Parameters: parent -- The parent window (`None` if no parent)
       Returns: dialog -- The dialog window
    '''
    def __init__(self, parent):
        super().__init__(title=STRING_TITLE, transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,     Gtk.ResponseType.OK
        )
        ok_btn = self.get_widget_for_response(Gtk.ResponseType.OK)
        self.set_focus(ok_btn)


    # ----------------------------------
    def show_guts(self, count):
        '''
              Name: show_guts
             Usage: dialog.show_guts(count)
           Purpose: Add the controls to the dialog and show them.
                    This cannot be done in __init__() since it needs the argument `count`.
        Parameters: count -- initial number of keys to display
           Returns: (none)
        '''

        # build the guts
        content_area = self.get_content_area()

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        self.grid = Gtk.Grid()

        subtitle = Gtk.Label(label=STRING_SORT_BY_FIELDS)
        self.grid.attach(subtitle, 0, 0, NUMBER_OF_COLUMNS, 1)

        if count == 0:
            fields_count = Gtk.Label(label=STRING_NO_FIELDS_FOUND)
        else:
            fields_count = Gtk.Label(label=STRING_NUMBER_OF_FIELDS+str(count))
        self.grid.attach(fields_count, 0, 1, NUMBER_OF_COLUMNS, 1)

        self.controls = ()
        for i in range(0, count):
            ctls = sort_controls(self.grid, i*2+CONTROLS_START_ROW, i+1, count)
            self.controls += (ctls,)

        # can also sort by entire lines
        subtitle = Gtk.Label(label=STRING_SORT_BY_LINES)
        self.grid.attach(subtitle, 0, count*2+CONTROLS_START_ROW, NUMBER_OF_COLUMNS, 1)
        ctls = sort_controls(self.grid, count*2+CONTROLS_START_ROW+1, ID_ENTIRE_LINE, count)
        self.controls += (ctls,)

        # show the guts
        scrolled.add(self.grid)
        content_area.add(scrolled)
        self.show_all()

        # set the correct height
        content_rectangle = self.grid.get_allocation()
        self.resize(content_rectangle.width+SCROLL_BAR_SIZE,
                    content_rectangle.height+SCROLL_BAR_SIZE
                    + ADDITIONAL_HEIGHT)


    # ----------------------------------
    def get_sortkeys(self,count):
        '''
              Name: get_sortkeys
             Usage: sortkeys = dialog.get_sortkeys()
           Purpose: Get the parameters of how the user wants to sort.
        Parameters: count    -- initial number of keys to display
           Returns: sortkeys -- a tuple of tuple of the parameters of the sort
        '''
        sortkeys = ()

        # rows have checkbutton for enable/disable
        for idx in range(0,len(self.controls)):
            enabled = self.controls[idx][ENABLE_COLUMN]
            if enabled is None:
                enabled = 1
            else:
                enabled = self.controls[idx][ENABLE_COLUMN].get_active()
            if enabled:
                sort_on = self.controls[idx][SORT_ON_COLUMN]
                if sort_on is None:
                    sort_on = str(ID_ENTIRE_LINE)
                else:
                    sort_on = self.controls[idx][SORT_ON_COLUMN].get_active_id()
                sortkeys += ((
                    sort_on,
                    self.controls[idx][SORT_AS_COLUMN].get_active_id(),
                    self.controls[idx][SORT_ORDER_COLUMN].get_active_id(),
                    self.controls[idx][LANGUAGE_COLUMN].get_active_id(),
                ),)

        return sortkeys


# --------------------------------------
def query_sortkeys(count):
    '''
          Name: query_sortkeys
         Usage: status, sortkeys = query_sortkeys(count)
       Purpose: Run a GTK Dialog to get the sortkeys.
    Parameters: count    -- number of fields
       Returns: status   -- 0 == OK button, proceed with sort
                            1 == cancel sort
                sortkeys -- tuple of sortkeys
    '''
    status = SUCCESS
    sortkeys = ()

    msgbx  = None
    dialog = SortkeyDialog(None)
    dialog.show_guts(count)

    while(True):
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            sortkeys = dialog.get_sortkeys(count)
            if sortkeys:
                break

            # popup asking to continue with sort or cancel
            if not msgbx:
                msgbx = Gtk.MessageDialog(
                    transient_for=dialog,
                    flags=0,
                    message_type=Gtk.MessageType.QUESTION,
                    buttons=Gtk.ButtonsType.YES_NO,
                    text = STRING_MSG,
                )
                msgbx.format_secondary_text(STRING_MSG2)
            msgbx.show()
            response = msgbx.run()
            if response == Gtk.ResponseType.YES:
                status = EXIT_STATUS_SORT_CANCELLED
                break
            msgbx.hide()
        else:
            # dialog was cancelled
            status = EXIT_STATUS_SORT_CANCELLED
            break

    dialog.hide()

    return status, sortkeys


# --------------------------------------
def cmp_simple_ascend(a, b):
    '''
          Name: cmp_simple_ascend
         Usage: cmp = cmp_simple_ascend(a, b)
       Purpose: Do a simple compare.
    Parameters: a -- simple type eg str, int, float
                b -- simple type eg str, int, float
       Returns: cmp -- 1 if a>b, 0 if a==b, -1 if a<b
    '''

    try:
        return (a>b)-(a<b)
    except:
        if type(a) is str:
            return 1
        elif type(b) is str:
            return -1
        else:
            return 0


# --------------------------------------
def cmp_simple_descend(a, b):
    '''
          Name: cmp_simple_descend
         Usage: cmp = cmp_simple_descend(a, b)
       Purpose: Do a simple compare but descending.
    Parameters: a -- simple type eg str, int, float
                b -- simple type eg str, int, float
       Returns: cmp -- 1 if a<b, 0 if a==b, -1 if a>b
    '''
    try:
        return (a<b)-(a>b)
    except:
        if type(a) is str:
            return -1
        elif type(b) is str:
            return 1
        else:
            return 0


# --------------------------------------
def cmp_collate_ascend(a,b):
    '''
          Name: cmp_collate_ascend
         Usage: cmp = cmp_collate_ascend(a,b)
       Purpose: Compare 2 strings using the locale ascending.
    Parameters: a -- any string
                b -- any string
       Returns: cmp -- 1 if a>b, 0 if a==b, -1 if a<b
    '''
    cmp = locale.strcoll(a,b)
    return cmp


# --------------------------------------
def cmp_collate_descend(a,b):
    '''
          Name: cmp_collate_descend
         Usage: cmp = cmp_collate_descend(a,b)
       Purpose: Compare 2 strings using the locale descending.
    Parameters: a -- any string
                b -- any string
       Returns: cmp -- 1 if a<b, 0 if a==b, -1 if a>b
    '''
    return locale.strcoll(b,a)


# --------------------------------------
def assign_keys(fields, sortkeys):
    '''
          Name: assign_keys
         Usage: keyed = assign_keys(fields, sortkeys)
       Purpose: Assign a sortkey to each field in fields
    Parameters: fields   -- ((marked,line,field1,field2,...),...)
                sortkeys -- ((field#,sort_as,type,order),...)
       Returns: keyed    -- ((marked,(field,sort_as,type,wants_descending)),...)
    '''

    keyed = ()
    for field in fields:

        keys_list = (field[0],)
        for sortkey in sortkeys:

            # check for missing fields
            sort_value = EMPTY_STRING
            if int(sortkey[0]) < len(field)-1:
                sort_value = field[int(sortkey[0])]

            sort_as    = sortkey[1]
            sort_order = sortkey[2]
            sort_lang  = sortkey[3]

            if sort_lang == ID_NONE:
                if sort_as == ID_TEXT:
                    if sort_order == ID_DESCENDING:
                        key = (sort_value,cmp_simple_descend,)
                    else:
                        key = (sort_value,cmp_simple_ascend,)
                elif sort_as == ID_NUMBER:
                    try:
                        sort_value = float(sort_value)
                    except:
                        # ignore all exceptions; use sort_value as is
                        pass
                    if sort_order == ID_DESCENDING:
                        key = (sort_value,cmp_simple_descend,)
                    else:
                        key = (sort_value,cmp_simple_ascend,)
            else:
                if sort_as == ID_TEXT:
                    if sort_order == ID_DESCENDING:
                        key = (sort_value,cmp_collate_descend,)
                    else:
                        key = (sort_value,cmp_collate_ascend,)
                elif sort_as == ID_NUMBER:
                    try:
                        sort_value = float(locale.delocalize(sort_value))
                    except:
                        # ignore all exceptions; use sort_value as is
                        pass
                    if sort_order == ID_DESCENDING:
                        key = (sort_value,cmp_simple_descend,)
                    else:
                        key = (sort_value,cmp_simple_ascend,)

            keys_list += (key,)
        keyed += (keys_list,)

    return keyed


# --------------------------------------
def cmp_fields(a, b):
    '''
          Name: cmp_fields
         Usage: cmp = cmp_fields(a, b)
       Purpose: Complex compare of 2 fields
    Parameters: a -- (marked_line,[value,type,language,wants_descending],...)
                b -- (marked_line,[value,type,language,wants_descending],...)
       Returns: cmp -- 1 if a>b, 0 if a==b, -1 if a<b
    '''
    for idx in range(1,len(a)):
        cmp_func = a[idx][1]
        cmp = cmp_func(a[idx][0],b[idx][0])
        if cmp != 0:
            return cmp

    return 0


# --------------------------------------
def sort_fields(keyed):
    '''
          Name: sort_fields
         Usage: ordered = sort_fields(keyed)
       Purpose: Do the sort.
    Parameters: keyed   -- ((marked,(field,sort_as,type,wants_descending)),...)
       Returns: ordered -- sorted marked lines
    '''

    # Do not reverse the sort. Reverse is done individually by field.
    # That is, some fields may be ascending and others descending.
    # Reversing has to been deep in the sort per field.
    ordered = sorted(keyed, key=functools.cmp_to_key(cmp_fields))
    return ordered


# --------------------------------------
def extract_marked(ordered):
    '''
          Name: extract_marked
         Usage: lines = extract_marked(ordered)
       Purpose: Extract the marked text from a complex structure.
    Parameters: ordered -- ((line,stuff...),...)
       Returns: lines -- the lines from the structure
    '''
    lines = ()
    for item in ordered:
        lines += (item[0],)
    return lines


# --------------------------------------
def main():
    '''
          Name: main
         Usage: main()
       Purpose: Isolates execution of the program from importing.
    Parameters: (none)
       Returns: (none)
    '''
    load_languages()

    text,     marked          = read_text()
    frontage, newline, ending = get_newline(marked)        # also preserves trailing blank lines
    count,    fields          = get_fields(text, marked)   # fields also contain unmarked & marked lines

    status, sortkeys = query_sortkeys(count)
    if status != SUCCESS:   # user cancelled sort
        print(marked, end=EMPTY_STRING)   # marked has its own newline at end
        exit(status)

    keyed   = assign_keys(fields, sortkeys)
    ordered = sort_fields(keyed)
    lines   = extract_marked(ordered)
    marked  = newline.join(lines)
    print(frontage, marked, sep=EMPTY_STRING, end=ending)


# don't execute if imported
if __name__ == '__main__':
    main()

