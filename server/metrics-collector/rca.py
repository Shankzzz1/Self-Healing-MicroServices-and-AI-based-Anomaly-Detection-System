def diagnose(metrics):

    rps = metrics["rps"]
    error_rate = metrics["error_rate"]
    latency = metrics["p95_latency"]


    # --------------------------------
    # Traffic spike
    # --------------------------------
    if rps > 1.2:
        return "traffic_spike"


    # --------------------------------
    # Service failure
    # --------------------------------
    if error_rate > 0:
        return "service_failure"


    # --------------------------------
    # Dependency issue
    # --------------------------------
    if latency > 0.008 and error_rate == 0:
        return "dependency_issue"


    # --------------------------------
    # Traffic drop
    # --------------------------------
    if rps < 0.4:
        return "traffic_drop"


    return "unknown"