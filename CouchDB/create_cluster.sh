#This file is developed by Team 52 of COMP90024 of The University of Melbourne.
#Researched cities : All the cities in Melbourne region
#Team member - id
#Nitish Mathur  				            954892     
#Yash Shinde     				            920691
#Nakia Silva  					            796504
#Shreyas Walvekar    				            961621
#Krishna Srinivas Sundararajan  		            977863

#!/bin/bash

# Usage: create-cluster.sh user password port local-port space-separated-ips

user="server_admin"
password="password"
port=$1
localPort=$2
ips=$3

firstIp=1

for ip in $ips; do

  if [ "$firstIp" == "1" ]; then

    echo "First IP=$ip"

    firstIp=$ip

  else

    echo "Registering membership for $ip"

    curl -X PUT http://$user:$password@$firstIp:$localPort/_nodes/couchdb@$ip -d {}

  fi

done

# Create system DBs
echo "Creating _users"
curl -X PUT http://$user:$password@$firstIp:$port/_users
echo "Creating _replicator"
curl -X PUT http://$user:$password@$firstIp:$port/_replicator
echo "Creating _global_changes"
curl -X PUT http://$user:$password@$firstIp:$port/_global_changes
