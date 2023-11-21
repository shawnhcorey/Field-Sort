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

Kai, Cashier
Olivia, Food preparation worker
Liam, Janitor
Amelia, Bartender
Noah, Server
Rowan, Retail sales associate
Mia, Stocking associate
Unique, Labourer
Eliana, Customer service representative
Apollo, Office clerk
Mila, Administrative assistant
Ezra, Line supervisor
Luca, Medical assistant
Maeve, Construction worker
Aria, Bookkeeper
Evelyn, Mechanic
Charlotte, Carpenter
Nova, Electrician
Ava, Registered nurse
Asher, Marketing specialist
"""

lines = re.sub('__', '', marked)

status = subprocess.call([field_sort, marked, lines])
print("\n")
if status == 0:
    print("sort initiated")
else:
    print(f"sort cancelled: {status}")
