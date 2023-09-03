-- Database: StudentTemplateDB

-- DROP DATABASE IF EXISTS "StudentTemplateDB";

CREATE DATABASE "StudentTemplateDB"
    WITH
    OWNER = master
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "StudentTemplateDB"
    IS 'Midtown Tech Hub e-Commerce Web Template Database for Students';