
# Connection details
- Username: `postgres`
- Database: `postgres`
- Password: `password`


# InfluxDB structure to mimic
- Database: <output_esdl_id>
  - Measurements: <carrier_id> (both return & supply carriers)
    - Time column
    - Field keys: key == name of KPI and specific types. These columns are dynamic and may not have a value for every timestamp! Example:
      - HeatIn.Q: nullable float
      - Heat_flow: nullable float
      - PostProc.Velocity: nullable float
    - Tag keys:
      - assetId: str
      - assetClass: enum[HeatingDemand, ResidualHeatSource, Pipe] <-- Is always the same per assetId. Perhaps add an asset metadata normal SQL table? <-- Why does this exist? Shouldn't this just be retrieved from the ESDL?
      - assetName: str <-- Is always the same per assetId. Perhaps add an asset metadata normal SQL table? <-- Why does this exist? Shouldn't this just be retrieved from the ESDL?
      - capability: enum[Consumer, Producer, Transport] <-- Is always the same per assetId. Perhaps add an asset metadata normal SQL table? <-- Why does this exist? Shouldn't this just be retrieved from the ESDL?
      - simulationRun: str <-- Constant per output esdl. Perhaps add in a separate metadata normal SQL table? <-- Why does this exist? Shouldn't this just be retrieved from the ESDL? 
      - simulation_type: str <-- Constant per output esdl. Perhaps add in a separate metadata normal SQL table? <-- Why does this exist? Shouldn't this just be retrieved from the ESDL? 

- Time + AssetId makes a unique row.
- A asset is only available within a single carrier_id.

See also in the excerpt duplicate rows on time for different assets


