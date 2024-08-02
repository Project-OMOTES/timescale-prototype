import datetime
import random
import uuid

NUM_OF_ASSETS = 10
KPIs = ["HeatIn.Q1", "Heat_flow1", "PostProc.Velocity1", "HeatIn.Q2", "Heat_flow2", "PostProc.Velocity2"]
START_DATETIME = datetime.datetime.fromisoformat('2020-01-01T00:00:00+00:00')
END_DATETIME = datetime.datetime.fromisoformat('2020-01-01T03:00:00+00:00')
RESOLUTION = datetime.timedelta(minutes=15)


esdl_id = uuid.uuid4()
asset_ids = [uuid.uuid4() for _ in range(0, NUM_OF_ASSETS)]

with open(f'timescaledb-init/{esdl_id}_metadata.sql', 'w+') as open_metadata_file:
    open_metadata_file.write(f'''\\connect esdl_profiles
    
set schema 'esdl_profiles_v1';

CREATE TABLE "{esdl_id}_metadata" (
    name TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO "{esdl_id}_metadata" (name, value) VALUES
    ('simulationRun', '{uuid.uuid4()}'),
    ('simulation_type', 'EndScenarioSizingDiscountedStagedHIGHS');
''')


with open(f'timescaledb-init/{esdl_id}_asset_metadata.sql', 'w+') as open_asset_metadata_file:
    open_asset_metadata_file.write(f'''\\connect esdl_profiles
    
set schema 'esdl_profiles_v1';

CREATE TABLE "{esdl_id}_asset_metadata" (
    asset_id TEXT PRIMARY KEY,
    asset_class asset_class_type NOT NULL,
    asset_name TEXT NOT NULL,
    asset_capability asset_capability_type NOT NULL,
    carrier_id TEXT NOT NULL
);

INSERT INTO "{esdl_id}_asset_metadata" VALUES
''')

    for asset_i, asset_id in enumerate(asset_ids):
        if asset_i == len(asset_ids) - 1:
            end_line = ';\n'
        else:
            end_line = ',\n'

        open_asset_metadata_file.write(f"    ('{asset_id}', '{random.choice(['HeatingDemand', 'Pipe', 'ResidualHeatSource'])}', 'Asset {asset_i}', '{random.choice(['Consumer', 'Transport', 'Producer'])}', '{uuid.uuid4()}'){end_line}")


with open(f'timescaledb-init/{esdl_id}_profiles.sql', 'w+') as open_profiles_file:
    open_profiles_file.write(f'''\\connect esdl_profiles
    
set schema 'esdl_profiles_v1';
    
CREATE TABLE "{esdl_id}_profiles" (
    time TIMESTAMPTZ,
    asset_id TEXT,
    {'\n    '.join(f'"{kpi}" real,' for kpi in KPIs)}
    PRIMARY KEY (time, asset_id)
);

SELECT public.create_hypertable('{esdl_id}_profiles', public.by_range('time', INTERVAL '1 year'));

INSERT INTO "{esdl_id}_profiles" VALUES
''')

    for asset_i, asset_id in enumerate(asset_ids):
        current_time = START_DATETIME
        while current_time < END_DATETIME:
            next_current_time = current_time + RESOLUTION

            if next_current_time >= END_DATETIME:
                end_line = ''
            else:
                end_line = ',\n'

            open_profiles_file.write(f"    ('{current_time.isoformat(sep=' ')}', '{asset_id}', {', '.join(str(random.uniform(0, 10)) for _ in KPIs)}){end_line}")
            current_time = next_current_time

        if asset_i == len(asset_ids) - 1:
            open_profiles_file.write(';\n')
        else:
            open_profiles_file.write(',\n')



