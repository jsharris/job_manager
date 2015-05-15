#!/bin/sh

#
# start the server
#

# Customizable settings go here
export HOME_DIR=/home/job_manager
export PROG_DIR=job-manager
export MY_PATH=${HOME_DIR}/${PROG_DIR}

export INI_FILE=BOGUS.ini
export INI_PATH=${MY_PATH}/ini_files/${INI_FILE}

export PROGRAM=${MY_PATH}/job_manager.py

##### Do not modify below this line #####


# ensure start is configured correctly before doing anything
if [ ${INI_FILE} = "BOGUS.ini" ]; then
    echo ""
    echo "ERROR: start_job_manager_server.sh has not been configured for this server"
    echo "       Edit start_job_manager_server.sh and put the correct ini filename in the INI_FILE definition"
    echo ""
    exit
fi

# ensure specified ini file actually exists
if [ ! -f ${INI_PATH} ]; then
    echo ""
    echo "ERROR: Cannot locate $INI_PATH"
    echo "       Make sure the correct ini file is specified in the INI_FILE definition"
    echo ""
    exit
fi


cd ${MY_PATH}
nohup python ${PROGRAM} ${INI_FILE} &
