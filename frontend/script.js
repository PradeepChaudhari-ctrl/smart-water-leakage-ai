const API = "http://127.0.0.1:8000";

let chart = null;


// ======================================================
// HELPER
// ======================================================

function setText(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


function getStatusClass(status) {

    const value = String(status || "").toLowerCase();

    if (
        value.includes("leakage") ||
        value.includes("warning") ||
        value.includes("alert")
    ) {
        return "status-warning";
    }

    return "status-normal";
}


// ======================================================
// LIVE SENSOR MONITORING
// ======================================================

async function updateSensor() {

    try {

        const response = await fetch(
            API + "/sensor/live",
            {
                cache: "no-store"
            }
        );


        if (!response.ok) {

            throw new Error(
                `Sensor API Error: ${response.status}`
            );

        }


        const data = await response.json();


        console.log("Live Sensor:", data);


        // --------------------------------------------------
        // FLOW RATE
        // --------------------------------------------------

        const flow = document.getElementById("flowRate");

        if (flow) {

            flow.textContent =
                `${Number(data.flow_rate).toFixed(2)} L/min`;

        }


        // --------------------------------------------------
        // PRESSURE
        // --------------------------------------------------

        const pressure =
            document.getElementById("pressure");

        if (pressure) {

            pressure.textContent =
                `${Number(data.pressure).toFixed(2)} Pa`;

        }


        // --------------------------------------------------
        // TEMPERATURE
        // --------------------------------------------------

        const temperature =
            document.getElementById("temperature");

        if (temperature) {

            temperature.textContent =
                `${Number(data.temperature).toFixed(2)} °C`;

        }


        // --------------------------------------------------
        // LIVE AI PREDICTION
        // --------------------------------------------------

        const result =
            await predictLive(data);


        // --------------------------------------------------
        // LIVE AI STATUS
        // --------------------------------------------------

        const sensorAIStatus =
            document.getElementById("sensorAIStatus");


        if (sensorAIStatus) {

            sensorAIStatus.innerHTML =
                `${result.status}<br>${result.leakage_probability}%`;

            sensorAIStatus.classList.remove(
                "status-normal",
                "status-warning"
            );

            sensorAIStatus.classList.add(
                getStatusClass(result.status)
            );

        }


    }

    catch (error) {

        console.error(
            "Sensor Error:",
            error
        );

        setText(
            "sensorAIStatus",
            "API Error"
        );

    }

}


// ======================================================
// LIVE AI PREDICTION
// ======================================================

async function predictLive(data) {

    const response = await fetch(

        API + "/sensor/predict",

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(data)

        }

    );


    if (!response.ok) {

        throw new Error(
            `Prediction API Error: ${response.status}`
        );

    }


    const result =
        await response.json();


    console.log(
        "Live Prediction:",
        result
    );


    // ==================================================
    // CURRENT STATUS
    // ==================================================

    const liveStatus =
        document.getElementById("liveStatus");


    if (liveStatus) {

        liveStatus.textContent =
            result.status;

        liveStatus.classList.remove(
            "status-normal",
            "status-warning"
        );

        liveStatus.classList.add(
            getStatusClass(result.status)
        );

    }


    // ==================================================
    // LEAKAGE PROBABILITY
    // ==================================================

    const probability =
        Number(
            result.leakage_probability ?? 0
        );


    const liveProbability =
        document.getElementById(
            "liveProbability"
        );


    if (liveProbability) {

        liveProbability.textContent =
            `${probability}%`;

    }


    // ==================================================
    // SEVERITY
    // ==================================================

    const liveSeverity =
        document.getElementById(
            "liveSeverity"
        );


    if (liveSeverity) {

        liveSeverity.textContent =
            result.severity || "-";

    }


    // ==================================================
    // RISK METER
    // ==================================================

    updateRiskMeter(
        probability
    );


    // ==================================================
    // LIVE ALERT
    // ==================================================

    updateAlert(
        result.status,
        probability
    );


    // ==================================================
    // OPTIONAL LIVE ANOMALY DATA
    // ==================================================

    updateAnomaly(
        result
    );


    return result;

}


// ======================================================
// CSV PREDICTION
// ======================================================

