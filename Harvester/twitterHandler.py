#This file is developed by Team 52 of COMP90024 of The University of Melbourne.
#Researched cities : All the cities in Melbourne region
#Team member - id
#Nitish Mathur  				954892     
#Yash Shinde     				920691
#Nakia Silva  					796504
#Shreyas Walvekar    				961621
#Krishna Srinivas Sundararajan  		977863

import json
from datetime import date

import couchdb
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


from functionTimeline import getTimeline

class myListener(StreamListener):

	def on_data(self, data):
		# jData = json.parse(data)
		print ("2")	
		if data[0].isdigit():
			print(data)
			#pass
		else:
			jData = json.loads(data)
			uId = jData['user']['id_str']
			uCreationYear = int(jData['user']['created_at'][-4:])
			
			# insert into database if doesn't exist
			try:
				db[uId] = { 'user_year' :  uCreationYear }
				print(uId,uCreationYear)
				getTimeline(uId, c_server, auth)
			except Exception as e:
				print (e)

			# print(uId, uCreationYear)
			# exit(0)

	def on_error(self, status) :
		print ("Stream",status)


keyId = 0
keys = None

cityId = 0
cityBounds = None

dbname = 'twitter_results'
c_server = None

with open('apiKeys.json') as fKeys:
	keys = json.load(fKeys)

if keys == None:
	print('Failed to load apiKeys.\nExitting.')
	exit(0)

with open('boxBounds.json') as fBounds:
	cityBounds = json.load(fBounds)[cityId]

if cityBounds == None:
	print('Failed to load city bounds.\nExitting.')
	exit(0)

try:
	user = "server_admin"
	password = "password"
	c_server = couchdb.Server("http://%s:%s@localhost:5984/" % (user,password))

except:
	print ("Cannot connect to DB.\nExitting.")
	exit(0)

if dbname in c_server:
	db = c_server[dbname]
else:
	db = c_server.create(dbname)

auth = tweepy.OAuthHandler( keys[keyId]['consumer']['key'], keys[keyId]['consumer']['secret'] )
auth.set_access_token( keys[keyId]['access']['key'], keys[keyId]['access']['secret'] )
print ("1",auth)
twitterStream = Stream(auth, myListener())
twitterStream.filter(locations=cityBounds['box'])