Excerpt:
```bash
root@90ae1fc1e846:/# influx -host localhost -port 8096 -username root -password '9012' -database '1ec54487-a62d-41a7-9489-7282b1333b68' -execute 'SHOW MEASUREMENTS;'
name: measurements
name
----
9f6aeb1a-138b-4bb9-9a09-d524e94658e6
9f6aeb1a-138b-4bb9-9a09-d524e94658e6_ret

root@90ae1fc1e846:/# influx -host localhost -port 8096 -username root -password '9012' -database '1ec54487-a62d-41a7-9489-7282b1333b68' -execute 'SHOW FIELD KEYS;'
name: 9f6aeb1a-138b-4bb9-9a09-d524e94658e6
fieldKey          fieldType
--------          ---------
HeatIn.Q          float
Heat_flow         float
PostProc.Velocity float

name: 9f6aeb1a-138b-4bb9-9a09-d524e94658e6_ret
fieldKey          fieldType
--------          ---------
HeatIn.Q          float
Heat_flow         float
PostProc.Velocity float


root@90ae1fc1e846:/# influx -host localhost -port 8096 -username root -password '9012' -database '1ec54487-a62d-41a7-9489-7282b1333b68' -execute 'Select * from "9f6aeb1a-138b-4bb9-9a09-d524e94658e6" limit 100;'
name: 9f6aeb1a-138b-4bb9-9a09-d524e94658e6
time                HeatIn.Q               Heat_flow          PostProc.Velocity     assetClass         assetId                              assetName               capability simulationRun                        simulation_type
----                --------               ---------          -----------------     ----------         -------                              ---------               ---------- -------------                        ---------------
1546297200000000000 0.00030697297792970957 0                                        HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0006577702542100457  152611.6488508306                        ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0002549774908736195  0                                        HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0006577702542100457  218358.67574960046 0.03259247220144119   Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.00030697297792970957 59764.0175318304   0.003997187341926258  Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0005619504688033291  162935.594840618   0.0046137784147355495 Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0000958197854067166  0                                        HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0002549774908736195  84644.367690332    0.002093440096493371  Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0000958197854067166  31809.10252189359  0.0012476982043074791 Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.0066065297462114874  2193156.466790333  0.05424154980115627   Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.0087172933410908     2893862.4358552275 0.11351049474734193   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.008928446533613792   1431026.6666666667                       HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.015534976279825278   5133501.027273953  0.1275467184606467    Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.008928446533613792   2921817.350865164  0.11625998388496069   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.0066065297462114874  1054256.0495500003                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.024252269620916082   4068921.0317341643                       ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.0087172933410908     1431026.6666666667                       HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.024252269620916082   8050977.44151627   1.201698341301327     Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.010183185946247942   1639293.3333333333                       HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.027014591313267958   4527422.235517498                        ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.010183185946247942   3338350.6841984973 0.13259832262546586   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.00997203275372495    3310395.7691885605 0.1298488334878471    Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.006859372613295061   2277092.207690333  0.05631746400931456   Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.017042558559543005   5633970.101507286  0.1399244118104031    Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.027014591313267958   8967979.849082936  1.338571196820675     Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.00997203275372495    1639293.3333333333                       HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.006859372613295061   1096223.9200000002                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.009150234979086456   1467840                                  HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.025564588288076777   4286744.933384164                        ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.007475271522426866   1198453.2845333335                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.025564588288076777   8486625.244816272  1.2667236436848077    Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.009150234979086456   2995444.0175318317 0.11914795784543038   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.016625506501513322   5495522.163907288  0.1365002919101992    Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.008939081786563455   1467840                                  HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.007475271522426866   2481550.936757     0.06137417496582059   Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.008939081786563455   2967489.1025218936 0.11639846870781148   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.00840373526391199    2789771.1880903332 0.06899713500792332   Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.011302763426560884   3752155.7691885605 0.14717667725066452   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.011513916619083882   1860173.3333333333                       HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.019917651882995872   6588409.081907286  0.16352977251834055   Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.011513916619083882   3780110.6841984983 0.14992616638828338   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.00840373526391199    1352563.4102000003                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.03122041530955676    5225521.725717499                        ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.011302763426560884   1860173.3333333333                       HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.03122041530955676    10364178.829482937 1.5469694951715516    Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.010698336000871672   1724799.9999999998                       HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.029995262277537595   5022165.92485083                         ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.008809743468317232   1419954.2760000003                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.029995262277537595   9957467.2277496    1.4862632441925512    Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.010698336000871672   3509364.0175318285 0.13930624620695484   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.019508079469188904   6452444.146840618  0.16016706269425626   Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.010487182808348686   1724799.9999999998                       HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.008809743468317232   2924552.9196903333 0.0723305816258779    Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.010487182808348686   3481409.102521893  0.13655675706933615   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.008815309101149313   2926400.531690333  0.0723762771062637    Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.010381148491788054   3446209.102521893  0.13517605238703995   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.029788759277248417   9888914.8397496    1.4760310343086878    Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.029788759277248417   4987889.73085083                         ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.010592301684311047   1707199.9999999998                       HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.008815309101149313   1420878.0820000002                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.010381148491788054   1707199.9999999998                       HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.010592301684311047   3474164.01753183   0.13792554152465872   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.01940761078546036    6419091.758840618  0.15934218528943664   Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.0112983096225002     3732150.039144219  0.14711868293033428   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.020111333575683447   6676319.184453008  0.16511995610685912   Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.03148302319425247    5269110.432850831                        ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.011371689618569016   3751423.080909505  0.14807418589810376   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.008813023953183244   2925641.935690333  0.07235751537022889   Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.03148302319425247    10451356.243749602 1.559981698333738     Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.011371689618569016   1848000                                  HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.0112983096225002     1848000                                  HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.008813023953183244   1420498.7840000002                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.011334541900235473   1830400                                  HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.00879436396185878    1417401.5240000002                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.01112338870771248    3692609.1025218936 0.14484098516311342   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.020128905862094253   6658538.642840619  0.16526422973992927   Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.011334541900235473   3720564.01753183   0.1475904743007322    Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.031252294569806736   5230813.172850831                        ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.01112338870771248    1830400                                  HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.00879436396185878    2919447.4156903336 0.07220431136031802   Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.031252294569806736   10374761.7237496   1.5485491103895546    Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.008789252649925099   2917750.6236903337 0.0721623459879591    Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.03930579131648111    13048264.931749603 1.947599336757138     Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.024153098579464596   7994441.850840619  0.19830403400537824   Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.008789252649925099   1416553.1280000003                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.015363845929539495   2499200                                  HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.015152692737016511   5030209.102521894  0.19730776309036946   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.015152692737016511   2499200                                  HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.015363845929539495   5058164.017531829  0.20005725222798812   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.03930579131648111    6567564.776850829                        ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.01702416271677624    5632950.039144533  0.22167673577435434   Pipe               Pipe5                                Pipe5                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.04291209277927272    7166153.118850832                        ResidualHeatSource 72d74fb5-134f-4bfb-829e-220ab76a8a7b ResidualHeatSource_72d7 Producer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.008790387349655194   1416741.4700000002                       HeatingDemand      8fbe3d4e-5d5b-4489-9271-9969c2b9e589 HeatingDemand_8fbe      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.04291209277927272    14245441.615749605 2.126291333580878     Pipe               Pipe1                                Pipe1                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.008790387349655194   2918127.3076903336 0.07217166220604691   Pipe               Pipe3                                Pipe3                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.025814550066431435   8569604.556453321  0.21194503874378817   Pipe               Pipe2                                Pipe2                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.017097542712841276   2798400                                  HeatingDemand      b0ff0df6-4a47-43a5-a0a5-aa10975c0a5c HeatingDemand_b0ff      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.01702416271677624    2798400                                  HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.017097542712841276   5652223.080909191  0.22263223874207458   Pipe               Pipe4                                Pipe4                   Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548050400000000000 0.019605218591964794   3203199.9999999995                       HeatingDemand      08fd3385-681a-4211-a083-51775cc99daa HeatingDemand_08fd      Consumer   544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS



root@90ae1fc1e846:/# influx -host localhost -port 8096 -username root -password '9012' -database '1ec54487-a62d-41a7-9489-7282b1333b68' -execute 'Select * from "9f6aeb1a-138b-4bb9-9a09-d524e94658e6_ret" limit 100;'
name: 9f6aeb1a-138b-4bb9-9a09-d524e94658e6_ret
time                HeatIn.Q               Heat_flow          PostProc.Velocity     assetClass assetId   assetName capability simulationRun                        simulation_type
----                --------               ---------          -----------------     ---------- -------   --------- ---------- -------------                        ---------------
1546297200000000000 0.0006577702542100457  74924.81403935658  0.03259247220144119   Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.00030697297792970957 50952.602768684905 0.003997187341926258  Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0005619504688033291  72781.6995793227   0.0046137784147355495 Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0000958197854067166  15904.55126094845  0.0012476982043074791 Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546297200000000000 0.0002549774908736195  42322.18384516685  0.002093440096493371  Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.0087172933410908     1446931.2179276152 0.11351049474734193   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.0066065297462114874  1096578.2333951674 0.05424154980115627   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.024252269620916082   3991234.1969226906 1.201698341301327     Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.015534976279825278   2558064.41579599   0.1275467184606467    Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1546729200000000000 0.008928446533613792   1481979.2694353515 0.11625998388496069   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.027014591313267958   4449735.400706023  1.338571196820675     Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.010183185946247942   1690245.9361020185 0.13259832262546586   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.00997203275372495    1655197.884594282  0.1298488334878471    Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.006859372613295061   1138546.1038451674 0.05631746400931456   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547161200000000000 0.017042558559543005   2808298.9529126566 0.1399244118104031    Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.025564588288076777   4209058.098572694  1.2667236436848077    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.009150234979086456   1518792.6027686861 0.11914795784543038   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.016625506501513322   2739074.984112658  0.1365002919101992    Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.008939081786563455   1483744.5512609484 0.11639846870781148   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1547593200000000000 0.007475271522426866   1240775.4683785008 0.06137417496582059   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.011302763426560884   1876077.8845942817 0.14717667725066452   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.00840373526391199    1394885.5940451678 0.06899713500792332   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.03122041530955676    5147834.890906025  1.5469694951715516    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.019917651882995872   3285518.443112658  0.16352977251834055   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548025200000000000 0.011513916619083882   1911125.9361020192 0.14992616638828338   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.029995262277537595   4944479.090039355  1.4862632441925512    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.010698336000871672   1775752.6027686833 0.13930624620695484   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.019508079469188904   3217535.975579322  0.16016706269425626   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.010487182808348686   1740704.5512609482 0.13655675706933615   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548028800000000000 0.008809743468317232   1462276.4598451676 0.0723305816258779    Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.010381148491788054   1723104.5512609484 0.13517605238703995   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.008815309101149313   1463200.2658451672 0.0723762771062637    Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.010592301684311047   1758152.6027686845 0.13792554152465872   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.029788759277248417   4910202.8960393565 1.4760310343086878    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548032400000000000 0.019407610785460362   3200859.7815793236 0.15934218528943667   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.03148302319425247    5191423.598039357  1.559981698333738     Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.020111333575683447   3317666.505191712  0.16511995610685912   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.008813023953183244   1462820.9678451675 0.07235751537022889   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.011371689618569016   1887518.5296485594 0.14807418589810376   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548036000000000000 0.0112983096225002     1875338.6243810733 0.14711868293033428   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.01112338870771248    1846304.5512609482 0.14484098516311342   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.011334541900235473   1881352.6027686845 0.1475904743007322    Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.020128905862094253   3320583.2235793234 0.16526422973992927   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.031252294569806736   5153126.338039356  1.5485491103895546    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548039600000000000 0.00879436396185878    1459723.7078451677 0.07220431136031802   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.03930579131648111    6489877.942039357  1.947599336757138     Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.008789252649925099   1458875.3118451675 0.0721623459879591    Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.015363845929539495   2550152.6027686833 0.20005725222798812   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.015152692737016511   2515104.551260948  0.19730776309036946   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548043200000000000 0.024153098579464596   3988534.8275793223 0.19830403400537824   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.017097542712841276   2837918.5296482462 0.22263223874207458   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.025814550066431435   4264309.191192026  0.21194503874378817   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.008790387349655194   1459063.6538451675 0.07217166220604691   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.04291209277927272    7088466.284039358  2.126291333580878     Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548046800000000000 0.01702416271677624    2825738.6243813876 0.22167673577435434   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548050400000000000 0.04778542308821815    7897361.142039358  2.367764525179512     Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548050400000000000 0.019605218591964794   3254152.602768684  0.2552854395198366    Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548050400000000000 0.02839135768877634    4692018.027579322  0.23310138622796794   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548050400000000000 0.019394065399441805   3219104.551260948  0.2525359503822179    Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548050400000000000 0.008786139096811547   1458358.5118451677 0.0721367828023299    Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548054000000000000 0.01900616041093318    3154718.529648333  0.24748492302341318   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548054000000000000 0.00889041110868109    1475665.9974633218 0.07299288664836676   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548054000000000000 0.01882115995977409    3124011.414763143  0.24507597658581146   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548054000000000000 0.04671773147938838    7720141.4180393545 2.3148604772117487    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548054000000000000 0.027711571068455187   4579184.325191936  0.22752013839638824   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548057600000000000 0.04735473058773617    7825873.0780393565 2.3464237405218262    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548057600000000000 0.028172733821415635   4655729.963579324  0.23130642005893384   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548057600000000000 0.009033470911959648   1499411.63585071   0.07416744965529598   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548057600000000000 0.019181996766320538   3183904.5512609477 0.24977454101762545   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548057600000000000 0.019139262909455987   3176811.4147631424 0.2492180906327001    Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548061200000000000 0.016531138852304728   2743904.551260948  0.21525692396022014   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548061200000000000 0.016742292044827713   2778952.602768683  0.21800641309783883   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548061200000000000 0.025514431262132802   4214494.2715793215 0.20948097520438413   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548061200000000000 0.04204557011443753    6944637.386039355  2.0833551933635355    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548061200000000000 0.008772139217305087   1456034.7558451674 0.07202183967929389   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548064800000000000 0.03949689661578707    6521598.364039358  1.95706859158481      Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548064800000000000 0.008879909771203454   1473922.943463434  0.07290666758303997   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548064800000000000 0.015215993196712595   2525611.414763143  0.19813201738774033   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548064800000000000 0.015400993647871022   2556318.529648224  0.20054096382533343   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548064800000000000 0.024095902967916052   3979041.271192048  0.19783444123407543   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548068400000000000 0.01381047889946289    2292318.5296484483 0.17983039359090788   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548068400000000000 0.02246779609014335    3708801.5791918244 0.18446720553170762   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548068400000000000 0.008730697186747925   1449156.0418451673 0.07168158843534597   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548068400000000000 0.036278274989606236   5987358.672039358  1.7975861047942814    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548068400000000000 0.013737098903395422   2280138.6243811855 0.17887489062315595   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548072000000000000 0.034123377553708804   5629680.176039358  1.6908110806472998    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548072000000000000 0.012676755737789236   2104138.6243812083 0.16506784380019562   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548072000000000000 0.02137324181985237    3527123.0831918474 0.17548059346111153   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548072000000000000 0.012750135733856426   2116318.529648425  0.16602334676794395   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548072000000000000 0.008696486082063136   1443477.5458451675 0.07140070521680349   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548075600000000000 0.01228976618987944    2039904.5512609486 0.16002873666837178   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548075600000000000 0.008662938704002601   1437909.2178451675 0.07112527138880745   Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548075600000000000 0.012500919382402425   2074952.602768684  0.16277822580599047   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548075600000000000 0.03345362427628447    5518511.848039357  1.6576248504452478    Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548075600000000000 0.021163858086405026   3492368.733579323  0.17376149150567888   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548079200000000000 0.03598208829691296    5938196.420039356  1.782910073936614     Pipe       Pipe1_ret Pipe1_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548079200000000000 0.022277643714011655   3677239.327191981  0.18290599866880503   Pipe       Pipe2_ret Pipe2_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548079200000000000 0.008646579127175919   1435193.7898451677 0.0709909544576411    Pipe       Pipe3_ret Pipe3_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548079200000000000 0.013704444582901305   2274718.52964829   0.17844968890859925   Pipe       Pipe4_ret Pipe4_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS
1548079200000000000 0.013631064586835735   2262538.6243813424 0.17749418594087205   Pipe       Pipe5_ret Pipe5_ret Transport  544364f5-31a9-4ff2-b1c4-86a09be1fa9b EndScenarioSizingDiscountedStagedHIGHS

```

