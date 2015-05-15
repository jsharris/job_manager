# Job Manager Installation Instructions
* Requires: working from an account with sudo privs
* Requires: a postgreSQL account with admin role
* Assumes: Linux, easily adaptable to other Unix type platforms

## Account Creation from an account with sudo privs
* sudo useradd job_manager
* sudo passwd job_manager

## Account Configuration
* sudo job_manager

### Create a python virtual environment
* virtualenv Ð-no-site-packages Env

### Update path so local python is found first
Edit .profile and add the following to the end of the file

    if [ -d "$HOME/Env" ] ; then
    		PATH=$HOME/Env/bin:$PATH
	fi

Reload the user environment

    . .profile
    
* Add python packages


    pip install flask
    pip install ujson
    pip install requests
    pip install psycopg2
    
### Localization
Edit job_manager/scripts/start_job_manager_service.sh

    Change the following line to something server appropriate:
        export INI_FILE=BOGUS.ini
    To something server appropriate, like:
        export INI_FILE=qa.ini

Ini file configuration
  
    Copy the sample.ini to an appropriate name
    Edit the new file
        Modify the port if want to run on a different port
        Set the auth_key to anything or just leave it as is
        Set the mailserver to an appropriate server
        Set the password to be the password that will be used for the postgreSQL user
        
## Database Configuration - This will require a postgreSQL account with the admin role
    cd ~job_manager/tools
    
Update create_db.sql to change the password for the job_manager account

    psql ÐU{POSTGRESQL_ADMIN_ACCOUNT} < create_db.sql
    psql ÐU{POSTGRESQL_ADMIN_ACCOUNT} < seed_data.sql


## Start up the application
    nohup scripts/start_job_manager_server.sh &
    
## Optional - Install the start/stop scripts for boot start and shutdown
Assumes Ubuntu 12.04, change as required for platform specific commands

    sudo cp scripts/init_job_manager server.sh /etc/init.d/job_manager
    sudo update-rc.d job_manager defaults
    
    
## Optional - Install a ProxyPass rule for Apache
Add this before the ProxyPass / ProxyPassReverse entry for / - if no ProxyPass, add right after DocumentRoot definition<br>
!!! Warning:  Make sure your apache is configured correctly before enabling any ProxyPass rules<br>
Change the port if necessary to the one you configured in the ini file

    ProxyPass        /job_manager/	http://localhost:9989/
    ProxyPassReverse /job_manager/	http://localhost:9989/

