#!/usr/bin/python3

import json
import re
import sys
import bs4

import html2markdown


def mangle_desc(desc):
    s = bs4.BeautifulSoup(desc)
    # strip tags we largely don't care about
    for tn in ['a', 'b', 'html', 'body', 'u', 'i', 'strong', 'div', 'span', 'blockquote', 'cite', 'ins', 'pre', 'sup']:
        for t in s.findAll(tn):
            t.replaceWithChildren()

    # kill things that aren't english-ish or are hard to represent
    for tn in ['img', 'figure', 'table']:
        for t in s.findAll(tn):
            t.decompose()

    # kill most attributes since we can't represent them well
    for tn in ['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'br']:
        for t in s.findAll(tn):
            t.attrs = {}

    desc = html2markdown.convert(str(s))
    return mangle_field(desc)


def mangle_field(f):
    # I don't know, encoding is hard.
    f = f.replace('&nbsp;', '')
    f = f.replace('&amp;', '&')
    return f


if __name__ == '__main__':
    infile = 'games.json'
    if len(sys.argv) >= 2:
        infile = sys.argv[1]

    games = None
    with open(infile, 'r') as f:
        games = json.loads(f.read())

    bad_ids = {
        # can't get markdown to generate right
        3313,
    }
    print('===')
    for g in games:
        if g['id'] in bad_ids:
            continue

        name = g['name']
        deck = g['deck']
        desc = g['description']

        # kill low-quality entries
        if deck is None or desc is None or len(desc) < 200:
            continue

        name = mangle_field(name)
        deck = mangle_field(deck)
        desc = mangle_desc(desc)

        # seperator
        print(name + "\n")
        print(deck + "\n")
        print(desc)
        print('===')