Comments:
- Be aware that id may be any uuid-like string and can contain [a-z,A-Z,0-9,-]




# ESDL timescale profile proposal

## Inherited
- id : EString (GenericProfile)
- name : EString (GenericProfile)
- profileType : ProfileTypeEnum (GenericProfile) - (deprecated in future version, to be replaced with Quantity and Units)
- interpolationMethod : InterpolationMethodEnum (GenericProfile) - Type of interpolation between elements in the profile.
- host : EString (DatabaseProfile)
- port : EInt (DatabaseProfile)
- database : EString (DatabaseProfile)
- filters : EString (DatabaseProfile) - Raw string that can be communicated as the WHERE clause of the query
- startDate : EDate (ExternalProfile)
- endDate : EDate (ExternalProfile)
- multiplier : EDouble (ExternalProfile) - A multiplier can be used to scale the supplied external profile by a certain factor (e.g. when using NEDU profiles).

Proposal is to set database to a constant for TimescaleDB profiles across ESDL.

## Added
- schema <-- Perhaps the value of schema should be the format_version? (for example, enums are
  created in the scope of a schema and may differ across format versions.)
- table
- format_version <-- Proposal is to add this to DatabaseProfile as all database profiles should 
  define this version. Goal of this field is to add an identifier on which sets of queries should
  work on the format that is detached from ESDL version (as a single ESDL version may work with
  multiple format_versions and one format_version may work in multiple ESDL versions).


