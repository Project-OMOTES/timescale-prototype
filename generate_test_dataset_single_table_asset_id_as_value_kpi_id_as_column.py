import datetime
import random
import uuid

NUM_OF_ASSETS = 250
KPIs = ["HeatIn.Q1", "Heat_flow1", "PostProc.Velocity1", "HeatIn.Q2", "Heat_flow2", "PostProc.Velocity2", "HeatIn.Q3", "Heat_flow3", "PostProc.Velocity3", "HeatIn.Q4"]
START_DATETIME = datetime.datetime.fromisoformat('2020-01-01T00:00:00+00:00')
END_DATETIME = datetime.datetime.fromisoformat('2021-01-01T00:00:00+00:00')
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
    {',\n    '.join(f'"{kpi}" real' for kpi in KPIs)}
);

''')

    def write_insert(rows_):
        if rows_:
            open_profiles_file.write(f'INSERT INTO "{esdl_id}_profiles" VALUES\n')

            for row_i, row in enumerate(rows_):
                if row_i == len(rows_) - 1:
                    end_line = ';\n'
                else:
                    end_line = ',\n'
                open_profiles_file.write(f"    {row}{end_line}")

    rows = []
    for asset_i, asset_id in enumerate(asset_ids):
        current_time = START_DATETIME
        while current_time < END_DATETIME:
            rows.append(f"('{current_time.isoformat(sep=' ')}', '{asset_id}', {', '.join(str(random.uniform(0, 10)) for _ in KPIs)})")
            current_time += RESOLUTION

            if len(rows) % 1000 == 0:
                write_insert(rows)
                rows = []

    write_insert(rows)
