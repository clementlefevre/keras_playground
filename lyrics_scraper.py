#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:28:32 2017

@author: ramon
"""

# coding: utf8
import urllib2,cookielib
import re
import time
from datetime import datetime

from bs4 import BeautifulSoup
from requests.utils import quote

file_name="lyrics.txt"
# create file
file = open(file_name,"w") 
file.write("")
file.close() 

BASE_URL = 'http://www.paroles-musique.com/paroles-Serge_Gainsbourg-lyrics,a689'

HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
def retrieve_titles():

    
    req = urllib2.Request(BASE_URL, headers=HDR)
    
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
        
    all_links = list()
    
    content = page.read()
    bs = BeautifulSoup(content)
    table = bs.find( "table", {"id":"art_track"} )
    rows = table.findAll('tr')
    
    for tr in rows:
        td = tr.find("td")
        try:
            all_links.append(td.find("a")["href"])
        except:
            print "no link"
    return all_links
    
def retrieve_lyrics(url):
    url = "http://www.paroles-musique.com/"+url[1:]
    req = urllib2.Request(url, headers=HDR)
    
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
        
    
    all_links = list()
    content = page.read()
    
    charset = page.headers['content-type'].split('charset=')[-1]

    print charset
    

    bs = BeautifulSoup(content)
    lyrics = bs.find( "div", {"id":"lyrics"} )
    return lyrics.text.encode('utf-8')
    
all_links = retrieve_titles()

for link in all_links:
    try:
        lyrics = retrieve_lyrics(link)
        print lyrics
        file = open(file_name,"a") 
        file.write(lyrics)
        file.close() 
    except Exception as e:
        print e


