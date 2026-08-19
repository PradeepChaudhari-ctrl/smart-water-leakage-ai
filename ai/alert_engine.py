def evaluate_alert(
    probability,
    pressure,
    flow_rate
):
    """
    Decide whether sensor conditions
    are strong enough to generate a leakage alert.
    """

    probability = float(probability)
    pressure = float(pressure)
    flow_rate = float(flow_rate)

    # HIGH RISK
    if (
        probability >= 80
        and pressure < 30
        and flow_rate > 12
    ):
        return {
            "alert": True,
            "severity": "HIGH",
            "message": "Critical water leakage detected"
        }

    # MEDIUM RISK
    if probability >= 50:
        return {
            "alert": True,
            "severity": "MEDIUM",
            "message": "Possible water leakage detected"
        }

    # NORMAL
    return {
        "alert": False,
        "severity": "LOW",
        "message": "Water system operating normally"
    }