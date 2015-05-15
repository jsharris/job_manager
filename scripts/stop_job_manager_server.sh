#!/bin/sh

#
# script to stop a running job_manager server
#
# relies on finding the running pids and killing them off, not graceful, but it works
#

pids=`ps -ef | grep job_manager | grep ini | grep -v grep | awk '{print $2}'`
echo "list of pids: " $pids
for pid in $pids
do
    echo "killing: " $pid
    kill $pid
done
