from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from subprocess import call
import time

import cups


class PrinterMgmt():
    def __init__(self):
        self.conn = cups.Connection()
        self._refresh()

    def _get_printer(self, printer_name):
        # get reference to the queue object that will
        # be examined on print.
        # Returns tuple (printer)

        printers = self.conn.getPrinters()
        for printer in printers:
            try:
                if printers[printer]['printer-make-and-model']\
                        == printer_name:
                    return printers[printer]
            except:
                # no valid destinations
                continue

    def _get_destination(self, printer_name):
        # destination used to clear the queue

        destinations = self.conn.getDests()
        for destination in destinations:
            if (destination[0]):
                if (destination[0].startswith(printer_name)):
                    return destination[0]

    def _refresh(self):
        # refreshes references to the printer
        # and the destination, since pycups gives
        # a snapshot of whats currently going on.

        self.info = self._get_printer(u'Star FVP10')
        self.destination = self._get_destination('Star_FVP10')

    def _status(self):
        # gets the printer state

        self._refresh()
        # state of 3 means good to go.
        # state of 4 means there is a queue.
        if self.info['printer-state'] == 3:
            return True
        else:
            return False

    def _clear(self):
        # clears the receipt printer queue

        try:
            # cancel all jobs doesnt seem to be doing
            # what it is intended to do.
            # self.conn.cancelAllJobs(self.destination)

            # command line approach
            cancel = "cancel -a"
            call(cancel.split(" "))
        except:
            print "could not clear"
        pass

    def notify(self):
        # notifies the correct parties
        sender = 'ruben@thedesignoffice.org'
        recipient = ['ruben@thedesignoffice.org',
                     '2068530275@txt.att.net']

        msg = MIMEMultipart()
        msg['Subject'] = 'Receipt Printer Alert'
        msg['From'] = sender
        msg['To'] = ', '.join(recipient)
        msg.attach(MIMEText('The receipt printer needs a fresh roll of paper.'))

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(sender, '')
        s.sendmail(sender, recipient, msg.as_string())
        s.quit()
        pass

    def check(self):
        time.sleep(2)
        if not self._status():
            time.sleep(5)
            if not self._status():
                self._clear()
                self.notify()
                return {
                    'status': 0,
                    'message': 'Out of paper. Notification sent.'
                }
            return {
                'status': 1,
                'message': 'Ready for printing.'
            }
        else:
            return {
                'status': 1,
                'message': 'Ready for printing.'
            }


if __name__ == '__main__':
    receipt_printer = PrinterMgmt()
    # status = receipt_printer.check()
    # print status
    receipt_printer.notify()
