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


from Shared.DC.ZRDB.Connection import DTMLFile, Connection
from .pyodbc_db import DB

database_type = 'PyODBC'

"""%s Database Connection""" % database_type


addpyodbcConnectionForm = DTMLFile(
    'dtml/pyodbcconnectionAdd',
    globals(),
    default_id='%s_database_connection' % database_type,
    default_title='Z %s Database Connection' % database_type,
    database_type=database_type,
)


def addpyodbcConnection(self, id, title, connection_string, auto_commit=None,
                        connected=None, MaxRows=10, REQUEST=None):
    """Add a Z PyODBC DB connection to a folder"""

    if connected is not None:
        connected = 1
    self._setObject(id, pyodbcConnection(id,
                                         title,
                                         connection_string,
                                         auto_commit,
                                         connected,
                                         MaxRows))
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)


class pyodbcConnection(Connection):
    """A database connection object"""
    database_type = database_type
    id = '%s_database_connection' % database_type
    meta_type = title = 'Z %s Database Connection' % database_type
    icon = 'misc_/Z%sDA/conn' % database_type
    _isAnSQLConnection = 1

    def __init__(self, id, title, connection_string, auto_commit=None,
                 connected=None, MaxRows=10):
        self.connx_string = connection_string
        self.MaxRows = MaxRows
        if auto_commit is not None:
            self.auto_commit = True
        else:
            self.auto_commit = False

        conn_param = {}
        conn_param['connx_string'] = self.connx_string
        conn_param['auto_commit'] = self.auto_commit
        conn_param['MaxRows'] = self.MaxRows

        Connection.__init__(self, id, title, repr(conn_param), connected)

    def get_backend_info(self):
        if self._v_connected:
            return self._v_database_connection.getdbinfo()
        return ''

    def manage_MaxRows(self, MaxRows, REQUEST):
        " "
        self.MaxRows = MaxRows
        self._v_database_connection.setMaxRows(MaxRows)
        return self.manage_main(self, REQUEST)

    manage_main = DTMLFile('dtml/pyodbcconnectionStatus', globals())

    manage_properties = DTMLFile('dtml/pyodbcconnectionEdit', globals())

    def manage_edit(self, title, connection_string, auto_commit=None,
                    connected=None, MaxRows=10, REQUEST=None):
        """Change connection"""
        self.connx_string = connection_string
        self.MaxRows = MaxRows
        if auto_commit is not None:
            self.auto_commit = True
        else:
            self.auto_commit = False

        conn_param = {}
        conn_param['connx_string'] = self.connx_string
        conn_param['auto_commit'] = self.auto_commit
        conn_param['MaxRows'] = self.MaxRows
        Connection.manage_edit(self, title, repr(
            conn_param), connected, REQUEST)

    def factory(self):
        return DB
