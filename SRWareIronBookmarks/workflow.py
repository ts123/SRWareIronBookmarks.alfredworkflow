#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import json

import alfred
import jsonpath

BOOKMARK_PATH = os.path.join(os.environ['HOME'], 'Library/Application Support/Chromium/Default/Bookmarks')

def main(query):
    results = []
    json_ = json.load(file(BOOKMARK_PATH))
    uid = uid_generator()
    for entry in jsonpath.jsonpath(json_, '''$..?(@.url and @.type=='url')'''):
        if not query in entry['name'].lower() and not query in entry['url']:
            continue
        results.append(alfred.Item(
            attributes = { 'uid': uid.next(), 'arg': entry['url'] }, 
            title = entry['name'], 
            subtitle = entry['url'], 
            icon = 'icon.png'))
    alfred.write(alfred.xml(results))

def uid_generator():
    import time
    uid = time.time()
    while True:
        uid += 1
        yield uid

if __name__ == '__main__':
    import sys
    main(unicode(sys.argv[1], 'utf-8'))

