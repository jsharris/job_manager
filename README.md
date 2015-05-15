# README #

* Quick summary
Framework for registering and tracking batch jobs.  Includes email notification events on completion, error and delete events
* Version 1.0


### How do I get set up? ###

* Summary of set up
Requires a postgres database.
Run the sql scripts:
    create_db.sql
    seed_data.sql
Run the server - python job_manager.py

* Configuration
via ini files located in the ini_files directory

* Dependencies
postgres server
python

* Database configuration
see the sql files

* How to run tests
unit tests run under pycharm

* Deployment instructions
See doc in the docs directory