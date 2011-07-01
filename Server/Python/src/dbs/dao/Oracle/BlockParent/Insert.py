#!/usr/bin/env python
""" DAO Object for BlockParents table """ 

__revision__ = "$Revision: 1.6 $"
__version__  = "$Id: Insert.py,v 1.6 2010/06/23 21:21:18 afaq Exp $ "

from WMCore.Database.DBFormatter import DBFormatter
from dbs.utils.dbsExceptionHandler import dbsExceptionHandler

class Insert(DBFormatter):

    def __init__(self, logger, dbi, owner):
        DBFormatter.__init__(self, logger, dbi)
        self.owner = "%s." % owner if not owner in ("", "__MYSQL__") else ""
        self.logger = logger

        self.sql = """INSERT INTO %sBLOCK_PARENTS (THIS_BLOCK_ID, PARENT_BLOCK_ID) 
                          VALUES (:this_block_id, :parent_block_id)""" % (self.owner)

    def execute( self, conn, binds, transaction=False ):
        if not conn:
	    dbsExceptionHandler("dbsException-db-conn-failed","Oracle/BlockParent/Insert. Expects db connection from upper layer.")
            
	result = self.dbi.processData(self.sql, binds, conn, transaction)

