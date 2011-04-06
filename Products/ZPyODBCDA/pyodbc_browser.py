##
##Copyright (C) 2007 Henry Zhou <jiangwen365@gmail.com>
## Copyright (C) 2001 Thierry MICHEL <thierry@nekhem.com>
##  
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##  
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##  
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##  
##
## Here are requests to have informations about tables.


from pyodbc_DA import pyodbcConnection, database_type, addpyodbcConnectionForm
from string import find,split
from pyodbc_DA import DTMLFile

def addpyodbcConnectionBrowser(self, id, title, connection_string, auto_commit=None, connected=None, MaxRows=10, REQUEST=None):
    """Add a Z PyODBC DB connection to a folder"""
        
    if not auto_commit is None:
        auto_commit = 1        
    if not connected is None:
        connected = 1
    self._setObject(id, pyodbcConnectionBrowser(id,
                                   title,
                                   connection_string,
                                   auto_commit,
                                   connected,
                                   MaxRows))
    if REQUEST is not None:
        return self.manage_main(self,REQUEST)

class pyodbcConnectionBrowser(pyodbcConnection):
    """pyodbc Connection with tables browser feature"""

    
    manage_options=pyodbcConnection.manage_options+(
        {'label':'Browser','action':'manage_browser'},
        )

    manage_browser = DTMLFile('dtml/pyodbcconnectionBrowser',globals())

    def __is_foreign_key(self,description):
        res=1
        if find(description,'FOREIGN') == -1:
            res=0
        return res

    def __get_source_table(self,arguments):
        res=''
        res= split(arguments,'\\000')[2]

        return res

    def __get_source_field(self,arguments):
        res= split(arguments,'\\000')[4]
        return res

    def __set_table_fkeys(self,tablename):
        if self._v_connected:
            records = self._v_database_connection.get_foreignKeys(tablename)
        self.fkeys = []
        for r in records:
            self.fkeys.append(((r[6],r[7]),r[2]))#(source table, source column)
                

    def __set_table_pkeys(self,tablename):
        if self._v_connected:
            records = self._v_database_connection.get_primaryKeys(tablename)
        self.pkeys = []
        for r in records:
            self.pkeys.append((r[2],r[3]))

    def is_primary_key(self,tablename,field):
        if (tablename,field) in self.pkeys:
            return 1
        return 0
    
    def is_foreign_key(self,tablename,field):
        for fkey in self.fkeys:
            if (tablename,field) == fkey[0]:
                return fkey[1]
        return 0

    def manage_get_table_infos(self,tablename):
        " "
        if self._v_connected:
            column_infos = self._v_database_connection.get_columns(tablename)
            self.__set_table_pkeys(tablename)
            self.__set_table_fkeys(tablename)
        else:
            return []
        
        result = []
        i = 1
        for info in column_infos:
            rsp = {}
            rsp['attnum'] = i
            rsp['attname'] = info[3]
            rsp['typname'] = info[5]
            rsp['attnotnull'] = info[10]
            rsp['attlen'] = info[6]
            result.append(rsp)
            i = i + 1
        return result

    def manage_get_tables (self):
        " "
        if self._v_connected:
            r = self._v_database_connection.get_tables()
        else:
            return []

        result = []
        for item in r:
            rsp = {}
            rsp['tablename'] = item[2]
            rsp['tabletype'] = item[3]
            result.append(rsp)

        return result

    
