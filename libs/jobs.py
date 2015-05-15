__author__ = 'jon'

from database import *
from environment import *
from helpers import email
import logging

log = logging.getLogger()


class Jobs(object):
    def __init__(self):
        pass

    def new(self, ini_file, job_type, email, notify):
        env = Environment(ini_file)
        db = DBConnect(env)
        status = db.new_job(email, job_type, notify)
        db.close()
        return status

    def update(self, ini_file, job_id, percentage, msg=None):
        env = Environment(ini_file)
        db = DBConnect(env)
        status = db.update_job(job_id, percentage, msg)
        db.close()
        return status

    def completed(self, ini_file, job_id, msg=None):
        env = Environment(ini_file)
        db = DBConnect(env)
        status = db.complete_job(job_id, msg)
        if status['status'] == 'Success':
            status = db.status_job_by_id([job_id])
            if status['data'][0]['notify']:
                status = email(ini_file, self, job_id)
        db.close()
        return status

    def error(self, ini_file, job_id, msg=None):
        env = Environment(ini_file)
        db = DBConnect(env)
        status = db.error_job(job_id, msg)
        if status['status'] == 'Success':
            status = db.status_job_by_id([job_id])
            if status['data'][0]['notify']:
                status = email(ini_file, self, job_id)
        db.close()
        return status

    def delete(self, ini_file, job_id, msg=None):
        env = Environment(ini_file)
        db = DBConnect(env)
        status = db.delete_job(job_id, msg)
        db.close()
        return status

    def purge(self, ini_file, job_id, auth_key):
        env = Environment(ini_file)
        if auth_key != env.getSetting('auth_key'):
            return {'status': 'Failure', 'message': 'Invalid auth_key provided'}
        db = DBConnect(env)
        status = db.purge_job(job_id)
        db.close()
        return status

    def status(self, ini_file, jtype=None, data=None):
        env = Environment(ini_file)
        db = DBConnect(env)
        if jtype == 'id':
            status = db.status_job_by_id([data])
        elif jtype == 'email':
            status = db.status_job_by_email(data)
        elif jtype == 'all':
            status = db.status_job_all()
        else:
            log.error('Status got a bad jtype "%s" passed in' % jtype)
            status = {'status': 'Failure', 'message': 'Bad job_type "%s" specified' % type}
        db.close()
        return status

    def flip_notify(self, ini_file, job_id, notify):
        if notify == 'True' or notify == 'False':
            env = Environment(ini_file)
            db = DBConnect(env)
            status = db.flip_job_notify(job_id, notify)
            db.close()
        else:
            status = {'status': 'Failure', 'message': 'Invalid value'}
        return status