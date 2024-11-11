#!/bin/env python3
'''
     Title: 01test
 Copyright: Copyright 2023 by Shawn H Corey. Some rights reserved.
   Purpose: Test the Field Sort for the Zinm Desktop Wiki.

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
'''

import subprocess
import os
import re

cwd = os.path.dirname(os.path.realpath(__file__))
field_sort = cwd + "/../field_sort.py"

marked = """zero       0
ten        10
empty
minus one  -1
PI         3.14159265358979
big number 1e10
e          2.71828182845905"""

print('pre-sort')
print(marked)
print('sorted')

lines = re.sub('__', '', marked)
status = subprocess.call([field_sort, marked, lines])

print('')
if status == 0:
    print("sort initiated")
else:
    print(f"sort cancelled: {status}")
