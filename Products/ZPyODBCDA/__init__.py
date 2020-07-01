#
# Copyright (C) 2007 Henry Zhou <jiangwen365@gmail.com>
# Copyright (C) 2001 Thierry MICHEL <thierry@nekhem.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#

"""Z PyODBC Database Adapter Package Registration"""

import sys
import traceback

from .pyodbc_browser import pyodbcConnectionBrowser
from .pyodbc_browser import addpyodbcConnectionBrowser
from .pyodbc_browser import addpyodbcConnectionForm


def initialize(context):
    "Initialize the product."
    try:
        context.registerClass(
            pyodbcConnectionBrowser,
            constructors=(
                addpyodbcConnectionForm,
                addpyodbcConnectionBrowser
            ),
            icon='www/pyodbc_icon.png'
        )
    except Exception:
        type, val, tb = sys.exc_info()
        sys.stderr.write(
            traceback.format_exception(
                type, val, tb
            ).join('')
        )
        del type, val, tb
