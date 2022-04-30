#!/bin/bash

. ./unimelb-COMP90024-2022-grp-13-openrc.sh;  ansible-playbook  -i inventory/hosts.ini -u ubuntu  --key-file=~/mrccloud.key deploy_harvest_streaming.yaml