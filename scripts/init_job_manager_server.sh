#! /bin/sh
### BEGIN INIT INFO
# Provides:             job_manager
# Required-Start:       $syslog
# Required-Stop:        $syslog
# Should-Start:         $local_fs
# Should-Stop:          $local_fs
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short-Description:   	Job Manager Service
# Description:          Job Manger Service
### END INIT INFO


PATH=/home/job_manager/Env/bin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MY_HOME=/home/job_manager/job-manager
START_SCRIPT=$MY_HOME/scripts/start_job_manager_server.sh
STOP_SCRIPT=$MY_HOME/scripts/stop_job_manager_server.sh

NAME=job_manager.py
DESC="Job Manager Service"

test -x $DAEMON || exit 0

set -e
echo "stop: " $STOP_SCRIPT

case "$1" in
    start)
        echo -n "Starting $DESC: "
        if start-stop-daemon --start --quiet --umask 007 --chuid job_manager:job_manager --exec $START_SCRIPT
        then
            echo "$NAME."
        else
            echo "failed"
        fi
        ;;

    stop)
        echo -n "Stopping $DESC: "
        if [ -x $STOP_SCRIPT ]
        then
            $STOP_SCRIPT
            echo "$NAME."
        else
            echo "failed"
        fi
        ;;

    restart|reload)
        ${0} stop
        ${0} start
        ;;

    *)
        echo "Usage: /etc/init.d/$NAME {start|stop|restart|reload}" >&2
        exit 1
        ;;
esac

exit 0
