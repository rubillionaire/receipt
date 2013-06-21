import cups


class PrinterMgmt():
    def __init__(self, printer_name):
        self.conn = cups.Connection()
        self.queue = self.get_dest(printer_name)

    # get reference to the queue object that will
    # be examined on print.
    def get_dest(self, printer):
        destinations = self.conn.getDests()
        for destination in destinations:
            try:
                if destination[0].startswith(printer):
                    return destination
            except:
                # no valid destinations
                continue
