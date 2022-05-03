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
curl -H 'Content-Type: application/json' -X DELETE 'http://admin:admin@172.26.128.22:5984/melbourne/database_id?_rev'