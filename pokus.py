#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikitools
from wikitools import api
import poster
import json

from xml.dom import minidom

print 'Nacitam xml'

xmldoc = minidom.parse('vodky.xml')
pageList = xmldoc.getElementsByTagName('page')

chlasty = []
kalby = []


for s in pageList:
	title = s.getElementsByTagName('title')
	text = s.getElementsByTagName('text')
	val = title[0].firstChild.nodeValue
	if not ':' in val:
		content = text[0].firstChild.nodeValue
		if '201' in val:
			kalby.append((val, content))
		else:
			chlasty.append((val, content))
#mrdky na zacatku
chlasty.pop(0)
chlasty.pop(0)

print 'nacteno'

print 'zkousim cupkyvodky.cz'

wiki = wikitools.wiki.Wiki('http://www.cupkyvodky.cz/api.php')
loginSuccess = wiki.login(username='cupkyadmin', password='Karelerak1')

print "login ok = " +  str(loginSuccess)

getTokenParams = {'action' : 'query', 'meta' : 'tokens'}
tokenRequest = api.APIRequest(wiki, getTokenParams)
tokenQuery = tokenRequest.query()
tokenQuery = tokenQuery['query']
tokenQuery = tokenQuery['tokens']
token = tokenQuery['csrftoken']
#tokenQuery = json.loads(str(tokenQueryJson))

print 'Token: ' + str(token)

print 'importuju kalby'

#editParams = {'action': 'edit', 'assert': 'user', 'format': 'json', 
#'text': 'nazdar chlaste, čuráci', 'summary': 'bot import', 'title': 'OMFG', 'token': token}
#editRequest = api.APIRequest(wiki, editParams)
#editQuery =  editRequest.query()
#print editQuery

#print chlasty[0][0]
#print chlasty[0][1]

for kalba in kalby:
	editParams = {'action' : 'edit', 'assert' : 'user', 'format' : 'json',
	'text' : kalba[1], 'summary' : 'bot import', 'title' : kalba[0],
	'token' : token}
	editRequest = api.APIRequest(wiki, editParams)
	editRequest.query()	

print 'hotovo'
print 'logout'
wiki.logout()













