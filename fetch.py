#!/usr/bin/python3

import json
import os
import sys
import time
import urllib.request

if __name__ == '__main__':
    api_key = os.environ['GB_API_KEY']
    if not api_key:
        print('API key must be provided in env GB_API_KEY')
        sys.exit(1)

    outfile = 'games.json'
    if len(sys.argv) >= 2:
        outfile = sys.argv[1]

    # Load in what games already exist.
    games = []
    try:
        with open(outfile, 'r') as f:
            games = json.loads(f.read())
    except FileNotFoundError:
        # Don't worry if the file doesn't exist, we'll make it.
        pass

    offset = None
    if len(games) != 0:
        offset = games[-1]['id']

    success = False
    while True:
        url = 'https://www.giantbomb.com/api/games/?' + \
            urllib.parse.urlencode({'api_key': api_key, 'format': 'json'})
        if offset:
            url += '&offset='+str(offset)

        print('fetching from id offset {}'.format(offset))
        r = urllib.request.urlopen(url)
        j = json.loads(r.read())
        if j['status_code'] != 1:
            # we've hit some kind of error, stop now, print it, and save what we've gathered.
            print(
                'got non-ok status code {}, error: {}'.format(j['status_code'], j['error']))
            break

        # We're at the end, congrats!
        if j['results'] is None or len(j['results']) == 0:
            success = True
            break

        games.extend(j['results'])
        offset = games[-1]['id']
        print('sleeping 10 seconds to give the api a rest')
        time.sleep(10)

    print('writing games to {}'.format(outfile))
    with open(outfile, 'w') as f:
        f.write(json.dumps(games))

    if not success:
        print('failed with error, maybe try again?')
        sys.exit(1)
