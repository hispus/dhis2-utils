#!/usr/bin/env python3

# This script deletes all metadata objects in a DHIS2 instance that are of a specified type
# and whose name contains a specified substring. Use with caution!

# Usage example:
# python3 delete.py http://servername/dhis2 username password predictors "ACT 06s"

import sys
import requests
import json
import urllib

if len(sys.argv) != 6:
	print('Usage: python3 delete.py server username password type substring')
	sys.exit(0)

server, username, password, typ, match = sys.argv[1:]
api = server + '/api/'
credentials = (username, password)

url = api + typ + '?fields=name,id&paging=none&filter=name:like:' + urllib.parse.quote_plus(match)
try:
	r = requests.get(url, auth=credentials)
except:
	print("Server call didn't work out. Perhaps server, username or password are incorrect.")
	sys.exit(0)
if r.status_code != 200:
	print("HTTP status code: ", r.status_code)
	print("Error trying to find '" + typ + "' like '" + match + "'")
	sys.exit(0)

objects = r.json()[typ]
if len(objects) == 0:
	print("No '" + typ + "' matching '" + match + "'")
for o in objects:
	print ("Deleting " + typ + " " + o['name'])
	r = requests.delete(api + typ + '/' + o['id'], auth=credentials)
	if r.status_code != 200:
		print("HTTP status code: ", r.status_code)
