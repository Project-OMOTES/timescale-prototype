\connect esdl_profiles
set schema 'esdl_profiles_v1';

GRANT ALL PRIVILEGES ON DATABASE esdl_profiles TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA esdl_profiles_v1 TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA esdl_profiles_v1 TO postgres;
