#!/bin/bash

. ./unimelb-COMP90024-2022-grp-13-openrc.sh;  ansible-playbook   --ask-become-pass  -u ubuntu  --key-file=~/mrccloud.key deploy_Instance.yaml