#!/Users/risdworks/Documents/receipt_env/bin/python

import sys
import time
import socket
from subprocess import Popen, PIPE, call

# setup django process
ENV_ROOT = '/Users/risdworks/Documents/receipt_env'

SETUP_FF = '/Users/risdworks/Documents/receipt_env/' +\
    'repo/receipt/receipt_project/to_start/setup_firefox.app'

activate = "{0}/bin/activate_this.py".format(ENV_ROOT)

execfile(activate, dict(__file__=activate))


def check_ip():
    # if socket.gethostbyname(socket.gethostname()) == '10.2.80.98':
    address = socket.gethostbyname(socket.gethostname())
    if address.startswith('10.2'):
        return launch_server(address)
    else:
        print >>sys.stderr, "Not the corret ip."
        print >>sys.stderr, "currently: {0}".format(
            socket.gethostbyname(socket.gethostname()))
        return delay_check_ip()


def delay_check_ip():
    time.sleep(5)
    check_ip()


def launch_server(address):
    call(["open", SETUP_FF])
    MANAGE_PATH = '/Users/risdworks/Documents/receipt_env/' +\
                  'repo/receipt/receipt_project/receipt_project/manage.py'

    command = 'python {0} runserver '.format(MANAGE_PATH) +\
              '{0}:8000 '.format(address) +\
              '--settings=receipt_project.settings.production'

    django = Popen(command,
                   shell=True,
                   stdout=PIPE).stdout

    django.read()


check_ip()
