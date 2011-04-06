.. contents:: Table of Contents
   :depth: 2

Products.ZPyODBCDA
****************************************

Overview
--------

ZPyODBCDA is a Zope Database Adapter based on Python's pyodbc moudle 
(http://pyodbc.sourceforge.net). It links the Zope server to ODBC data sources. 
It is distributed under the GPL licence.

The reason I wrote a new Zope ODBC Database Adapter and didn't simply use the
existing "New ZODBC DA" on zope.org is that I felt the underlying Pywin32's 
ODBC module which the "New ZODBC DA" depended on was not stable enough, 
and occasionally crashed my Python programs.

The mxODBCDA is a commercial product which is not free.

The Products.ZPyODBCDA product is modified from the codes of Thierry MICHEL's 
GPL licensed ZPoPyDA product, which links Zope to PostgreSQL and seems to be 
very mature.

Products.ZPyODBCDA requires Python 2.4 or higher.

If your Zope runs on the win32 platform, you probably don't need any other moudules, as I already included pyodbc's binary code (pyodbc.pyd) in the package folder; for other platform like Linux, you may first need to install the pyodbc moudule for your Python instance.

I hope this product can provide a more reliable free Zope/ODBC connec solution to you.


Requirements
------------

    * Pyodbc (http://code.google.com/p/pyodbc/)
    
    * Zope 2.12
    
    * Plone 4 (optional)
    
Installation
------------
    
To enable this product,on a buildout based installation:

    1. Edit your buildout.cfg and add ``Products.ZPyODBCDA``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            Products.ZPyODBCDA
    
After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product (check its checkbox) and click the 'Install' button.

Uninstall -- This can be done from the same management screen, but only
if you installed it from the quick installer.

Note: You may have to empty your browser cache and save your resource registries
in order to see the effects of the product installation.

Sponsoring
----------

Adaptation of this product was sponsored by 
`TRT13 <http://www.trt13.jus.br/>`_ and implemented by 
`Simples Consultoria <http://www.simplesconsultoria.com.br/>`_.


Credits
-------
    
    * Henry Zhou (Jiangwen365 at gmail dot com) - Coding
    * Simples Consultoria (products at simplesconsultoria dot com dot br) - 
      Egg implementation
    





