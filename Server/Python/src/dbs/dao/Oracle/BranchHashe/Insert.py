#!/usr/bin/env python
""" DAO Object for BranchHashes table """ 
from WMCore.Database.DBFormatter import DBFormatter
from dbs.utils.dbsExceptionHandler import dbsExceptionHandler

class Insert(DBFormatter):

    def __init__(self, logger, dbi):
            DBFormatter.__init__(self, logger, dbi)
	    self.owner = "%s." % owner if not owner in ("", "__MYSQL__") else ""
           
            self.sql = """INSERT INTO %sBRANCH_HASHES ( BRANCH_HASH_ID, HASH, CONTENT) VALUES (:branch_hash_id, :branch_hash, :content)""" % (self.owner)

    def execute( self, conn, binds, transaction=False ):
        if not conn:
	    dbsExceptionHandler("dbsException-db-conn-failed","Oracle/BranchHashe/Insert. Expects db connection from upper layer.")
	
	result = self.dbi.processData(self.sql, binds, conn, transaction)
	return


