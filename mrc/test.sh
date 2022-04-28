#!/usr/bin/env bash

echo "== Set variables =="
declare -a nodes=(172.26.128.22 172.26.128.123 172.26.131.52)
declare -a ports=(5984 15984 25984)
export master_node=172.26.128.22
export master_port=5984
export size=${#nodes[@]}
export user=admin
export pass=admin
echo "--------"
for node in "${nodes[@]}"; do  curl -X GET "http://${user}:${pass}@${node}:5984/_all_dbs"; done