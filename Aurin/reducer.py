#This file is developed by Team 52 of COMP90024 of The University of Melbourne.
#Researched cities : All the cities in Melbourne region
#Team member - id
#Nitish Mathur  				954892     
#Yash Shinde     				920691
#Nakia Silva  					796504
#Shreyas Walvekar    				961621
#Krishna Srinivas Sundararajan  		977863
import couchdb
import tweepy

def update_got_fan_base(got_user_db,grid_dict):
	print ("Calculating GOT Fan Base")
	for item in got_user_db.view('tweetAnalyzer/gotFanView',group=True):
		# print (item)
		user_id = item.key
		became_got_fan_in = int(item.value)
		if became_got_fan_in in list_of_years:
			increment_years = list_of_years[list_of_years.index(became_got_fan_in):]
			for year in increment_years:
				grid_dict[str(year)]['got_fans'] += 1


def update_user_count(user_creation_db,grid_dict):
	print (" Finding users created")
	for item in user_creation_db.view('_all_docs',include_docs=True):
		# print (item.doc)
		req_year = item.doc['user_year']
		if req_year in list_of_years:
			increment_years = list_of_years[list_of_years.index(req_year):]
			for year in increment_years:
				grid_dict[str(year)]['existing_users'] += 1


grid_dict = {}
list_of_years=[2010,2011,2012,2013,2014,2015,2016]

for year in list_of_years:
	grid_dict[str(year)]={"got_fans":0,"existing_users":0}

try:
	user = "server_admin"
	password = "password"
	c_server = couchdb.Server("http://%s:%s@localhost:5984/" % (user,password))
except:
	print ("Cannot connect to DB.\nExitting.")
	exit(0)

got_user_db = "twitter_timeline"
user_creation_db = "twitter_results"

if got_user_db in c_server:
	got_user_db = c_server[got_user_db]
else:
	got_user_db = c_server.create(got_user_db)

if user_creation_db in c_server:
	user_creation_db = c_server[user_creation_db]
else:
	user_creation_db = c_server.create(user_creation_db)


update_got_fan_base(got_user_db,grid_dict)
update_user_count(user_creation_db,grid_dict)
print (grid_dict)

front_end_db = "twitter_front_end"
#if front_end_db in c_server:
#	del c_server[front_end_db]

db = c_server[front_end_db]

def updateDoc(db, year, values):
	doc = db.get(year)
	doc["got_fans"] = values["got_fans"]
	doc["existing_users"] =values["existing_users"]	
	doc = db.save(doc)
	print ("Saved")

for year, values in grid_dict.items():
	updateDoc(db,year,values)

