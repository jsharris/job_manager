__author__ = 'jon'
# -*- coding: utf-8 -*-

import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from environment import *
# from database import *
# from jobs import *


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
    Env = Environment(ini_file)

    if Env.getSetting('mailserver') is not None:
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
            server = smtplib.SMTP(Env.getSetting('mailserver'))
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

    if type(message) is list:
    # expect 2 items in list
        promo_msg = message[0]
        main_msg = message[1]
    else:
        promo_msg = "Your files are ready to download"
        main_msg = message


    promo_block = '<p style="font-family: Times New Roman, Times, serif; font-size: 36px; font-weight: bold; line-height: 38px; word-spacing: -1px; letter-spacing: -1px; color: #5FD665 !important; margin: 0; ">%s.</p>' % promo_msg
    main_block = '<p style="color: #000000; font-family: Arial, sans-serif; font-size: 16px; line-height: 21px; margin: 1em 0;"> %s</p>' % main_msg

    # print "promo: ", promo_msg
    # print "main: ", main_msg
    html = """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Shared Shelf</title>
    </head> """

    html2 = """
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

    <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; margin: 0 !important; padding: 0 !important; width: 100% !important; line-height: 100% !important;" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td>
                <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; margin: 16px auto 16px auto;" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" width="632" height="36" valign="top">
                     <tr>
                        <td width="16"></td>
                        <td valign="top">
                            <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" cellpadding="0" cellspacing="0" border="0" bgcolor="#000000" height="36" valign="top">
                                <tr>
                                    <td width="16" height="36"></td>
                                    <td width="584" height="36" valign="center">
                                            <a href="http://catalog.sharedshelf.artstor.org/login.html" target="_blank"> <img src="http://design.artstor.acit.com/design2/sharedshelfemail/ShSh_White_v2-01.gif" alt="Shared Shelf" title="Shared Shelf" width="113" height="16" style="outline:none; text-decoration:none; -ms-interpolation-mode: bicubic; display:block; border: none;" /></a></td>
                                </tr>
                            </table>
                        </td>
                        <td width="16"></td>
                    </tr>
                    <tr>
                        <td width="16"></td>
                        <td height="64"></td>
                        <td width="16"></td>
                    <tr>
                    <tr>
                        <td width="16"></td>
                        <td valign="top">
                            <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" cellpadding="0" cellspacing="0" border="0" width="600">
                                <tr>
                                    <td width="108"></td>
                                    <td width="384" align="center">
    """
    html3 = """                                    </td>
                                    <td width="108"></td>
                                </tr>
                            </table>
                        </td>
                        <td width="16"></td>
                    </tr>
                    <tr>
                        <td width="16"></td>
                        <td height="64"></td>
                        <td width="16"></td>
                    <tr>
                    <tr>
                        <td width="16"></td>
                        <td>
                            <hr style="background-color: #DCDCDC; color: #DCDCDC; border: 0; margin: 0; height: 1px; width: 600px;" />
                        </td>
                        <td width="16"></td>
                    </tr>
                    <tr>
                        <td width="16"></td>
                        <td height="34"></td>
                        <td width="16"></td>
                    </tr>
"""
    html4 = """
                    <tr>
                        <td width="16"></td>
                        <td valign="top">
                            <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" cellpadding="0" cellspacing="0" border="0" width="600">
                                <tr>
                                    <td width="50"></td>
                                    <td width="500">
"""

