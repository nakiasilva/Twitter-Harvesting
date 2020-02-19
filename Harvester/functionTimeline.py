#This file is developed by Team 52 of COMP90024 of The University of Melbourne.
#Researched cities : All the cities in Melbourne region
#Team member - id
#Nitish Mathur  				954892     
#Yash Shinde     				920691
#Nakia Silva  					796504
#Shreyas Walvekar    				961621
#Krishna Srinivas Sundararajan  		977863
import couchdb
from tweepy import API as tApi, Cursor as tCursor


def getTimeline(uId, c_server, auth):

	api = tApi(auth)

	# start asking Twitter about the timeline
	twitDoc = {}
	twitDoc['docs'] = []
	
	try:
		
		for status in tCursor(api.user_timeline, user_id=uId, tweet_mode="extended", trim_user=True).items():
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
		print ("Number of tweets in the timeline -,",len(twitDoc['docs']))
		print ("-"*10,"Connecting to DB","-"*10)
		
		dbname = 'twitter_timeline'
		if dbname in c_server:
			db = c_server[dbname]
		else:
			db = c_server.create(dbname)


		count = 0
		for document in twitDoc['docs']:
			try:
				db.save(document)
				count += 1
			except Exception as e:
				print (e)
				print (document)
		print ("-"*10,str(count)+" documents inserted","-"*10)

	except TwitterSearchException as e: # catch all those ugly errors
		print(e) 
