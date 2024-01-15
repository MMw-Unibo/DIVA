# The following dictionary contains the time and radius thresholds used to 
# understand if the DEN message received is too old or too far. This depends on the eventType
# eventype: threshold (secs,meters)
# Time values come from: 
#   - https://www.car-2-car.org/fileadmin/documents/Basic_System_Profile/Release_1.6.2/C2CCC_RS_2007_TrafficJam.pdf
#   - https://www.car-2-car.org/fileadmin/documents/Basic_System_Profile/Release_1.4.0/C2CCC_RS_2066_Pre-CrashInformation.pdf
arbitrary_thresholds = {
    1: (60,200), # trafficCondition
    2: (3600,200), # accident
    3: (None,200), # roadworks
    5: (None,200),# impassability
    6: (86400,200), # adverseWeatherCondition_Adhesion
    7: (86400,200), # aquaplannning
    9: (3600,200), # hazardousLocation_SurfaceCondition
    10: (3600,200), # hazardousLocation_ObstacleOnTheRoad
    11: (3600,200), # hazardousLocation_AnimalOnTheRoad
    12: (600,200), # humanPresenceOnTheRoad
    14: (600,200), # wrongWayDriving
    15: (3600,200), # rescueAndRecoveryWorkInProgress
    17: (3600,200), # adverseWeatherCondition_ExtremeWeatherCondition
    18: (1800,200), # adverseWeatherCondition_Visibility
    19: (1800,200), # adverseWeatherCondition_Precipitation
    26: (600,200), # slowVehicle
    27: (20,200), # dangerousEndOfQueue
    91: (600,200), # vehicleBreakdown
    92: (3600,200), # postCrash
    93: (600,200), # humanProblem
    94: (600,200), # stationaryVehicle
    95: (120,200), # emergencyVehicleApproaching
    96: (120,200), # hazardousLocation_DangerousCurve
    97: (2,100), # collisionRisk
    98: (120,200), # signalViolation
    99: (120,200), # dangerousSituation
}

mean_based_thresholds = {
    1: (60,292.19), # trafficCondition
    2: (3600,200), # accident
    3: (None,200), # roadworks
    5: (None,200),# impassability
    6: (86400,200), # adverseWeatherCondition_Adhesion
    7: (86400,200), # aquaplannning
    9: (3600,200), # hazardousLocation_SurfaceCondition
    10: (3600,200), # hazardousLocation_ObstacleOnTheRoad
    11: (3600,200), # hazardousLocation_AnimalOnTheRoad
    12: (600,200), # humanPresenceOnTheRoad
    14: (600,200), # wrongWayDriving
    15: (3600,200), # rescueAndRecoveryWorkInProgress
    17: (3600,200), # adverseWeatherCondition_ExtremeWeatherCondition
    18: (1800,200), # adverseWeatherCondition_Visibility
    19: (1800,200), # adverseWeatherCondition_Precipitation
    26: (600,200), # slowVehicle
    27: (20,448.74), # dangerousEndOfQueue
    91: (600,200), # vehicleBreakdown
    92: (3600,200), # postCrash
    93: (600,200), # humanProblem
    94: (600,200), # stationaryVehicle
    95: (120,200), # emergencyVehicleApproaching
    96: (120,200), # hazardousLocation_DangerousCurve
    97: (2,257.33), # collisionRisk
    98: (120,200), # signalViolation
    99: (120,200), # dangerousSituation
}


mode_based_thresholds = {
    1: (60,126.71), # trafficCondition
    2: (3600,200), # accident
    3: (None,200), # roadworks
    5: (None,200),# impassability
    6: (86400,200), # adverseWeatherCondition_Adhesion
    7: (86400,200), # aquaplannning
    9: (3600,200), # hazardousLocation_SurfaceCondition
    10: (3600,200), # hazardousLocation_ObstacleOnTheRoad
    11: (3600,200), # hazardousLocation_AnimalOnTheRoad
    12: (600,200), # humanPresenceOnTheRoad
    14: (600,200), # wrongWayDriving
    15: (3600,200), # rescueAndRecoveryWorkInProgress
    17: (3600,200), # adverseWeatherCondition_ExtremeWeatherCondition
    18: (1800,200), # adverseWeatherCondition_Visibility
    19: (1800,200), # adverseWeatherCondition_Precipitation
    26: (600,200), # slowVehicle
    27: (20,415.21), # dangerousEndOfQueue
    91: (600,200), # vehicleBreakdown
    92: (3600,200), # postCrash
    93: (600,200), # humanProblem
    94: (600,200), # stationaryVehicle
    95: (120,200), # emergencyVehicleApproaching
    96: (120,200), # hazardousLocation_DangerousCurve
    97: (2,137.75), # collisionRisk
    98: (120,200), # signalViolation
    99: (120,200), # dangerousSituation
}


