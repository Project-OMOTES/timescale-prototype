import datetime
import random
import uuid

NUM_OF_ASSETS = 250
KPIs = ["HeatIn_Q1", "Heat_flow1", "PostProc_Velocity1", "HeatIn_Q2", "Heat_flow2", "PostProc_Velocity2", "HeatIn_Q3", "Heat_flow3", "PostProc_Velocity3", "HeatIn_Q4"]
START_DATETIME = datetime.datetime.fromisoformat('2020-01-01T00:00:00+00:00')
END_DATETIME = datetime.datetime.fromisoformat('2021-01-01T00:00:00+00:00')
RESOLUTION = datetime.timedelta(minutes=15)


esdl_id = uuid.uuid4()
asset_ids = [uuid.uuid4() for _ in range(0, NUM_OF_ASSETS)]

with open(f'timescaledb-init/0_{esdl_id}_init.sql', 'w+') as open_init_file:
    open_init_file.write(f'''\\connect esdl_profiles

CREATE SCHEMA "esdl_profiles_v1__{esdl_id}";
set schema 'esdl_profiles_v1__{esdl_id}';

CREATE TYPE asset_class_type AS ENUM ('HeatingDemand', 'ResidualHeatSource', 'Pipe');
CREATE TYPE asset_capability_type AS ENUM ('Consumer', 'Producer', 'Transport');
''')

with open(f'timescaledb-init/{esdl_id}_metadata.sql', 'w+') as open_metadata_file:
    open_metadata_file.write(f'''\\connect esdl_profiles
    
set schema 'esdl_profiles_v1__{esdl_id}';

CREATE TABLE "metadata" (
    name TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO "metadata" (name, value) VALUES
    ('simulationRun', '{uuid.uuid4()}'),
    ('simulation_type', 'EndScenarioSizingDiscountedStagedHIGHS');
''')


with open(f'timescaledb-init/{esdl_id}_asset_metadata.sql', 'w+') as open_asset_metadata_file:
    open_asset_metadata_file.write(f'''\\connect esdl_profiles
    
set schema 'esdl_profiles_v1__{esdl_id}';

CREATE TABLE "asset_metadata" (
    asset_id TEXT PRIMARY KEY,
    asset_class asset_class_type NOT NULL,
    asset_name TEXT NOT NULL,
    asset_capability asset_capability_type NOT NULL,
    carrier_id TEXT NOT NULL
);

INSERT INTO "asset_metadata" VALUES
''')

    for asset_i, asset_id in enumerate(asset_ids):
        if asset_i == len(asset_ids) - 1:
            end_line = ';\n'
        else:
            end_line = ',\n'

        open_asset_metadata_file.write(f"    ('{asset_id}', '{random.choice(['HeatingDemand', 'Pipe', 'ResidualHeatSource'])}', 'Asset {asset_i}', '{random.choice(['Consumer', 'Transport', 'Producer'])}', '{uuid.uuid4()}'){end_line}")


with open(f'timescaledb-init/{esdl_id}_profiles.sql', 'w+') as open_profiles_file:
    open_profiles_file.write(f'''\\connect esdl_profiles

    set schema 'esdl_profiles_v1__{esdl_id}';
''')

    for kpi in KPIs:
        for asset_i, asset_id in enumerate(asset_ids):
                open_profiles_file.write(f'''CREATE TABLE "{asset_id}_{kpi}" (
        time TIMESTAMPTZ,
        value REAL
    );
    
    
    INSERT INTO "{asset_id}_{kpi}" VALUES
    ''')

                current_time = START_DATETIME
                while current_time < END_DATETIME:
                    next_time = current_time + RESOLUTION

                    if next_time >= END_DATETIME:
                        end_line = ';\n'
                    else:
                        end_line = ',\n'

                    open_profiles_file.write(f"    ('{current_time.isoformat(sep=' ')}', {random.uniform(0, 10)}){end_line}")
                    current_time = next_time
