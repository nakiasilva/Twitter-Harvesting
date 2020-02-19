#!/bin/bash

. ./unimelb-comp90024-group-52-openrc.sh; ansible-playbook -i hosts -u ec2-user --key-file=~/.ssh/sins101 wordpress.yaml
