import cups


class PrinterMgmt():
    def __init__(self, printer_name):
        self.conn = cups.Connection()
        self.info = self.get_printer(u'Star FVP10')
        self.destination = self.get_destination('Star_FVP10')

    # get reference to the queue object that will
    # be examined on print.
    # Returns tuple (printer)
    def get_printer(self, printer_name):
        printers = self.conn.getPrinters()
        for printer in printers:
            try:
                if printers[printer]['printer-make-and-model']\
                        == printer_name:
                    return printers[printer]
            except:
                # no valid destinations
                continue

    # destination used to clear the queue
    def get_destination(self, printer_name):
        destinations = self.conn.getDests()
        for destination in destinations:
            if (destination[0]):
                if (destination[0].startswith(printer_name)):
                    return destination[0]


    # clears the receipt printer queue
    def clear(self):
        self.conn.cancelAllJobs(self.destination)
        pass