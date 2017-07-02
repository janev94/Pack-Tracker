import json
import re
import time
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


cardsOpened = 0
packsOpened = 0

# lineString has the following format, extracted from HS logs
# D TIME_INFO EVENT_FIRED: EVENT INFO
# for card gained, the event info is in the form:
# [name=CARD_NAME cardId=CARD_ID type=CARD_TYPE]
def processCardGained(lineString):
    cardId_regex = re.search('cardId=(.*) type=', lineString)
    card_id = cardId_regex.group(1)


    #TODO: extract card with following id from (DB/API)
    global cardsOpened, packsOpened
    cardsOpened += 1
    if cardsOpened % 4 == 0:
        packsOpened += 1
        #update the pack opened json


class ChangeHandler(PatternMatchingEventHandler):
    def __init__(self):
        super(ChangeHandler, self).__init__()

    @staticmethod
    def process(event):
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

            logfile = open(event.src_path, "r")
            loglines = follow(logfile)
            for line in loglines:
                if 'NotifyOfCardGained' in line:
                    processCardGained(line)
                print "LINE: ", line,


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

    #read previously saved data
    f = open('../data/packStats.dat', 'r')
    global packsOpened, cardsOpened
    packsOpened = json.loads(f.read())['packs opened']
    cardsOpened = 0
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