async function predict() {

    const fileInput =
        document.getElementById("file");


    if (!fileInput || !fileInput.files.length) {

        alert(
            "Please select CSV file"
        );

        return;

    }


    const file =
        fileInput.files[0];


    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    try {

        const response =
            await fetch(

                API + "/predict",

                {

                    method: "POST",

                    body: formData

                }

            );


        if (!response.ok) {

            throw new Error(
                `Prediction Error: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "CSV Prediction:",
            data
        );


        // ==================================================
        // STATUS
        // ==================================================

        setText(
            "status",
            `Status: ${data.status}`
        );


        // ==================================================
        // PROBABILITY
        // ==================================================

        setText(
            "probability",
            `Leakage Probability: ${data.leakage_probability}%`
        );


        // ==================================================
        // SEVERITY
        // ==================================================

        setText(
            "severity",
            `Severity: ${data.severity}`
        );


        // ==================================================
        // RISK METER
        // ==================================================

        updateRiskMeter(
            Number(
                data.leakage_probability ?? 0
            )
        );


        // ==================================================
        // ALERT
        // ==================================================

        updateAlert(
            data.status,
            Number(
                data.leakage_probability ?? 0
            )
        );


        // ==================================================
        // ANOMALY
        // ==================================================

        updateAnomaly(
            data
        );


        // ==================================================
        // EXPLANATION
        // ==================================================

        const explanation =
            document.getElementById(
                "explanation"
            );


        if (explanation) {

            explanation.innerHTML = `

                <li>
                    ✔ Sensor signal analyzed
                </li>

                <li>
                    ✔ Pressure pattern checked
                </li>

                <li>
                    ✔ Machine Learning model executed
                </li>

                <li>
                    ✔ Leakage probability calculated
                </li>

                <li>
                    ✔ Leakage severity calculated
                </li>

            `;

        }


        // ==================================================
        // GRAPH
        // ==================================================

        if (data.signal) {

            drawChart(
                data.signal
            );

        }


        // ==================================================
        // HISTORY
        // ==================================================

        await loadHistory();

    }


    catch (error) {

        console.error(
            "CSV Prediction Error:",
            error
        );


        alert(
            "Backend connection error. Make sure FastAPI is running."
        );

    }

}


// ======================================================
// RISK METER
// ======================================================

function updateRiskMeter(value) {

    const probability =
        Number(value) || 0;


    const circle =
        document.getElementById(
            "riskCircle"
        );


    const text =
        document.getElementById(
            "gaugeValue"
        );


    if (text) {

        text.textContent =
            `${probability}%`;

    }


    if (!circle) {

        return;

    }


    // Remove old colors

    circle.style.borderColor =
        "";


    // -----------------------------------------------
    // LOW
    // -----------------------------------------------

    if (probability < 30) {

        circle.style.borderColor =
            "green";

    }


    // -----------------------------------------------
    // MEDIUM
    // -----------------------------------------------

    else if (probability < 80) {

        circle.style.borderColor =
            "orange";

    }


    // -----------------------------------------------
    // HIGH
    // -----------------------------------------------

    else {

        circle.style.borderColor =
            "red";

    }

}


// ======================================================
// ALERT SYSTEM
// ======================================================

function updateAlert(
    status,
    probability = 0
) {

    const box =
        document.getElementById(
            "alertBox"
        );


    const msg =
        document.getElementById(
            "alertMessage"
        );


    const action =
        document.getElementById(
            "action"
        );


    if (!box || !msg || !action) {

        return;

    }


    const statusText =
        String(status || "").toLowerCase();


    const leakDetected =
        statusText.includes("leakage");


    // ==================================================
    // LEAKAGE
    // ==================================================

    if (leakDetected) {

        msg.textContent =
            "⚠️ Water Leakage Alert";


        action.textContent =
            `Action: Inspect pipeline immediately (${probability}% probability)`;


        box.className =
            "card alert-card alert-danger";

    }


    // ==================================================
    // NORMAL
    // ==================================================

    else {

        msg.textContent =
            "✅ System Normal";


        action.textContent =
            "No action required";


        box.className =
            "card alert-card alert-normal";

    }

}


// ======================================================
// ANOMALY ANALYSIS
// ======================================================

function updateAnomaly(data) {

    const anomalyStatus =
        document.getElementById(
            "anomalyStatus"
        );


    const anomalyScore =
        document.getElementById(
            "anomalyScore"
        );


    const anomalyCount =
        document.getElementById(
            "anomalyCount"
        );


    const anomalyMessage =
        document.getElementById(
            "anomalyMessage"
        );


    // --------------------------------------------------
    // If backend doesn't send anomaly data,
    // keep existing dashboard stable.
    // --------------------------------------------------

    if (!data) {

        return;

    }


    // --------------------------------------------------
    // Anomaly status
    // --------------------------------------------------

    if (
        anomalyStatus &&
        data.anomaly_status !== undefined
    ) {

        anomalyStatus.textContent =
            `Status: ${data.anomaly_status}`;

    }


    // --------------------------------------------------
    // Anomaly score
    // --------------------------------------------------

    if (
        anomalyScore &&
        data.anomaly_score !== undefined
    ) {

        anomalyScore.textContent =
            `Score: ${data.anomaly_score}`;

    }


    // --------------------------------------------------
    // Anomaly count
    // --------------------------------------------------

    if (
        anomalyCount &&
        data.anomaly_count !== undefined
    ) {

        anomalyCount.textContent =
            `Anomalies: ${data.anomaly_count}`;

    }


    // --------------------------------------------------
    // Anomaly message
    // --------------------------------------------------

    if (
        anomalyMessage &&
        data.anomaly_message !== undefined
    ) {

        anomalyMessage.textContent =
            data.anomaly_message;

    }

}


// ======================================================
// GRAPH
// ======================================================

function drawChart(signal) {

    const canvas =
        document.getElementById(
            "sensorChart"
        );


    if (!canvas) {

        return;

    }


    if (!Array.isArray(signal)) {

        return;

    }


    if (chart) {

        chart.destroy();

    }


    chart =
        new Chart(

            canvas,

            {

                type: "line",

                data: {

                    labels:
                        signal.map(
                            (_, index) => index
                        ),

                    datasets: [

                        {

                            label:
                                "Pressure Signal",

                            data:
                                signal,

                            borderWidth:
                                2,

                            pointRadius:
                                0,

                            tension:
                                0.3

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false,

                    animation:
                        false

                }

            }

        );

}


// ======================================================
// HISTORY
// ======================================================

async function loadHistory() {

    try {

        const response =
            await fetch(

                API + "/history",

                {
                    cache: "no-store"
                }

            );


        if (!response.ok) {

            throw new Error(
                `History API Error: ${response.status}`
            );

        }


        const data =
            await response.json();


        const table =
            document.getElementById(
                "history"
            );


        if (!table) {

            return;

        }


        table.innerHTML = "";


        if (!Array.isArray(data)) {

            return;

        }


        data.forEach(
            item => {

                table.innerHTML += `

                    <tr>

                        <td>
                            ${item.filename ?? "-"}
                        </td>

                        <td>
                            ${item.status ?? "-"}
                        </td>

                        <td>
                            ${item.probability ?? "-"}%
                        </td>

                        <td>
                            ${item.severity ?? "-"}
                        </td>

                        <td>
                            ${item.timestamp ?? "-"}
                        </td>

                    </tr>

                `;

            }
        );

    }


    catch (error) {

        console.error(
            "History Error:",
            error
        );

    }

}


// ======================================================
// AUTO ALERT CHECK
// ======================================================

async function checkAlert() {

    try {

        const response =
            await fetch(

                API + "/alert/status",

                {
                    cache: "no-store"
                }

            );


        if (!response.ok) {

            throw new Error(
                `Alert API Error: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Alert Status:",
            data
        );


        const msg =
            document.getElementById(
                "alertMessage"
            );


        const box =
            document.getElementById(
                "alertBox"
            );


        const action =
            document.getElementById(
                "action"
            );


        if (!msg || !box) {

            return;

        }


        // ==================================================
        // ALERT
        // ==================================================

        if (data.alert) {

            msg.textContent =
                data.message ||
                "⚠️ Water Leakage Alert";


            if (action) {

                action.textContent =
                    "Action: Inspect pipeline immediately";

            }


            box.className =
                "card alert-card alert-danger";

        }


        // ==================================================
        // NORMAL
        // ==================================================

        else {

            msg.textContent =
                data.message ||
                "✅ System Normal";


            if (action) {

                action.textContent =
                    "No action required";

            }


            box.className =
                "card alert-card alert-normal";

        }

    }


    catch (error) {

        console.error(
            "Alert Error:",
            error
        );

    }

}


// ======================================================
// DASHBOARD STATS
// ======================================================

async function loadStats(){

    try{

        const response = await fetch(
            API + "/stats",
            {
                cache:"no-store"
            }
        );


        if(!response.ok){

            throw new Error(
                "Stats API Error: " + response.status
            );

        }


        const data =
            await response.json();


        console.log(
            "Stats Data:",
            data
        );


        setText(
            "totalPredictions",
            data.total_predictions
        );


        setText(
            "leakageCases",
            data.leakage_detected
        );


        setText(
            "normalCases",
            data.normal_cases
        );


        setText(
            "averageRisk",
            data.average_probability + "%"
        );


    }


    catch(error){

        console.error(
            "Stats Error:",
            error
        );

    }

}



// ======================================================
// PAGE LOAD
// ======================================================

window.addEventListener(
    "load",
    async function(){

        console.log(
            "💧 Smart Water Leakage AI Dashboard Started"
        );


        await loadHistory();


        await updateSensor();


        await checkAlert();


        await loadStats();


    }
);



// ======================================================
// AUTO REFRESH
// ======================================================


// Live sensor + AI prediction

setInterval(
    updateSensor,
    5000
);


// Alert status

setInterval(
    checkAlert,
    5000
);


// History

setInterval(
    loadHistory,
    15000
);


// Statistics

setInterval(
    loadStats,
    15000
);