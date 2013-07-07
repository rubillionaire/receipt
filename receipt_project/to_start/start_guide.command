#!/Users/risdworks/Documents/receipt_env/bin/python

from subprocess import Popen, PIPE

# setup django process
ENV_ROOT = '/Users/risdworks/Documents/receipt_env'

activate = "{0}/bin/activate_this.py".format(ENV_ROOT)

execfile(activate, dict(__file__=activate))


MANAGE_PATH = '/Users/risdworks/Documents/receipt_env/' +\
              'repo/receipt/receipt_project/receipt_project/manage.py'

command = 'python {0} runserver 10.0.1.26:8000 '.format(MANAGE_PATH) +\
          '--settings=receipt_project.settings.production'

django = Popen(command,
               shell=True,
               stdout=PIPE).stdout

django.read()
