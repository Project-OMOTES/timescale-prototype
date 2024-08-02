\connect esdl_profiles
    
set schema 'esdl_profiles_v1';

CREATE TABLE "71067404-fd66-4a5b-ac1d-d392bab89a6f_asset_metadata" (
    asset_id TEXT PRIMARY KEY,
    asset_class asset_class_type NOT NULL,
    asset_name TEXT NOT NULL,
    asset_capability asset_capability_type NOT NULL,
    carrier_id TEXT NOT NULL
);

INSERT INTO "71067404-fd66-4a5b-ac1d-d392bab89a6f_asset_metadata" VALUES
    ('174e0299-e888-4fb5-8f86-ff487d303030', 'HeatingDemand', 'Asset 0', 'Producer', '35ae20d9-098a-43ab-9d9f-aae917c720a8'),
    ('913c791a-bf56-43d1-bba2-05025a8f305b', 'ResidualHeatSource', 'Asset 1', 'Consumer', '0bbb46c6-2c92-4714-857d-1cfaec72ed5c'),
    ('c8b9279d-e10f-4e68-a1e8-21c6ec296b0c', 'HeatingDemand', 'Asset 2', 'Consumer', '680d37e7-9094-41bc-9a53-4a93ab5722df'),
    ('5e75b742-6c23-4d6f-8add-f6fcf8799d61', 'ResidualHeatSource', 'Asset 3', 'Producer', '08790b09-ff75-440a-bd9a-d02564667c7f'),
    ('5eea34a6-46a3-4674-84cb-28ed3e2e00a9', 'Pipe', 'Asset 4', 'Consumer', 'd4d4d522-dd70-4d55-b6ec-bd20e86c4eae'),
    ('75c8dc5a-8494-4f7a-9f8d-b31d7653ce1e', 'ResidualHeatSource', 'Asset 5', 'Producer', 'cc164fc8-8136-4a88-a53c-19654496498e'),
    ('00a4e211-d0f7-4d93-8736-e80ab9bd78cc', 'ResidualHeatSource', 'Asset 6', 'Producer', '0ba14a04-fda3-4b69-a6d6-bd10fe77773c'),
    ('d921dd1b-218a-45be-912e-f7aa67e558d0', 'HeatingDemand', 'Asset 7', 'Producer', 'efdbd39d-609d-4c1d-88a7-f0cf3cb7ca45'),
    ('5eba73e0-0916-4f33-975c-27422c576311', 'Pipe', 'Asset 8', 'Transport', '0d6988e3-2b86-4d7f-8ca0-c120461e9785'),
    ('10c67c40-f5e5-4171-9fb3-405b142c86a9', 'ResidualHeatSource', 'Asset 9', 'Consumer', '240f90fa-f3a3-4f54-8e69-b36efd89b9f1');
