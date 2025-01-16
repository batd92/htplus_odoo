import os, time, sys
import re, shutil
import logging
import paramiko
_logger = logging.getLogger(__name__)

def ishostaccessible(details):
    response = dict(
        status=True,
        message='Success'
    )
    try:
        ssh_obj = paramiko.SSHClient()
        ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _logger.info("Database Backup In check_connectivity scipt at Line {}".format(17))
        ssh_obj.connect(hostname = details['host'], username = details['user'], password = details['password'], port = details['port'])
        response['result'] = ssh_obj
        return response
    except Exception as e:
        _logger.info("Couldn't connect remote %r"%e)
        response['status'] = False
        response['message'] = e
    return response
