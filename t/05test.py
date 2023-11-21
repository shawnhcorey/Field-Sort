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

Kai, __Cashier__
Olivia, __Food preparation worker__
Liam, __Janitor__
Amelia, __Bartender__
Noah, __Server__
Rowan, __Retail sales associate__
Mia, __Stocking associate__
Unique, __Labourer__
Eliana, __Customer service representative__
Apollo, __Office clerk__
Mila, __Administrative assistant__
Ezra, __Line supervisor__
Luca, __Medical assistant__
Maeve, __Construction worker__
Aria, __Bookkeeper__
Evelyn, __Mechanic__
Charlotte, __Carpenter__
Nova, __Electrician__
Ava, __Registered nurse__
Asher, __Marketing specialist__

"""

lines = re.sub('__', '', marked)

status = subprocess.call([field_sort, marked, lines])
print("\n")
if status == 0:
    print("sort initiated")
else:
    print(f"sort cancelled: {status}")