# Standard access patterns
ESDL profiles are a 'write once' / 'read many' (WORM) type of data structure.
We should therefore mostly optimize for queries as writes happen very little.

Type of current queries:

- Datastructure should allow all (KPI) profiles of an ESDL to exist in multiple format versions.
- An ESDL will reference a single profile consisting of all measurements for 1 KPI/profile column within a single carrier for a single asset.
  - Profiles are written per KPI/profile column, per carrier per asset
  - Profiles are read per KPI/profile column, per carrier per asset

Future, expected queries:
- Query multiple profiles within the same timespan within the same ESDL.
- Query the same (couple of) profiles across ESDLs to compare scenarios.
- Query for multiple years, but aggregate to time buckets of days
- Query for a week, but keep data as detailed as possible.

  
# Considerations
- Basic system admin maintenance (auto vacuum should be fine): https://www.timescale.com/learn/how-to-reduce-bloat-in-large-postgresql-tables
- Hypertables are chunked: https://docs.timescale.com/use-timescale/latest/hypertables/about-hypertables/
  - They are chunked per default on the time column. We must make sure to limit the amount of chunks
    that are hit by a query or else TimescaleDB will continuously swap chunks in and out.
  - Chunk size may be set per hypertable: https://docs.timescale.com/use-timescale/latest/hypertables/change-chunk-intervals/#change-the-chunk-interval-length-when-creating-a-hypertable