median_based_thresholds = {
    1: (60,126.71), # trafficCondition
    2: (3600,200), # accident
    3: (None,200), # roadworks
    5: (None,200),# impassability
    6: (86400,200), # adverseWeatherCondition_Adhesion
    7: (86400,200), # aquaplannning
    9: (3600,200), # hazardousLocation_SurfaceCondition
    10: (3600,200), # hazardousLocation_ObstacleOnTheRoad
    11: (3600,200), # hazardousLocation_AnimalOnTheRoad
    12: (600,200), # humanPresenceOnTheRoad
    14: (600,200), # wrongWayDriving
    15: (3600,200), # rescueAndRecoveryWorkInProgress
    17: (3600,200), # adverseWeatherCondition_ExtremeWeatherCondition
    18: (1800,200), # adverseWeatherCondition_Visibility
    19: (1800,200), # adverseWeatherCondition_Precipitation
    26: (600,200), # slowVehicle
    27: (20,444.42), # dangerousEndOfQueue
    91: (600,200), # vehicleBreakdown
    92: (3600,200), # postCrash
    93: (600,200), # humanProblem
    94: (600,200), # stationaryVehicle
    95: (120,200), # emergencyVehicleApproaching
    96: (120,200), # hazardousLocation_DangerousCurve
    97: (2,158.15), # collisionRisk
    98: (120,200), # signalViolation
    99: (120,200), # dangerousSituation
}

ninetieth_quantile_based_thresholds ={
    1: (60,575.95), # trafficCondition
    2: (3600,200), # accident
    3: (None,200), # roadworks
    5: (None,200),# impassability
    6: (86400,200), # adverseWeatherCondition_Adhesion
    7: (86400,200), # aquaplannning
    9: (3600,200), # hazardousLocation_SurfaceCondition
    10: (3600,200), # hazardousLocation_ObstacleOnTheRoad
    11: (3600,200), # hazardousLocation_AnimalOnTheRoad
    12: (600,200), # humanPresenceOnTheRoad
    14: (600,200), # wrongWayDriving
    15: (3600,200), # rescueAndRecoveryWorkInProgress
    17: (3600,200), # adverseWeatherCondition_ExtremeWeatherCondition
    18: (1800,200), # adverseWeatherCondition_Visibility
    19: (1800,200), # adverseWeatherCondition_Precipitation
    26: (600,200), # slowVehicle
    27: (20,450.11), # dangerousEndOfQueue
    91: (600,200), # vehicleBreakdown
    92: (3600,200), # postCrash
    93: (600,200), # humanProblem
    94: (600,200), # stationaryVehicle
    95: (120,200), # emergencyVehicleApproaching
    96: (120,200), # hazardousLocation_DangerousCurve
    97: (2,574.92), # collisionRisk
    98: (120,200), # signalViolation
    99: (120,200), # dangerousSituation
}

event_type_names = {
    1: "trafficCondition",
    2: "accident",
    3:  "roadworks",
    5:  "impassability",
    6: "adverseWeatherCondition_Adhesion",
    7: "aquaplannning",
    9:  "hazardousLocation_SurfaceCondition",
    10: "hazardousLocation_ObstacleOnTheRoad",
    11: "hazardousLocation_AnimalOnTheRoad",
    12: "humanPresenceOnTheRoad",
    14: "wrongWayDriving",
    15: "rescueAndRecoveryWorkInProgress",
    17: "adverseWeatherCondition_ExtremeWeatherCondition",
    18: "adverseWeatherCondition_Visibility",
    19: "adverseWeatherCondition_Precipitation",
    26: "slowVehicle",
    27: "dangerousEndOfQueue",
    91: "vehicleBreakdown",
    92: "postCrash",
    93: "humanProblem",
    94: "stationaryVehicle",
    95: "emergencyVehicleApproaching",
    96: "hazardousLocation_DangerousCurve",
    97: "collisionRisk",
    98: "signalViolation",
    99: "dangerousSituation",
}

threshold_types = ['mean', 'median', 'mode', '90percentile']

def get_threshold_set_from_type(ttype):
    if ttype == 'mean':
        return mean_based_thresholds
    elif ttype == 'mode':
        return mode_based_thresholds
    elif ttype == 'median':
        return median_based_thresholds
    elif ttype == '90percentile':
        return ninetieth_quantile_based_thresholds
    else:
        return None