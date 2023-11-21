
# Field Sort — A Zim Desktop Wiki Tool

Sort lines by marked fields.


## Description

Field Sort is a custom tool for the [Zim Desktop Wiki](https://zim-wiki.org/).


## Requirements

*   zim     -- Zim Desktop Wiki. <https://zim-wiki.org/>
*   python3 -- version 3.8 or later. <https://www.python.org/>
*   GTK3    -- version 3 or later. <https://www.gtk.org/>


## Installation

Download `field-sort.py`.

Open Zim and from the menu, select `Tools -> Custom Tools`.
Press the `+` button at the top of the right column to add a new tool.
Fill in the following:

    Name: Field Sort
    Description: Sort lines by marked fields.
    Command: **/field_sort.py %T %t

Replace the double asterisks with the path to `field_sort.py`.

Check `Output should replace current selection`
and `Show in the toolbar`.

Press `OK`, then `Close`.
Field Sort should appear in the menu Toolbar just above the Custom Tool item.


## Usage

Mark the fields in the lines to be sorted.
Selection the text for each field and mark it via the menu `Format -> Mark` or pres `Ctrl+U`.
You may have more than one field per line.

Select all the lines to be sorted.
May sure you get the entire lines.
If the lines are a bullet list or a numbered list, be sure to include the bullet or number in the first line.

Run the Field Sort by the menu `Tools -> Field Sort`.
A dialog will appear allowing you to choose:

*   the order the fields will be sorted,
*   how they will be sorted as,
*   the locale to apply to the sort,
*   and the order of the sort, that is, ascending or descending.

There is also an option to sort by the entire lines after all the fields sorting is done.

Press `OK` and the selection should be replaced with the sorted lines on the Zim page.


## Copyright and Licences

Copyright 2023 by Shawn H Corey. Some rights reserved.
See `LICENCE.md` for details.


### Software Licence

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

