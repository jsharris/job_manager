#!/bin/sh

DATE=`/bin/date +%Y-%m-%d-%H:%M`

if [ -d ~job_manager/job-manager ]
then
	cd ~job_manager/job-manager
fi

if [ -f nohup.out ]
then
	cp nohup.out logs/nohup.out.$DATE
	cat /dev/null > nohup.out
fi

if [ -f job_manager.log ]
then
	cp job_manager.log logs/job_manager.log.$DATE
	cat /dev/null > job_manager.log
fi
