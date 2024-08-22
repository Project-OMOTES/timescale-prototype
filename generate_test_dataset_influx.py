import datetime
import random
import uuid

NUM_OF_ASSETS = 250
KPIs = ["HeatIn_Q1", "Heat_flow1", "PostProc_Velocity1", "HeatIn_Q2", "Heat_flow2", "PostProc_Velocity2", "HeatIn_Q3", "Heat_flow3", "PostProc_Velocity3", "HeatIn_Q4"]
START_DATETIME = datetime.datetime.fromisoformat('2020-01-01T00:00:00+00:00')
END_DATETIME = datetime.datetime.fromisoformat('2021-01-01T00:00:00+00:00')
RESOLUTION = datetime.timedelta(minutes=15)

CARRIER_ID = uuid.uuid4()
SIMULATION_RUN_ID = uuid.uuid4()

esdl_id = uuid.uuid4()
asset_ids = [uuid.uuid4() for _ in range(0, NUM_OF_ASSETS)]

with open(f'test_dataset.influx_inline', 'w+') as open_dataset_file:
    open_dataset_file.write("""# DDL
CREATE DATABASE energy_profiles

# DML
# CONTEXT-DATABASE: energy_profiles
""")

    current_time = START_DATETIME
    while current_time < END_DATETIME:
        next_time = current_time + RESOLUTION

        if next_time >= END_DATETIME:
            end_line = ';\n'
        else:
            end_line = ',\n'
        for asset_i, asset_id in enumerate(asset_ids):
            open_dataset_file.write(
                f"{CARRIER_ID},assetId={asset_id},assetClass={random.choice(['HeatingDemand', 'Pipe', 'ResidualHeatSource'])},assetName=Asset\\ {asset_i},capability={random.choice(['Consumer', 'Transport', 'Producer'])},simulationRun={SIMULATION_RUN_ID},simulation_type=EndScenarioSizingDiscountedStagedHIGHS {','.join([f'{kpi}={random.uniform(0, 10)}' for kpi in KPIs])} {round(current_time.timestamp() * 10**9)}\n")
        current_time = next_time
