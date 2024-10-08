import threading


class EmailThread(threading.Thread):
    def __init__(self, email_object):
        threading.Thread.__init__(self)

        self.email_object = email_object

    def run(self):
        self.email_object.send()
