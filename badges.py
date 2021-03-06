#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# licensed under CC-Zero: https://creativecommons.org/publicdomain/zero/1.0

import requests
import json
import pywikibot
from pywikibot.data import api

site = pywikibot.Site('wikidata', 'wikidata')
site.login()
repo = site.data_repository()
site.get_tokens('edit')

tasks = [
    {
        'badge': 'Q17580674',
        'category': 'Featured portals',
        'language': 'en',
        'project': 'wikipedia',
        'site': 'enwiki'
    },
    {
        'badge': 'Q17506997',
        'category': 'Featured lists',
        'language': 'en',
        'project': 'wikipedia',
        'site': 'enwiki'
    },
    {
        'badge': 'Q17437796',
        'category': 'Featured articles',
        'language': 'en',
        'project': 'wikipedia',
        'site': 'enwiki'
    },
    {
        'badge': 'Q17437798',
        'category': 'Good articles',
        'language': 'en',
        'project': 'wikipedia',
        'site': 'enwiki'
    },
    {
        'badge': 'Q17437798',
        'category': u'Wikipedie:Dobré články',
        'language': 'cs',
        'project': 'wikipedia',
        'site': 'cswiki'
    },
    {
        'badge': 'Q17437796',
        'category': u'Wikipedie:Nejlepší články',
        'language': 'cs',
        'project': 'wikipedia',
        'site': 'cswiki'
    },
    {
        'badge': 'Q17437798',
        'category': u'Wikipédia:Dobré články',
        'language': 'sk',
        'project': 'wikipedia',
        'site': 'skwiki'
    },
    {
        'badge': 'Q17437796',
        'category': u'Wikipédia:Najlepšie články',
        'language': 'sk',
        'project': 'wikipedia',
        'site': 'skwiki'
    },
    {
        'badge': 'Q17580674',
        'category': 'Wikipedia:Informatives Portal',
        'language': 'de',
        'project': 'wikipedia',
        'site': 'dewiki'
    },
    {
        'badge': 'Q17506997',
        'category': 'Wikipedia:Informative Liste',
        'language': 'de',
        'project': 'wikipedia',
        'site': 'dewiki'
    },
    {
        'badge': 'Q17437796',
        'category': 'Wikipedia:Exzellent',
        'language': 'de',
        'project': 'wikipedia',
        'site': 'dewiki'
    },
    {
        'badge': 'Q17437798',
        'category': 'Wikipedia:Lesenswert',
        'language': 'de',
        'project': 'wikipedia',
        'site': 'dewiki'
    }    
]

# remove badges
for t in tasks:
    payload = {
        'categories': t['category'],
        'language': t['language'],
        'project': t['project'],
        'sparql': 'SELECT ?item WHERE { ?article schema:about ?item;wikibase:badge wd:'+t['badge']+';schema:isPartOf <https://'+t['language']+'.'+t['project']+'.org/>}',
        'source_combination': 'sparql not categories',
        'ns[0]': 1,
        'ns[100]': 1,
        'format': 'json',
        'doit': 'Do it!'
    }
    r = requests.get('https://petscan.wmflabs.org/', params=payload)
    data = r.json()
    for m in data['*'][0]['a']['*']:
        params = {
            'action': 'wbsetsitelink',
            'id': m['title'],
            'linksite': t['site'],
            'badges': '',
            'token': site.tokens['edit']
        }
        req = api.Request(site=site, **params)
        data = req.submit()

# add badges
for t in tasks:
    payload = {
        'categories': t['category'],
        'language': t['language'],
        'project': t['project'],
        'sparql': 'SELECT ?item WHERE { ?article schema:about ?item;wikibase:badge wd:'+t['badge']+';schema:isPartOf <https://'+t['language']+'.'+t['project']+'.org/>}',
        'source_combination': 'categories not sparql',
        'ns[0]': 1,
        'ns[100]': 1,
        'format': 'json',
        'doit': 'Do it!'
    }
    r = requests.get('https://petscan.wmflabs.org/', params=payload)
    data = r.json()
    for m in data['*'][0]['a']['*']:
        params = {
            'action': 'wbsetsitelink',
            'id': m['title'],
            'linksite': t['site'],
            'badges': t['badge'],
            'token': site.tokens['edit']
        }
        req = api.Request(site=site, **params)
        data = req.submit()
