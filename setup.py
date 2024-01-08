# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = open(os.path.join(
    "Products", "ZPyODBCDA", "version.txt")).read().strip()

setup(
    name='Products.ZPyODBCDA',
    version=version,
    description="ODBC DA for Zope",
    long_description=(
        open(os.path.join("Products", "ZPyODBCDA", "README.txt")).read() +
        "\n" +
        open(os.path.join("docs", "HISTORY.txt")).read()
    ),
    # Get more strings from
    # https://pypi.org/classifiers
    classifiers=[
        "Framework :: Zope",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='odbc database pyodbc zope zopeda',
    author='Simples Consultoria',
    author_email='products@simplesconsultoria.com.br',
    url='https://bitbucket.org/simplesconsultoria/products.zpyodbcda/',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pyodbc',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
