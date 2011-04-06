##
##Copyright (C) 2008 Henry Zhou <jiangwen365@gmail.com>
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


import pyodbc

from decimal import Decimal
from Shared.DC.ZRDB.TM import TM
import string, sys
from DateTime import DateTime
from string import strip, split, find,replace
from types import *

DB_Error = pyodbc.Error

class DB(TM):
        """DB class from pyodbc driver"""

        def __init__(self,po_conx):
                conn_param = eval(po_conx)
                self._conxString = conn_param['connx_string']
                self._auto_commit = conn_param['auto_commit']
                self._MaxRows = conn_param['MaxRows']
                
                self._conx = pyodbc.connect(self._conxString, autocommit = self._auto_commit)
                self._cursor = self._conx.cursor
                self._numTry = 0
                self._numMaxTry = 5
        
        def setAutocommit(self, auto_commit=None):
                self._auto_commit = auto_commit
                

        def setMaxRows(self,MaxRows):
                try:
                        self._MaxRows = int(MaxRows)
                except ValueError,mesg:
                        raise mesg
                
        def connect(self,ps_queryString):
                from time import sleep
                while (self._numTry < self._numMaxTry):
                        self._numTry = self._numTry + 1
                        try:
                                self._conx = pyodbc.connect(self._conxString,self._auto_commit)
                                self._cursor = self._conx.cursor
                                return self.query(ps_queryString)
                        except pyodbc.OperationalError, mesg:
                                sleep(5)
                self._numTry = 0
                raise mesg
                                
        def close(self):
                pass
                
                
        def query(self,ps_queryString, pl_maxRows=None):                        
                self._register()
                #ps_queryString = replace(ps_queryString,"\n"," ")  #This seems not necessary and sometimes breaks certain SQLs.
                
                o_cur = self._cursor()          
                try:
                        o_ret = o_cur.execute(ps_queryString)
                except: #Occaionally the connection is lost which I havn't figure out why, but this re-connecting works for me very well. Need to imporve though!
                        o_cur.close()
                        self._conx.close()
                        self._conx = pyodbc.connect(self._conxString, autocommit = self._auto_commit)
                        self._cursor = self._conx.cursor
                        o_cur = self._cursor()
                        o_ret = o_cur.execute(ps_queryString)                           
                o_desc = o_cur.description                      
                                        
                if o_desc is None:
                        o_cur.close()
                        return (),()

                o_items = map(lambda x:{'name':x[0],'type':x[1],'dsize':x[2],'isize':x[3],'precision':x[4],'scale':x[5],'null':x[6]}, o_desc)
                field_types = [i['type'] for i in o_items]
                
                # get date field ids to be convert to DateTime type
                date_field_ids = [i for i in range(len(field_types)) if field_types[i] in (datetime.datetime, datetime.date)]
                #get float field ids to be convert from decimal to float
                float_field_ids = [i for i in range(len(field_types)) if field_types[i] in (float,)]     
                
                if pl_maxRows == None:
                        o_result = o_cur.fetchmany(self._MaxRows)
                else:
                        o_result = o_cur.fetchmany(pl_maxRows)
                
                o_cur.close()

                
                # if any pyodbc's object type needs to be converted to Zope's object type.
                if len(date_field_ids)+len(float_field_ids) > 0:
                    for row in o_result:
                            for field_id in date_field_ids:
                                    if row[field_id] != None:
                                            # Currently we don't do timezones. Everything is UTC.
                                            # Ideally we'd get the current Oracle timezone and use that.
                                            row[field_id] = DateTime(*(row[field_id].timetuple()[:6] + ('UTC',)))
                            for field_id in float_field_ids:
                                    if row[field_id] != None:
                                            row[field_id] = float(row[field_id])                    
                        
                return o_items,o_result
                
                                
        def _datetime_convert(self, dt, val):
                if dt and (val!=None):
                        # Currently we don't do timezones. Everything is UTC.
                        # Ideally we'd get the current Oracle timezone and use that.
                        x = val.timetuple()[:6] + ('UTC',)
                        return DateTime(*x) 
                return val
                
        def _Decimal_convert(self, dt, val):
                if dt and (val!=None):
                        return float(val)
                return val
                
        
        def getdbinfo (self):
                dbinfo = ''
                try:
                        dbinfo += self._conx.getinfo(pyodbc.SQL_DBMS_NAME) + ' '
                        dbinfo += self._conx.getinfo(pyodbc.SQL_DBMS_VER) + ' '
                        dbinfo += self._conx.getinfo(pyodbc.SQL_DATABASE_NAME) + ' '
                except:
                        pass
                return dbinfo
                
        def get_columns (self, table_name):
                o_cur = self._cursor()
                columns = [column for column in o_cur.columns(table_name)]
                o_cur.close()
                return columns
                
        def get_tables (self):
                o_cur = self._cursor()
                tables = [table for table in o_cur.tables()]
                o_cur.close()
                return tables           
                
                (tablename)
                        
        def get_primaryKeys (self, table_name):
                o_cur = self._cursor()
                primaryKeys = []
                try:
                        primaryKeys = [p_key for p_key in o_cur.primaryKeys(table_name)]
                except:
                        pass
                o_cur.close()
                return primaryKeys              
                        
        def get_foreignKeys (self, table_name):
                o_cur = self._cursor()
                foreignKeys = []
                try:
                        foreignKeys = [f_key for f_key in o_cur.foreignKeys(foreignTable=table_name)]
                except:
                        pass
                o_cur.close()
                return foreignKeys      
                        
                        
        def _finish (self):
                try:
                        self._conx.commit()
                        pass
                except (DB_Error), s_mesg:
                        raise sys.exc_type, sys.exc_value, sys.exc_traceback
                

        def _abort (self):
                try:
                        self._conx.rollback()
                except (DB_Error),s_mesg:
                        raise sys.exc_type, sys.exc_value, sys.exc_traceback
                
        def _begin (self):
                pass
