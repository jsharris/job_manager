__author__ = 'jon'

import psycopg2
import logging
from datetime import datetime


log = logging.getLogger()


#
# Class for presenting a simple interface for manipulating postgres
#
class DBConnect(object):
    def __init__(self, env, server=None, db=None, dbuser=None, passwd=None):
        # need the db parameters from the config
        if server is None:
            self.server = env.getSetting('dbhost')
        else:
            self.server = server

        if db is None:
            self.db = env.getSetting('database')
        else:
            self.db = db

        if dbuser is None:
            self.dbuser = env.getSetting('dbuser')
        else:
            self.dbuser = dbuser

        if passwd is None:
            self.passwd = env.getSetting('password')
        else:
            self.passwd = passwd

        self.conn = psycopg2.connect(host=self.server, database=self.db, user=self.dbuser, password=self.passwd)

    def close(self):
        self.conn.close()

    def new_job(self, email, job_type, notify):
        if self.conn:
            cur = self.conn.cursor()
            dt = datetime.now()
            status = self._get_status_code('Queued')
            job_type = self._get_job_code(job_type)
            if job_type == 0:
                return {'status': 'Failure', 'message': 'Invalid job_type specified'}
            query = "insert into jobs " \
                    "(id, job_type_id, email, submitted, last_updated, status_id, percentage, notify) " \
                    "values (DEFAULT, %s, %s, %s, %s, %s, %s, %s) returning id"
            data = (job_type, email, dt, dt, status, 0, notify)
            try:
                cur.execute(query, data)
                job_id = cur.fetchone()[0]
                status = {'status': 'Success', 'data': {'job_id': job_id}}
            except:
                log.error("Failed trying to create a job")
                status = {'status': 'Failure', 'message': 'Unable to create the job'}
            self.conn.commit()
            cur.close()
        else:
            log.error("new_job: No database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def update_job(self, job_id, percentage, message):
        if self.conn:
            cur = self.conn.cursor()
            dt = datetime.now()
            status = self._get_status_code('Active')
            query = "update jobs set percentage=%s, status_id=%s, last_updated=%s, message=%s where id=%s"
            data = (percentage, status, dt, message, job_id)
            try:
                cur.execute(query, data)
                if cur.rowcount > 0:
                    status = {'status': 'Success'}
                else:
                    status = {'status': 'Failure', 'message': 'Unable to update database - bad job id?'}
            except:
                status = {'status': 'Failure', 'message': 'Unable to update the job'}
            self.conn.commit()
            cur.close()
        else:
            log.error("update_job: No database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def complete_job(self, job_id, message):
        if self.conn:
            cur = self.conn.cursor()
            dt = datetime.now()
            status = self._get_status_code('Completed')
            query = "update jobs set percentage=100, status_id=%s, last_updated=%s, message=%s where id=%s"
            data = (status, dt, message, job_id)
            try:
                cur.execute(query, data)
                if cur.rowcount > 0:
                    status = {'status': 'Success'}
                else:
                    status = {'status': 'Failure', 'message': 'Unable to update database - bad job id?'}
            except:
                status = {'status': 'Failure', 'message': 'Unable to update the job'}
            self.conn.commit()
            cur.close()
        else:
            log.error("completed_job: No database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def error_job(self, job_id, message):
        if self.conn:
            cur = self.conn.cursor()
            dt = datetime.now()
            status = self._get_status_code('Error')
            query = "update jobs set percentage=100, status_id=%s, last_updated=%s, message=%s where id=%s"
            data = (status, dt, message, job_id)
            try:
                cur.execute(query, data)
                if cur.rowcount > 0:
                    status = {'status': 'Success'}
                else:
                    status = {'status': 'Failure', 'message': 'Unable to update database - bad job id?'}
            except:
                status = {'status': 'Failure', 'message': 'Unable to update the job'}
            self.conn.commit()
            cur.close()
        else:
            log.error("error_job: No database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def delete_job(self, job_id, message):
        if self.conn:
            cur = self.conn.cursor()
            dt = datetime.now()
            status = self._get_status_code('Deleted')
            query = "update jobs set percentage=100, status_id=%s, last_updated=%s, message=%s where id=%s"
            data = (status, dt, message, job_id)
            try:
                cur.execute(query, data)
                if cur.rowcount > 0:
                    status = {'status': 'Success'}
                else:
                    status = {'status': 'Failure', 'message': 'Unable to update database - bad job id?'}
            except:
                status = {'status': 'Failure', 'message': 'Unable to update the job'}
            self.conn.commit()
            cur.close()
        else:
            log.error("delete_job: No database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def purge_job(self, job_id):
        if self.conn:
            cur = self.conn.cursor()
            query = "delete from jobs where id=%s"
            data = (job_id, )
            try:
                cur.execute(query, data)
                if cur.rowcount > 0:
                    status = {'status': 'Success'}
                else:
                    status = {'status': 'Failure', 'message': 'Unable to update database - bad job id?'}
            except:
                status = {'status': 'Failure', 'message': 'Unable to purge the job'}
            self.conn.commit()
            cur.close()
        else:
            log.error("purge_job: No database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def status_job_by_id(self, job_ids):
        list_of_results = []
        if self.conn:
            for job_id in job_ids:
                good_id = True
                if type(job_id) is not int:
                    try:
                        job_id = int(job_id)
                    except:
                        good_id = False
                if good_id:
                    cur = self.conn.cursor()
                    query = "select * from jobs where id=%s"
                    data = (job_id, )
                    cur.execute(query, data)
                    results = cur.fetchone()
                    if results is not None:
                        list_of_results.append(self._results_to_dict(results))
                    self.conn.commit()
                    cur.close()
            if len(list_of_results) > 0:
                status = {'status': 'Success', 'data': list_of_results}
            else:
                status = {'status': 'Failure', 'message': 'Unable to find job(s)'}
        else:
            log.error("status_job: No database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def status_job_by_email(self, email):
        list_of_results = []
        if self.conn:
            cur = self.conn.cursor()
            query = "select * from jobs where email=%s order by id"
            data = (email, )
            cur.execute(query, data)
            jobs = cur.fetchall()
            for results in jobs:
                list_of_results.append(self._results_to_dict(results))
            if len(list_of_results) > 0:
                status = {'status': 'Success', 'data': list_of_results}
            else:
                status = {'status': 'Failure', 'message': 'Unable to find job(s)'}
            self.conn.commit()
            cur.close()
        else:
            log.error("status_job: No database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def status_job_all(self):
        list_of_results = []
        if self.conn:
            cur = self.conn.cursor()
            query = "select * from jobs order by id"
            cur.execute(query)
            jobs = cur.fetchall()
            for results in jobs:
                list_of_results.append(self._results_to_dict(results))
            if len(list_of_results) > 0:
                status = {'status': 'Success', 'data': list_of_results}
            else:
                status = {'status': 'Failure', 'message': 'Unable to find jobs(s)'}
            self.conn.commit()
            cur.close()
        else:
            log.error("status_job_all: No Database connection")
            status = {'status': 'Failure', 'message': 'Not able to connect to database'}
        return status

    def flip_job_notify(self, job_id, notify):
        print "notify: job: %s, notify: %s" % (job_id, notify)
        if self.conn:
            cur = self.conn.cursor()
            query = "update jobs set notify=%s where id=%s"
            data = (notify, job_id)
            try:
                cur.execute(query, data)
                if cur.rowcount != 1:
                    status = {'status': 'Failure', 'message': 'Unable to update notify field'}
                else:
                    status = {'status': 'Success'}
            except:
                status = {'status': 'Failure', 'message': 'Unable to update database'}
            self.conn.commit()
            cur.close()
        else:
            log.error("flip_job_notify: No database connection")
            status = {'status': 'Failure', 'message': 'No database connection'}
        return status


    def _results_to_dict(self, results):
        ret_val = dict()
        ret_val['id'] = results[0]
        ret_val['job_type'] = self._get_job_desc(results[1])
        ret_val['email'] = results[2]
        ret_val['submitted'] = results[3].strftime("%m/%d/%Y %H:%M")
        ret_val['last_updated'] = results[4].strftime("%m/%d/%Y %H:%M")
        ret_val['status'] = self._get_status_desc(results[5])
        ret_val['percentage'] = results[6]
        ret_val['notify'] = results[7]
        ret_val['message'] = results[8]
        return ret_val

    def _get_status_code(self, description):
        if self.conn:
            cur = self.conn.cursor()
            query = "select id from status where description=%s"
            data = (description, )
            cur.execute(query, data)
            code = cur.fetchone()
            if code is None:
                return 0
            return code[0]

    def _get_status_desc(self, sid):
        if self.conn:
            cur = self.conn.cursor()
            query = "select description from status where id=%s"
            data = (sid, )
            cur.execute(query, data)
            desc = cur.fetchone()
            if desc is None:
                return 0
            return desc[0]

    def _get_job_code(self, description):
        if self.conn:
            cur = self.conn.cursor()
            query = "select id from job_type where description=%s"
            data = (description, )
            cur.execute(query, data)
            code = cur.fetchone()
            if code is None:
                return 0
            return code[0]

    def _get_job_desc(self, jid):
        if self.conn:
            cur = self.conn.cursor()
            query = "select description from job_type where id=%s"
            data = (jid, )
            cur.execute(query, data)
            desc = cur.fetchone()
            if desc is None:
                return 0
            return desc[0]

