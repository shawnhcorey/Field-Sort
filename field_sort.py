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


# Imports
import sys
import re
import numbers
import functools

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gettext
_T = gettext.gettext


# constants
EXIT_STATUS_SORT_CANCELLED =  2
EXIT_STATUS_INTERNAL_ERROR = -1

EMPTY_STRING = ''

NUMBER_OF_COLUMNS  = 5
CONTROLS_START_ROW = 2

NARROW_MARGIN = 0
SIDE_MARGIN   = 5
WIDE_MARGIN   = 5

# consolidated strings
STRING_NONE = _T("None")

# consolidated strings for 'Sort as:'
STRING_TEXT    = _T("Text")
STRING_NUMBERS = _T("Numbers")

# consolidated strings for 'Order:'
STRING_ASCENDING  = _T("Ascending")
STRING_DESCENDING = _T("Descending")

SORT_AS_LIST = (
    STRING_TEXT,
    STRING_NUMBERS,
)
SORT_ORDER_LIST = (
    STRING_ASCENDING,
    STRING_DESCENDING,
)

# global variables

# this list is expanded dynamically
LocaleList = (
    STRING_NONE,
)

# code


def number_or_zero(string):
    '''
          Name: number_or_zero
         Usage: number = number_or_zero(string)
       Purpose: Converts a string to a number if possible, or returns zero
    Parameters: string  -- text
       Returns: number -- True if a number
    '''
    try:
        return float(string)
    except ValueError:
        return 0


