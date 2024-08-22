CREATE DATABASE esdl_profiles WITH OWNER postgres;

\connect esdl_profiles

CREATE EXTENSION timescaledb;

CREATE SCHEMA "esdl_profiles_v1";
set schema 'esdl_profiles_v1';

CREATE TYPE asset_class_type AS ENUM ('HeatingDemand', 'ResidualHeatSource', 'Pipe');
CREATE TYPE asset_capability_type AS ENUM ('Consumer', 'Producer', 'Transport');
