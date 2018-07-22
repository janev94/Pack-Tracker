import json
import re
import time
import os
import requests

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

exp_lookup = {
    'OG': 'Whispers of the Old Gods.dat',
    'UNG': "Journey to Un'Goro.dat",
    'GVG': "Goblins vs Gnomes.dat",
    'AT': "The Grand Tournament.dat",
    'BRM': "Blackrock Mountain.dat",
    'NAX': "Naxxramas.dat",
    'LOE': "The League of Explorers.dat",
    'CFM': "Mean Streets of Gadgetzan.dat",
    'EX1': "Classic.dat",
    'KAR': "One Night in Karazhan.dat",
}


# lineString has the following format, extracted from HS logs
# D TIME_INFO EVENT_FIRED: EVENT INFO
# for card gained, the event info is in the form:
# [name=CARD_NAME cardId=CARD_ID type=CARD_TYPE]
def processCardGained(lineString):
    cardId_regex = re.search("cardId=(.*) type=", lineString)
    card_id = cardId_regex.group(1)
    exp_key = card_id[:card_id.index('_')]
    fname = ''
    for (k, v) in exp_lookup.iteritems():
        if exp_key in k:
            fname = v
            break

    if not fname:
        print 'Unrecognized card ID: %s' % exp_key
        return

    jsonFile = open('../expansions/' + fname, 'r')
    ogJson = json.loads(jsonFile.read())
    card = None
    for card_desc in ogJson.values()[0]:
        if card_desc['cardId'] == card_id:
            card = card_desc
            break

    if not card:
        print 'No card was found'
        return

    openedStatsFile = open('../data/cardsOpened.dat', 'r+')
    # fix this logic
    # if openedStatsFile.read():
    content = openedStatsFile.read()

    openedJson = json.loads(content)

    # else:
    #     openedJson = {}

    previousStats = openedJson.get(card['name'],  0)
    previousStats += 1
    openedJson[card['name']] = previousStats
    openedStatsFile.write(json.dumps(openedJson))
    print 'Cards file updated'


    global cardsOpened, packsOpened

    cardsOpened += 1
    print "cards opened: %d" % cardsOpened

    if cardsOpened % 4 == 0:
        packsOpened += 1
        packsFile = open('../data/packStats.dat', 'r+')
        packsJson = json.loads(packsFile.read())
        packsJson['packs opened'] = packsJson['packs opened'] + 1
        packsFile.write(json.dumps(packsJson))
        print 'packs updated'


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