def get_text():
    '''
          Name: get_text
         Usage: text, marked = get_text()
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
    marked = re.sub('^(?:\r?\n)+', EMPTY_STRING, marked)   # remove leading newline, if any

    ending = EMPTY_STRING
    found = re.search('((?:\r?\n)+)$', marked)
    if found:
        ending = found.group(1)
    marked = re.sub('(?:\r?\n)+$', EMPTY_STRING, marked)   # remove trailing newline, if any

    newline = EMPTY_STRING
    found = re.search('((?:\r?\n)+)', marked)
    if found:
        newline = found.group(1)

    return frontage, newline, ending


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
        per_line = (item[0], item[1])
        found = re.findall('__[^_]*(?:(?:_[^_]+))*__', item[0])
        cnt = 0
        for each in found:
            each = re.search('__(.*)__', each).group(1)
            per_line = per_line + (each, )
            cnt = cnt + 1
        fields = fields + (per_line, )
        if count < cnt:
            count = cnt
    return count, fields


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
    if top == None:
        top = left
    if right == None:
        right = left
    if bottom == None:
        bottom = top
    widget.set_margin_start(left)
    widget.set_margin_top(top)
    widget.set_margin_end(right)
    widget.set_margin_bottom(bottom)


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
       Returns: controls        -- for future manipulations
    '''
    controls = ()

    # en-/disable control
    if row > CONTROLS_START_ROW and count > 0:
        ctl = Gtk.CheckButton()
        ctl.set_active(field>1)
        set_margins(ctl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
        grid.attach(ctl, 0, row, 1, 2)
        controls += (ctl,)
    else:
        lbl = Gtk.Label(label=' ')
        set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
        grid.attach(lbl, 0, row, 1, 2)
        if count == 0:
            controls += (0,)

    # field order
    if row == CONTROLS_START_ROW or count == 0:
        lbl = Gtk.Label(label=_T("Sort on:"))
    else:
        lbl = Gtk.Label(label=_T("Then on:"))
    set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, NARROW_MARGIN)
    grid.attach(lbl, 1, row, 1, 1)
    if field > 0:
        ctl = Gtk.SpinButton()
        ctl.set_adjustment(Gtk.Adjustment(value=field, lower=1, upper=count, step_increment=1))
        ctl.set_increments(1,1)
        ctl.set_numeric(True)
        ctl.set_value(field)
        set_margins(ctl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
        grid.attach(ctl, 1, row+1, 1, 1)
        controls += (ctl,)
    else:
        lbl = Gtk.Label(label=_T("entire line"))
        set_margins(lbl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
        grid.attach(lbl, 1, row+1, 1, 1)

    # datatype
    lbl = Gtk.Label(label=_T("Sort as:"))
    set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, NARROW_MARGIN)
    grid.attach(lbl, 2, row, 1, 1)
    ctl = Gtk.ComboBoxText()
    for idx, sort_as_text in enumerate(SORT_AS_LIST):
        ctl.append(str(idx), sort_as_text)
    ctl.set_active(0)
    set_margins(ctl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
    grid.attach(ctl, 2, row+1, 1, 1)
    controls += (ctl,)

    # locale
    lbl = Gtk.Label(label=_T("Locale:"))
    set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, NARROW_MARGIN)
    grid.attach(lbl, 3, row, 1, 1)
    ctl = Gtk.ComboBoxText()
    for idx, sort_as_text in enumerate(LocaleList):
        ctl.append(str(idx), sort_as_text)
    ctl.set_active(0)
    set_margins(ctl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
    grid.attach(ctl, 3, row+1, 1, 1)
    controls += (ctl,)

    # order
    lbl = Gtk.Label(label=_T("Order:"))
    set_margins(lbl, SIDE_MARGIN, WIDE_MARGIN, SIDE_MARGIN, NARROW_MARGIN)
    grid.attach(lbl, 4, row, 1, 1)
    ctl = Gtk.ComboBoxText()
    for idx, sort_as_text in enumerate(SORT_ORDER_LIST):
        ctl.append(str(idx), sort_as_text)
    ctl.set_active(0)
    set_margins(ctl, SIDE_MARGIN, NARROW_MARGIN, SIDE_MARGIN, WIDE_MARGIN)
    grid.attach(ctl, 4, row+1, 1, 1)
    controls += (ctl,)

    return controls


class SortkeyDialog(Gtk.Dialog):
    '''
          Name: SortkeyDialog
         Usage: dialog = SortkeyDialog(parent)
       Purpose: A dialog that allows the user determine what fields
                are sorted, tha manner of the sort, and whether
                sorted in ascending or descending order.
    Parameters: parent -- The parent window (`None` if no parent)
       Returns: dialog -- The dialog window
    '''
    def __init__(self, parent):
        super().__init__(title=_T("Field Sort - Zim Desktop Wiki"), transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,     Gtk.ResponseType.OK
        )
        ok_btn = self.get_widget_for_response(Gtk.ResponseType.OK)
        self.set_focus(ok_btn)


    def show(self, count):
        '''
              Name: show
             Usage: dialog.show(count)
           Purpose: add the controls to the dialog
        Parameters: count -- initial number of keys to display
           Returns: (none)
        '''

        self.set_default_size(600, 600)

        # build the guts
        content_area = self.get_content_area()

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        self.grid = Gtk.Grid()

        subtitle = Gtk.Label(label=_T("Sort by Fields"))
        self.grid.attach(subtitle, 0, 0, NUMBER_OF_COLUMNS, 1)

        if count == 0:
            fields_count = Gtk.Label(label=_T(f"No fields found"))
        else:
            fields_count = Gtk.Label(label=_T(f"Number of fields: {count}"))
        self.grid.attach(fields_count, 0, 1, NUMBER_OF_COLUMNS, 1)

        self.controls = ()
        for i in range(0, count):
            ctls = sort_controls(self.grid, i*2+CONTROLS_START_ROW, i+1, count)
            self.controls += (ctls,)

        # can also sort by entire lines
        subtitle = Gtk.Label(label=_T("Sort by Lines"))
        self.grid.attach(subtitle, 0, count*2+CONTROLS_START_ROW, NUMBER_OF_COLUMNS, 1)
        ctls = sort_controls(self.grid, count*2+CONTROLS_START_ROW+1, 0, count)
        self.controls += (ctls,)

        # show the controls
        scrolled.add(self.grid)
        content_area.add(scrolled)
        self.show_all()


    def get_sortkeys(self,count):
        '''
              Name: get_sortkeys
             Usage: sortkeys = dialog.get_sortkeys()
           Purpose: Get the parameters of how the user wants to sort.
        Parameters: count    -- initial number of keys to display
           Returns: sortkeys -- a tuple of tuple of the parameters of the sort
        '''
        sortkeys = ()

        if count > 0:
            # first row has 4 controls
            sortkeys = ((
                self.controls[0][0].get_value(),
                self.controls[0][1].get_active_text(),
                self.controls[0][2].get_active_text(),
                self.controls[0][3].get_active_text(),
            ),)

        # other rows have checkbutton for enable/disable
        for idx in range(1,len(self.controls)-1):
            if self.controls[idx][0].get_active():
                sortkeys += ((
                    self.controls[idx][1].get_value(),
                    self.controls[idx][2].get_active_text(),
                    self.controls[idx][3].get_active_text(),
                    self.controls[idx][4].get_active_text(),
                ),)

        # do entire line
        if count == 0 or(isinstance(self.controls[-1][0], Gtk.CheckButton)
            and self.controls[-1][0].get_active()):
            sortkeys += ((
                0,
                self.controls[-1][1].get_active_text(),
                self.controls[-1][2].get_active_text(),
                self.controls[-1][3].get_active_text(),
            ),)

        return sortkeys


def query_sortkeys(count, fields):
    '''
          Name: query_sortkeys
         Usage: status, sortkeys = query_sortkeys(count, fields)
       Purpose: Run a GTK Dialog to get the sortkeys.
    Parameters: count    -- number of fields
                fields   -- a tuple of tuples with marked, text, and fields
       Returns: status   -- 0 == OK button, proceed with sort
                            1 == cancel sort
                sortkeys -- tuple of sortkeys
    '''
    status = 0  # zero is success
    sortkeys = ()

    dialog = SortkeyDialog(None)
    dialog.show(count)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        sortkeys = dialog.get_sortkeys(count)
    else:
        # dialog was cancelled
        status = EXIT_STATUS_SORT_CANCELLED

    dialog.destroy()

    return status, sortkeys


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
        item = (field[0],)
        for sortkey in sortkeys:
            if int(sortkey[0]+1.01) < len(field):
                sort_on = field[int(sortkey[0]+1.01)]
            else:
                sort_on = None
            element = [sort_on,
                        sortkey[1],
                        sortkey[2],
                        sortkey[3] == STRING_DESCENDING,
                    ]
            # do some preconditioning
            if element[2] == STRING_NONE:
                if element[1] == STRING_NUMBERS:
                    element[0] = number_or_zero(element[0])

            item += (element,)

        keyed += (item,)

    return keyed


def cmp_simple(a, b, wants_descending):
    '''
          Name: cmp_simple
         Usage: cmp = cmp_simple(a, b)
       Purpose: Do a simple compare.
    Parameters: a -- simple type eg str, int, float
                b -- simple type eg str, int, float
       Returns: cmp -- 1 if a>b, 0 if a==b, -1 if a<b
    '''
    if a is None and b is None:
        return 0
    if a is None:
        return -1
    if b is None:
        return 1
    cmp = (a > b) - (a < b)
    if wants_descending:
        cmp = -cmp
    return cmp


def cmp_fields(a, b):
    '''
          Name: cmp_fields
         Usage: cmp = cmp_fields(a, b)
       Purpose: Complex compare of 2 fields
    Parameters: a -- (marked_line,[value,type,locale,wants_descending],...)
                b -- (marked_line,[value,type,locale,wants_descending],...)
       Returns: cmp -- 1 if a>b, 0 if a==b, -1 if a<b
    '''
    for idx in range(1,len(a)):
        if a[idx][2] == STRING_NONE:
            if a[idx][1] == STRING_NUMBERS or a[idx][1] == STRING_TEXT:
                cmp = cmp_simple(a[idx][0], b[idx][0], a[idx][3])
                if cmp != 0:
                    return cmp
    return 0


def sort_fields(keyed):
    '''
          Name: sort_fields
         Usage: ordered = sort_fields(keyed)
       Purpose: Do the sort.
    Parameters: keyed   -- ((marked,(field,sort_as,type,wants_descending)),...)
       Returns: ordered -- sorted marked lines
    '''

    ordered = sorted(keyed, key=functools.cmp_to_key(cmp_fields))
    return ordered


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


def main():
    '''
          Name: main
         Usage: main()
       Purpose: Isolates execution of the program from importing.
    Parameters: (none)
       Returns: (none)
    '''
    text,     marked          = get_text()
    frontage, newline, ending = get_newline(marked)        # also preserves trailing blank lines
    count,    fields          = get_fields(text, marked)   # fields also contain unmarked & marked lines
    status,   sortkeys        = query_sortkeys(count, fields)
    if status != 0:   # user cancelled sort
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