- PostgreSQL partitioning is taken care of automatically.
  - Partitioning is to group data together within a table so it is easy to delete in 1 go or to 
    limit the amount of data that is read into memory for a query (if the query is scoped to only 
    that partition).
  - Partioning & chunked work together. If the chunks are proper, we shouldn't have to care about
    partitions. https://www.reddit.com/r/PostgreSQL/comments/t6pbqa/comment/hzyz97q/
- Proper indexing for hypertables: https://docs.timescale.com/use-timescale/latest/schema-management/about-indexing/
- ESDL may have multiple versions, but there also may be multiple versions of this format.
  - This is especially useful to update enums. Enums are created within the scope of a schema.

## Authorization & authentication
We expect that access is granted on a minimum of 'per-ESDL' profiles. In other words,
 a user will receive access for ALL profiles within an ESDL or no access at all. We must
ensure that the authorization model can give access at least on a per schema basis.
We also expect that both read and write privileges should be given separately.

In practice for the time being, we expect that a single user with both read and write privileges
to all ESDLs is enough. But the chosen structure should support the per-ESDL requirement.

As such, we expect:

- PostgreSQL allows authorization on a per-table and per-schema basis. Therefore, creating a 
a separate user with limited access to a selection of ESDLs is possible with the proposed database
structure as a single ESDL maps to 3 separate tables.

