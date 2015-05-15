__author__ = 'jon'
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from environment import *


log = logging.getLogger()


def arg_checker(args, required=None):
    if required is None:
        return {'status': 'Failure', 'message': 'Required argument list not supplied'}
    if args is None:
        return {'status': 'Failure', 'message': 'No Args supplied to check'}

    missing = []
    for r in required:
        if r not in args:
            missing.append(r)
    if len(missing) > 0:
        return {'status': 'Failure', 'message': 'Missing required parameters: %s' % missing}
    else:
        return {'status': 'Success'}


def email(ini_file, job, job_id):
    env = Environment(ini_file)

    if env.getSetting('mailserver') is not None:
        me = 'noreply@sharedshelf.org'

        status = job.status(ini_file, 'id', job_id)
        you = status['data'][0]['email']

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Your Shared Shelf media files are ready"
        msg['From'] = "Shared Shelf <%s>" % me
        msg['To'] = you

        # html = email_completion_msg(status['data'][0]['message'])
        html = email_message(status['data'][0]['message'])

        # print "html: ", html

        part1 = MIMEText(html, 'html')

        msg.attach(part1)

        try:
            server = smtplib.SMTP(env.getSetting('mailserver'))
            server.sendmail(me, you, msg.as_string())
            server.quit()
            status = {'status': 'Success'}
        except:
            log.error('Problem sending mail')
            status = {'status': 'Failure', 'message': 'Problem sending email'}
    else:
        log.info('No mail server configured, so do not sent mail, and return success')
        status = {'status': 'Success'}
    return status


def email_message(message):

    # feel free to change the default promo message, this was originally developed to notify when a batch job was
    # finished generating user requested data and to provide a link to fetch the zipped results
    if type(message) is list:
        # expect 2 items in list
        if len(message) == 1:
            promo_msg = "Your files are ready to download"
            main_msg = message
        else:
            promo_msg = message[0]
            main_msg = message[1]
    else:
        promo_msg = "Your files are ready to download"
        main_msg = message

    # everything after here can be customized for generating html formatted email
    promo_block = '<p style="font-family: Times New Roman, Times, serif; font-size: 36px; font-weight: bold; line-height: 38px; word-spacing: -1px; letter-spacing: -1px; color: #5FD665 !important; margin: 0; ">%s.</p>' % promo_msg
    main_block = '<p style="color: #000000; font-family: Arial, sans-serif; font-size: 16px; line-height: 21px; margin: 1em 0;"> %s</p>' % main_msg

    header_start = """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Shared Shelf</title>
    </head> """

    body_start = """
    <body style="width:100% !important; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; margin:0; padding:0;">
        <style type="text/css">
            table td {border-collapse: collapse;}
                a {
                    color: #969696;
                    font-size: 10px;
                    font-family: Arial, sans-serif;
                    text-decoration: none;
                }
        </style>
    """

    # do any extra stuff here like links to home page, email us links, etc...
    body_content = """
"""

    body_end = """
    </body>
    """

    header_end = """
    </html>
    """

    return header_start + body_start + promo_block + main_block + body_content + body_end + header_end


def email_completion_msg(msg):
    html = """\
    <html>
        <head></head>
        <body>
            Your batch job has been completed.<br>
            <br>
            ==================================================<br>
            Job Completion Message:<br>
            %s<br>
            ==================================================<br>
            <br>
            Thank You<br>
        </body>
    </html>
    """ % msg

    return html


def email_submission_msg():
    html = """\
    <html>
        <head></head>
        <body>
            Your batch job has been submitted for processing.<br>
            <br>
            You will receive an email when the job has completed.<br>
            <br>
            Thank You<br>
        </body>
    </html>
    """

    return html


def email_error_msg(msg):
    html = """\
    <html>
        <head></head>
        <body>
            Your batch job has encountered an error during processing.<br>
            <br>
            ==================================================<br>
            Details are as follows:<br>
            %s<br>
            ==================================================<br>
            <br>
            Thank You<br>
        </body>
    </html>
    """ % msg

    return html