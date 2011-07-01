#!/usr/bin/env python
"""
This module provides business object class to interact with DBSAcqusitionEra. 
"""

__revision__ = "$Id: DBSAcquisitionEra.py,v 1.6 2010/08/12 19:52:24 afaq Exp $"
__version__ = "$Revision $"

from WMCore.DAOFactory import DAOFactory
from dbs.utils.dbsExceptionHandler import dbsExceptionHandler
from dbs.utils.dbsException import dbsException,dbsExceptionCode

class DBSAcquisitionEra:
    """
    DBSAcqusition Era business object class
    """
    def __init__(self, logger, dbi, owner):
        daofactory = DAOFactory(package='dbs.dao', logger=logger, dbinterface=dbi, owner=owner)
        self.logger = logger
        self.dbi = dbi
        self.owner = owner

        self.acqin = daofactory(classname="AcquisitionEra.Insert")
        self.acqlst = daofactory(classname="AcquisitionEra.List")
        self.sm = daofactory(classname="SequenceManager")

    def listAcquisitionEras(self, acq=''):
        """
        Returns all acquistion eras in dbs
        """
        if type(acq) is not str:
            dbsExceptionHandler('dbsException-invalid-input', 'Acquistion era name given is not valid : %s' %acq)
        try:
            conn=self.dbi.connection()
            result= self.acqlst.execute(conn,acq)
            return result
        except Exception, ex:
            raise ex
        finally:
            if conn: conn.close()

    def insertAcquisitionEra(self, businput):
        """
        Input dictionary has to have the following keys:
        acquisition_era_name, creation_date, create_by
        it builds the correct dictionary for dao input and executes the dao
        """
	conn = self.dbi.connection()
        tran = conn.begin()
        try:
	    businput["acquisition_era_id"] = self.sm.increment(conn, "SEQ_AQE", tran)
            businput["acquisition_era_name"] = businput["acquisition_era_name"].upper()
            self.acqin.execute(conn, businput, tran)
            tran.commit()
        except KeyError, ke:
            dbsExceptionHandler('dbsException-invalid-input', "Invalid input:"+ke.args[0])
        except Exception, ex:
            if str(ex).lower().find("unique constraint") != -1 or str(ex).lower().find("duplicate") != -1:
                # already exists
                self.logger.warning("DBSAcquisitionEra/insertAcquisitionEra: Unique constraint violation being ignored...")
                self.logger.warning("%s" % ex)
                pass
            else:
                tran.rollback()
                raise
        finally:
            conn.close()