# Proposed database structure
PostgreSQL utilizes both the database & schema grouping mechanism. A table exists within
a schema which exists within a database. 

- Database: constant name: esdl_profiles
  - Schema: format_version of the schema used.
    - Per ESDL:
      - Table for metadata: <esdl_id>_metadata    This is the equivalent of adding an arbitrary tag in influxdb that is constant for the whole profile. <-- Why does this exist? Shouldn't this just be retrieved from the ESDL?
        - Columns (which are mostly dynamic!):
          - name: str <-- primary key e.g. simulation_run or simulation_type 
          - value: str
      - Table for asset metadata: <esdl_id>_asset_metadata  This is the equivalent of adding an arbitrary tag in influxdb that is constant per asset in the profile. <-- Why does this exist? Shouldn't this just be retrieved from the ESDL?
        - Columns:
          - asset_id (primary key)
          - asset_class: enum[HeatingDemand, ResidualHeatSource, Pipe]
          - asset_name: str
          - capability: enum[Consumer, Producer, Transport]
          - carrier_id: str
      - Hypertable for profiles: <esdl_id>_profiles   This is the equivalent of all values for each profile in influxdb.
        - Chunk interval:
        - Dimensions:
        - Columns (which are mostly dynamic!):
          - time (primary key)  <-- always there
          - asset_id (primary key) <-- always there
          - HeatIn.Q: nullable float <-- dynamic, example
          - Heat_flow: nullable float <-- dynamic, example
          - PostProc.Velocity: nullable float <-- dynamic, example
          - ... other dynamic columns




## Retention
It is important to be able to remove unneeded data from the database. Due to the chosen format,
there is a neat package of 3 tables that describe a single ESDL. Removing the data for a single
ESDL would entail removing all 3 tables.

While 1 table is a hypertable, setting a retention policy would remove the data but not the table.
Also it would operate per chunk and we have chosen to keep all data for up to 10 years in a single
chunk. A retention policy in Timescaledb would remove old data on a per-chunk basis. 

The 2 other tables are normal SQL table and they require a manual `DROP TABLE` operation.

Therefore, retention should be handled manually. The ESDL package should provide an easy
'delete profiles for ESDL' operation that removes the 3 tables for a single ESDL from the
database.

## Scaling
Why use a single table for all profiles instead of having a hypertable per kpi?
Otherwise we would have to write joins or create multiple queries to group results together in the 
case of a graph which shows multiple assets. TimescaleDB allows for segmentation & ordering on
compression & we can add an index to help the hypertable for single asset and/or single carrier
queries while still having the flexibility of querying multiple assets with a single query.
It also prevents many chunks from being created as all profiles are kept together in the same chunk.
Each chunk will host data for ~1 year (perhaps a couple). Assuming a double precision (8 bytes) is used for
15 minute intervals, we would expect ~35.040 data points per profile per asset per year which amounts to
~275 KB per profile per asset per year of data. Also we need to account for the asset id which is
32 bytes and the datetime which is 8 bytes, both per data point. This equals to 1,34MB per asset per year.
TimescaleDB reckons to keep chunk sizes smaller than 25% of PostgreSQL RAM allocation but still as large
as possible to prevent chunks from being swapped in and out. All in all, this leads to 2
considerations: 1) Utilize a single hypertable for all profiles within an ESDL and 2) Set the 
(chunk) time interval of the hypertable to 1 years.

