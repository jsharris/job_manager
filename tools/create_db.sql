CREATE USER job_manager WITH PASSWORD 'jmadmin' NOCREATEUSER NOCREATEDB NOCREATEROLE;

CREATE DATABASE job_manager
  WITH OWNER = job_manager
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;

GRANT ALL PRIVILEGES ON DATABASE job_manager to job_manager;

\c job_manager

CREATE TABLE status
(
  id serial NOT NULL,
  description text NOT NULL,
  CONSTRAINT stat_id_uniq UNIQUE (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE status OWNER TO job_manager;


CREATE TABLE job_type
(
  id serial NOT NULL,
  description text NOT NULL,
  CONSTRAINT jt_id_uniq UNIQUE (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE job_type OWNER TO job_manager;


CREATE TABLE jobs
(
  id serial NOT NULL,
  job_type_id integer NOT NULL,
  email text NOT NULL,
  submitted timestamp without time zone NOT NULL,
  last_updated timestamp without time zone NOT NULL,
  status_id integer NOT NULL,
  percentage integer NOT NULL,
  notify boolean NOT NULL,
  message text,
  CONSTRAINT id_pkey PRIMARY KEY (id),
  CONSTRAINT jt_id_fkey FOREIGN KEY (job_type_id)
      REFERENCES job_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT status_id_fkey FOREIGN KEY (status_id)
      REFERENCES status (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE jobs OWNER TO job_manager;