#                                        <p style="color: #000000; font-family: Arial, sans-serif; font-size: 16px; line-height: 21px; margin: 1em 0;"> The selected media files from the <strong> %s PROJECT_HERE </strong> have been zipped and are <a href="" style="font-size: 16px; font-weight: bold; color: #000000; text-decoration: underline;" target="_blank">ready to download</a>. This link will expire in 3 days.</p>
    html5 = """                                        <p style="color: #000000; font-family: Arial, sans-serif; font-size: 16px; line-height: 21px; margin: 1em 0;">Thanks,<br />Shared Shelf Support</p>
                                    </td>
                                    <td width="50"></td>
                                </tr>
                            </table>
                        </td>
                        <td width="16"></td>
                    </tr>
                    <tr>
                        <td width="16"></td>
                        <td height="64"></td>
                    <tr>
                    <tr>
                        <td width="16"></td>
                            <td>
                                <hr style="background-color: #DCDCDC; color: #DCDCDC; border: 0; margin: 0; height: 1px; width: 600px;" />
                        </td>
                        <td width="16"></td>
                    </tr>
                    <tr>
                        <td width="16"></td>
                        <td>
                            <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" cellpadding="0" cellspacing="0" border="0" width="600">
                                <tr>
                                    <td width="300" height="72" valign="center" align="center">
                                        <a href="http://help.artstor.org/sshelp/index.php/Training_Options" style="font-family: Times New Roman, Times, serif; font-size: 18px; line-height: 26px; color: #000000; text-decoration: underline;" target="_blank">Training Sessions</a>
                                    </td>
                                    <td width="300" height="72" valign="center" align="center">
                                        <a href="http://www.youtube.com/playlist?list=PLO02jn_Rv19pW8kfUPmGTcO3qkhhrUCdM" style="font-family: Times New Roman, Times, serif; font-size: 18px; line-height: 26px; color: #000000; text-decoration: underline;" target="_blank">How-to Videos</a>
                                    </td>
                                    <td width="300" height="72" valign="center" align="center">
                                        <a href="http://help.artstor.org/sshelp/index.php/Shared_Shelf_Help" style="font-family: Times New Roman, Times, serif; font-size: 18px; line-height: 26px; color: #000000; text-decoration: underline;" target="_blank">Online Help</a>
                                    </td>
                                <tr>
                            </table>
                        </td>
                        <td width="16"></td>
                    </tr>
                    <tr>
                        <td width="16"></td>
                        <td>
                            <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" cellpadding="0" cellspacing="0" border="0" width="600" bgcolor="#F4F4F4" style="background-color: #F4F4F4;">
                                <tr>
                                    <td width="16"></td>
                                    <td width="376"><p style="margin: 1em 0; padding-top: 4px; padding-left: 0px; padding-bottom: 4px; font-size: 12px; line-height: 18px; color: #A7A7A7; font-family: Arial, sans-serif;"><a href="mailto:support@sharedshelf.org" target="_blank" style="font-family: Arial, sans-serif; font-size: 12px; line-height: 18px; color: #A7A7A7; text-decoration: underline;">support@sharedshelf.org</a><br> © Artstor, 151 East 61st Street, New York, NY 10065</p></td>
                                    <td width="16"></td>
                                    <td width="176" align="right">
                                        <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td><a href="http://artstor.wordpress.com/" target="_blank"> <img src="http://design.artstor.acit.com/design2/sharedshelfemail/social-media-02.gif" alt="Artstor Blog" alt="Artstor Blog" height="28" width="28" style="outline:none; text-decoration:none; -ms-interpolation-mode: bicubic; display:block; border: none;"/></a></td>
                                                <td width="8"></td>
                                                <td><a href="http://www.youtube.com/user/artstor" target="_blank"> <img src="http://design.artstor.acit.com/design2/sharedshelfemail/social-media-04.gif" alt="Artstor Channel" alt="Artstor Channel" height="28" width="28" style="outline:none; text-decoration:none; -ms-interpolation-mode: bicubic; display:block; border: none;" /></a></td>
                                                <td width="8"></td>
                                                <td><a href="http://www.facebook.com/ARTstor" target="_blank"> <img src="http://design.artstor.acit.com/design2/sharedshelfemail/social-media-01.gif" alt="Facebook" alt="Facebook" height="28" width="28" style="outline:none; text-decoration:none; -ms-interpolation-mode: bicubic; display:block; border: none;" /></a></td>
                                                <td width="8"></td>
                                                <td><a href="http://twitter.com/ARTstor" target="_blank"> <img src="http://design.artstor.acit.com/design2/sharedshelfemail/social-media-03.gif" alt="Twitter" alt="Twitter" height="28" width="28" style="outline:none; text-decoration:none; -ms-interpolation-mode: bicubic; display:block; border: none;" /></a></td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td width="16"></td>
                                </tr>
                            </table>
                        </td>
                        <td width="16"></td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    <!-- End of wrapper table -->
    </body>
    </html>
    """

    return html + html2 + promo_block + html3 + html4 + main_block + html5


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