See https://www.timescale.com/blog/timescale-cloud-tips-testing-your-chunk-size/ for chunk
size recommendations.

Plusses:
- Queries within a single ESDL are fast and require only a single chunk to be read.
- Data is retained as an per-ESDL unit so dropping chunks/tables is easy.
- Only 1 chunk is expected to be created for most ESDLs as the interval is set to 1 years.

Downsides:
- Queries across multiple ESDLs and/or multiple years would require multiple chunks to be read.
  However, the only practical solution for this would be to dump all data from all ESDLs into a
  single table which would be disastrous due to chunking. We expect queries to be mostly on a
  per-ESDL basis so this downside is expected not to happen too often.

## Worst-case analysis
Assume an ESDL with 500 assets and 20 distinct KPI profiles running up to 5 years with a 15 minute
resolution. The chunk would become `500 assets * 20 profiles * 5 years * 275KB = ~13,1GB`.
While an ESDL may quickly grow (adding a pipe always adds a return pipe which
results in 2 assets added) 500 assets would be on the large side. 20 profiles would also be on
the high side but not unreasonable. For instance, a single simulation may be interested in
pressure, flowrate, temperature, heat-loss and heat-transferred KPI's and perhaps a number of
financial KPI's may be added as well. 5 years may be unreasonable for our current purposes.
Simulating or optimizing over multiple years may not make sense as a single year may just
be repeated multiple years. A time resolution of 15 minutes is considered very detailed, but
hourly is considered normal.

13,1GB of data for a single ESDL is unreasonable even though the input parameters aren't.
Therefor, we need to protect the architecture against generating this much data in the first place.
Therefor, we recommend an upper limit of 1GB per ESDL of data. This would ensure that queries
across 5 ESDLs (scenarios) would lead to the concurrent reading of 5GB of data.


A lot of profile information maybe generated with the threshold at `1GB`. For instance, assuming a
more average 250 assets, 10 profiles for 1 year leads to `1006MB` of data.

Using the recommendation of 25% of PostgreSQL RAM allocation of all active chunks, it would lead to at least
4GB for PostgreSQL in a production deployment for a single concurrent user. However, to be safe, we will recommend 32GB of RAM
for PostgreSQL memory allocation due to concurrent users.


## Optimization
As the access patterns expect that a profile will be retrieved per asset, it is advised to create
an index on the `asset_id` column on the `<esdl_id>_profiles` hypertable. This will allow
PostgreSQL to be very fast on retrieving all rows that are associated with some `asset_id` as
opposed to performing a table scan. A quick check on laptop showed an improvement from 480ms
down to 22ms on the query `select "HeatIn.Q1" from "47ba5e2e-dbed-40b2-bfa7-ae10bec48bcb_profiles" where asset_id='0540ea6a-88ef-4d24-b015-d7e34aa999f2';`
where the `<esdl_id>_profiles` table contained a year profile on 15 minute resolution for 250 assets
with 10 KPI profiles in total.


# TODO
Check with simulation AND optimization teams:
- Would we always optimize/simulate up to a year? Or also for multiple years?
- What would be the lowest expected time resolution for optimization/simulation? 1 hour? 15 minutes? 
  Does the resolution matter for the total timespan of the simulation?
- How many assets do you expect to exist at most in an ESDL?
- How many KPI profiles do you expect to generate at most?
- When a user views the data, which time spans would they be expected to use? Multiple years?
  Within a day? Within an hour? Within a month?

Check with ESDL team:
- Are id's always uuids? If so, we can save some storage by setting the appropriate columns to uuid type!

Work on myself:
In current setup, the performance to add a column is going to suck if the table is already large.
Query would be similar to `insert ... where asset_id='...' and time='...'` and would need
to be performed e.g. 35040 / as many data points as there are. 
Adding data for a new asset is fine as it would lead to completely new rows.