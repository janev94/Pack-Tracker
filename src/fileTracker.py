import json
import time
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pprint import pprint


class ChangeHandler(PatternMatchingEventHandler):
    patterns = ["*.*"]

    def __init__(self):
        super(ChangeHandler, self).__init__()

    def process(self, event):
        '''
        event.event_type: The type of the event as a string.
        event.src_path: Source path of the file system object
                that triggered this event
        event.is_directory: True if event was emitted for
                a directory; False otherwise.
        '''
        print event.event_type
        print event.src_path
        print event.is_directory
        # DO UPLOAD HERE

    def on_modified(self, event):
        if 'Achievements.log' in event.src_path:
            print "PATH:\n ------\n\n ACH MOD \n\n------"

            logfile = open(event.src_path, "r")
            loglines = follow(logfile)
            for line in loglines:
                print "LINE: ", line,

            # f = open('Achievements.log', 'r')
            # content = f.read()
            # print content
            # print "\n\n\n\n"

        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        '''
        file is deleted, maybe do some other operations?
        '''
        pass


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    f = open('../packTracker.cfg', 'r')
    config = json.loads(f.read())
    f.close()

    observer = Observer()
    PATH_TO_HS_LOG = config['pathToHS']
    path = os.path.join(PATH_TO_HS_LOG, "")

    print path

    observer.schedule(ChangeHandler(), path=path,
                      recursive=True)
    observer.start()
    while True:
        time.sleep(1)


