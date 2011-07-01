#!/usr/bin/env python
"""
This module provides business object class to interact with datatiers table. 
"""
from WMCore.DAOFactory import DAOFactory
from dbs.utils.dbsExceptionHandler import dbsExceptionHandler
from dbs.utils.dbsException import dbsException,dbsExceptionCode

class DBSDataTier:
    """
    DataTier business object class
    """
    def __init__(self, logger, dbi, owner):
	daofactory = DAOFactory(package='dbs.dao', logger=logger, dbinterface=dbi, owner=owner)
	self.logger = logger
	self.dbi = dbi
	self.owner = owner

	self.sm = daofactory(classname="SequenceManager")
	self.dataTier = daofactory(classname="DataTier.List")
	self.dtin = daofactory(classname="DataTier.Insert")

    def listDataTiers(self, data_tier_name=""):
	"""
	List data tier(s)
	"""
        if type(data_tier_name) is not str:
            dbsExceptionHandler('dbsException-invalid-input', 'data_tier_name given is not valid : %s' %data_tier_name)
	try:
	    conn = self.dbi.connection()
	    result = self.dataTier.execute(conn, data_tier_name.upper())
	    return result
	except Exception, ex:
	    raise ex
	finally:
	    conn.close()

    def insertDataTier(self, businput):
        """
        Input dictionary has to have the following keys:
        data_tier_name, creation_date, create_by
        it builds the correct dictionary for dao input and executes the dao
        """
	conn = self.dbi.connection()
        tran = conn.begin()
        try:
	    businput["data_tier_id"] = self.sm.increment(conn, "SEQ_DT", tran)
            businput["data_tier_name"] = businput["data_tier_name"].upper()
            self.dtin.execute(conn, businput, tran)
            tran.commit()
        except KeyError, ke:
            dbsExceptionHandler('dbsException-invalid-input', "Invalid input:"+ke.args[0])
        except Exception, ex:
            if str(ex).lower().find("unique constraint") != -1 or str(ex).lower().find("duplicate") != -1:
                # already exist
                self.logger.warning("Unique constraint violation being ignored...")
                self.logger.warning("%s" % ex)
                pass
            else:
                tran.rollback()
                raise
        finally:
            conn.close()

