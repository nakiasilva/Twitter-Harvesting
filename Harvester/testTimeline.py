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
import tweepy
# import couchdb


def getTimeline(userId, c_server, auth):


currentUser = 'shreyasAujc'
dbname = 'twitter_timeline'
keyId = 0
keys = None

# try:
# 	user = "server_admin"
# 	password = "password"
# 	c_server = couchdb.Server("http://%s:%s@localhost:5984/" % (user,password))

# except:
# 	print ("Cannot connect to DB.\nExitting.")
# 	exit(0)

with open('apiKeys.json') as fKeys:
	keys = json.load(fKeys)

if keys == None:
	print('Failed to load apiKeys.\nExitting.')
	exit(0)


# if # dbname in c_server:
# 	# db = c_server[# dbname]
# else:
# 	# db = c_server.create(# dbname)

try:
	
	auth = tweepy.OAuthHandler(keys[keyId]['consumer']['key'], keys[keyId]['consumer']['secret'])
	auth.set_access_token(keys[keyId]['access']['key'], keys[keyId]['access']['secret'])
	
	api = tweepy.API(auth)

	# start asking Twitter about the timeline
	twitDoc = {}
	twitDoc['docs'] = []
	for status in tweepy.Cursor(api.user_timeline, user_id=413132335, tweet_mode="extended", trim_user=True).items():
		try:
			twitYear = status.created_at.year
			twitUserId = status.user.id
			try:
				twitText = status.retweeted_status.full_text
			except:
				twitText = status.full_text
			
			twitDoc['docs'].append({'user_id':twitUserId,'year':twitYear,'text':twitText})
		except Exception as e:
			print(e)
	twitDoc['docs'].reverse()
					
	# INSERT INTO DB HERE
	print(json.dumps(twitDoc, indent=2))
	print ("Number of tweets in the timeline -,",len(twitDoc['docs']))
	print ("-"*10,"Connecting to DB","-"*10)
	count = 0
	for document in twitDoc['docs']:
		try:
			# db.save(document)
			count += 1
		except Exception as e:
			print (e)
			print (document)
	print ("-"*10,str(count)+" documents inserted","-"*10)



except TwitterSearchException as e: # catch all those ugly errors
	print(e)
