\connect esdl_profiles
    
set schema 'esdl_profiles_v1';

CREATE TABLE "71067404-fd66-4a5b-ac1d-d392bab89a6f_metadata" (
    name TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO "71067404-fd66-4a5b-ac1d-d392bab89a6f_metadata" (name, value) VALUES
    ('simulationRun', '3913fcd5-6ba1-4c68-9b3c-d2e9524e19f5'),
    ('simulation_type', 'EndScenarioSizingDiscountedStagedHIGHS');
