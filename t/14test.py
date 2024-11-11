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

marked = """
__A__ __B__ __C__ __D__ __E__ __F__ __G__ __H__ __I__ __J__ __K__ __L__ __M__ __N__ __O__ __P__ __Q__ __R__ __S__ __T__ __U__ __V__ __W__ __X__ __Y__ __Z__ __a__ __b__ __c__ __d__ __e__ __f__ __g__ __h__ __i__ __j__ __k__ __l__ __m__ __n__ __o__ __p__ __q__ __r__ __s__ __t__ __u__ __v__ __w__ __x__ __y__ __z__
"""

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
