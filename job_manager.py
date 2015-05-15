from flask import Flask, request, render_template
import ujson
from libs.jobs import *
from libs.helpers import arg_checker
from libs.environment import *

import sys


def buildLogging():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    fh = logging.FileHandler('job_manager.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(' %(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)


app = Flask(__name__)
buildLogging()
local = dict()


@app.route('/status')
def job_status():
    job = Jobs()
    if 'id' in request.args:
        results = job.status(local['ini_file'], jtype='id', data=request.args['id'])
    elif 'email' in request.args:
        results = job.status(local['ini_file'], jtype='email', data=request.args['email'])
    elif 'all' in request.args:
        results = job.status(local['ini_file'], jtype='all')
    else:
        results = {'status': 'Failure', 'message': 'Bad Argument to status call'}
    return ujson.dumps(results)


@app.route('/new')
def new_job():
    job = Jobs()
    required = [
        'email',
        'job_type',
        'notify'
    ]
    data = arg_checker(request.args.keys(), required)
    if data['status'] == 'Failure':
        return ujson.dumps(data)
    return ujson.dumps(job.new(local['ini_file'], request.args['job_type'], request.args['email'],
                               request.args['notify']))


@app.route('/update')
def update_job():
    job = Jobs()
    required = [
        'id',
        'percentage'
    ]
    data = arg_checker(request.args.keys(), required)
    if data['status'] == 'Failure':
        return ujson.dumps(data)
    try:
        percentage = int(request.args['percentage'])
    except:
        return ujson.dumps({'status': 'Failure', 'message': 'Percentage not between 0 and 100'})
    if percentage < 0 or percentage > 100:
        return ujson.dumps({'status': 'Failure', 'message': 'Percentage not between 0 and 100'})
    return ujson.dumps(job.update(local['ini_file'], request.args['id'], request.args['percentage']))


@app.route('/completed')
def complete_job():
    job = Jobs()
    required = [
        'id',
        'message'
    ]
    data = arg_checker(request.args.keys(), required)
    if data['status'] == 'Failure':
        return ujson.dumps(data)
    log.info("complete_job: %s" % request.args)
    return ujson.dumps(job.completed(local['ini_file'], request.args['id'], request.args['message']))


@app.route('/error')
def error_job():
    job = Jobs()
    required = [
        'id',
        'message'
    ]
    data = arg_checker(request.args.keys(), required)
    if data['status'] == 'Failure':
        return ujson.dumps(data)
    return ujson.dumps(job.error(local['ini_file'], request.args['id'], request.args['message']))


@app.route('/delete')
def delete_job():
    job = Jobs()
    required = [
        'id',
        'message'
    ]
    data = arg_checker(request.args.keys(), required)
    print "data: ", data
    if data['status'] == 'Failure':
        return ujson.dumps(data)
    return ujson.dumps(job.delete(local['ini_file'], request.args['id'], request.args['message']))


@app.route('/purge')
def purge_job():
    job = Jobs()
    required = [
        'id',
        'auth_key'
    ]
    data = arg_checker(request.args.keys(), required)
    print "data: ", data
    if data['status'] == 'Failure':
        return ujson.dumps(data)
    return ujson.dumps(job.purge(local['ini_file'], request.args['id'], request.args['auth_key']))


@app.route('/flip_notify')
def flip_notify_job():
    job = Jobs()
    required = [
        'id',
        'notify'
    ]
    data = arg_checker(request.args.keys(), required)
    print "data: ", data
    if data['status'] == 'Failure':
        return ujson.dumps(data)
    return ujson.dumps(job.flip_notify(local['ini_file'], request.args['id'], request.args['notify']))


@app.route('/usage')
def usage():
    return render_template('usage.html')

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n\n\nERROR: Missing config.ini parameter\nUsage: nohup python job_manager.py $config.ini &\n\n\n"
        exit()
    ini_file = sys.argv[1]
    env = Environment(ini_file)
    app.debug = True
    local['ini_file'] = ini_file
    # app.run(host='0.0.0.0', port=9989)
    app.run(host='0.0.0.0', port=int(env.getSetting('port')))
