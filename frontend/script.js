const API = "http://127.0.0.1:8000";


let chart = null;
let liveSensorChart = null;
let severityChart = null;


// Prevent multiple calls
let sensorRunning = false;


// ======================================================
// HELPER FUNCTIONS
// ======================================================


function setText(id, value){

    const element = document.getElementById(id);

    if(element){

        element.textContent = value;

    }

}



function getStatusClass(status){

    const value = String(status || "").toLowerCase();


    if(
        value.includes("leakage") ||
        value.includes("warning") ||
        value.includes("alert")
    ){

        return "status-warning";

    }


    return "status-normal";

}




// ======================================================
// LIVE SENSOR UPDATE
// ======================================================


async function updateSensor(){


    // stop duplicate request

    if(sensorRunning){

        return;

    }


    sensorRunning = true;


    try{


        const response = await fetch(

            API + "/sensor/live",

            {
                cache:"no-store"
            }

        );



        if(!response.ok){

            throw new Error(
                "Sensor API Error"
            );

        }



        const data =
        await response.json();



        console.log(
            "Live Sensor:",
            data
        );



        // FLOW

        // FLOW

setText(
    "flow",
    `${Number(data.flow_rate).toFixed(2)} L/min`
);



        // PRESSURE

        setText(

            "pressure",

            `${Number(data.pressure).toFixed(2)} Pa`

        );



        // TEMPERATURE

        setText(

            "temperature",

            `${Number(data.temperature).toFixed(2)} °C`

        );





        // AI prediction

        const result =
        await predictLive(data);





        const sensorStatus =
        document.getElementById(
            "sensorAIStatus"
        );



        if(sensorStatus){


            sensorStatus.innerHTML =

            `
            ${result.status}
            <br>
            ${result.leakage_probability}%
            `;



            sensorStatus.className =
            getStatusClass(
                result.status
            );

        }



    }


    catch(error){


        console.error(
            "Sensor Error:",
            error
        );


        setText(
            "sensorAIStatus",
            "API Error"
        );


    }


    finally{


        sensorRunning = false;


    }



}





// ======================================================
// LIVE AI PREDICTION
// ======================================================


async function predictLive(data){



    const response =
    await fetch(

        API + "/sensor/predict",

        {


            method:"POST",


            headers:{

                "Content-Type":
                "application/json"

            },


            body:
            JSON.stringify(data)


        }

    );




    if(!response.ok){

        throw new Error(
            "Prediction API Error"
        );

    }





    const result =
    await response.json();




    console.log(
        "Live Prediction:",
        result
    );




    const probability =
    Number(
        result.leakage_probability ?? 0
    );




    // STATUS


    const liveStatus =
    document.getElementById(
        "liveStatus"
    );



    if(liveStatus){


        liveStatus.textContent =
        result.status;



        liveStatus.className =
        getStatusClass(
            result.status
        );


    }





    // PROBABILITY


    setText(

        "liveProbability",

        `${probability}%`

    );






    // SEVERITY


    setText(

        "liveSeverity",

        result.severity || "-"

    );






    // RISK

    updateRiskMeter(
        probability
    );






    // ALERT

    updateAlert(

        result.status,

        probability

    );






    // ANOMALY

updateAnomaly(result);

updateExplanation(result);


return result;
    


}






// ======================================================
// RISK METER
// ======================================================


function updateRiskMeter(value){


    const probability =
    Number(value) || 0;




    setText(

        "gaugeValue",

        `${probability}%`

    );





    const circle =
    document.getElementById(
        "riskCircle"
    );



    if(!circle){

        return;

    }




    if(probability < 30){


        circle.style.borderColor =
        "green";


    }

    else if(probability < 80){


        circle.style.borderColor =
        "orange";


    }

    else{


        circle.style.borderColor =
        "red";


    }



}





// ======================================================
// ALERT SYSTEM
// ======================================================


function updateAlert(status, probability=0){


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



    if(!box || !msg){

        return;

    }




    const text =
    String(status || "")
    .toLowerCase();





    if(text.includes("leakage")){


        msg.textContent =
        "⚠️ Water Leakage Alert";



        if(action){

            action.textContent =
            `Inspect pipeline (${probability}%)`;

        }




        box.className =
        "card alert-card alert-danger";


    }


    else{


        msg.textContent =
        "✅ System Normal";



        if(action){

            action.textContent =
            "No action required";

        }




        box.className =
        "card alert-card alert-normal";

    }



}





// ======================================================
// ANOMALY
// ======================================================


function updateAnomaly(data){

    if(!data || !data.anomaly){
        return;
    }


    const anomaly = data.anomaly;


    setText(
        "anomalyStatus",
        anomaly.status || "-"
    );


    setText(
        "anomalyScore",
        anomaly.anomaly_score + "%" || "-"
    );


    setText(
        "anomalyCount",
        anomaly.anomaly_count || "-"
    );


    setText(
        "anomalyMessage",
        anomaly.status === "Normal"
        ? "No abnormal pattern detected"
        : "Abnormal sensor pattern detected"
    );

}
// ======================================================
// AI EXPLANATION
// ======================================================

function updateExplanation(data){

    const box =
    document.getElementById(
        "explanation"
    );


    if(!box){
        return;
    }


    box.innerHTML = "";


    if(data.explanation){

        data.explanation.forEach(item=>{

            box.innerHTML +=
            `
            <li>
                ${item}
            </li>
            `;

        });

    }

}
// ======================================================
// CSV PREDICTION
// ======================================================


async function predict(){


    const fileInput =
    document.getElementById(
        "file"
    );



    if(
        !fileInput ||
        !fileInput.files.length
    ){

        alert(
            "Please select CSV file"
        );

        return;

    }




    const formData =
    new FormData();



    formData.append(

        "file",

        fileInput.files[0]

    );





    try{


        const response =
        await fetch(

            API + "/predict",

            {

                method:"POST",

                body:formData

            }

        );





        if(!response.ok){

            throw new Error(
                "CSV Prediction Error"
            );

        }





        const data =
        await response.json();





        console.log(
            "CSV Result:",
            data
        );






        setText(

            "status",

            `Status: ${data.status}`

        );




        setText(

            "probability",

            `Leakage Probability: ${data.leakage_probability}%`

        );





        setText(

            "severity",

            `Severity: ${data.severity}`

        );






        updateRiskMeter(

            data.leakage_probability

        );





        updateAlert(

            data.status,

            data.leakage_probability

        );






        updateAnomaly(data);





        if(data.signal){

            drawChart(
                data.signal
            );

        }





        await loadHistory();



    }


    catch(error){


        console.error(
            error
        );


        alert(
            "Backend connection error"
        );


    }



}









// ======================================================
// PRESSURE SIGNAL CHART
// ======================================================


function drawChart(signal){



    const canvas =
    document.getElementById(
        "sensorChart"
    );



    if(
        !canvas ||
        !Array.isArray(signal)
    ){

        return;

    }




    if(chart){

        chart.destroy();

    }





    chart =
    new Chart(

        canvas,

        {


            type:"line",


            data:{


                labels:
                signal.map(
                    (_,i)=>i
                ),



                datasets:[

                    {

                        label:
                        "Pressure Signal",


                        data:
                        signal,


                        borderWidth:2,


                        pointRadius:0,


                        tension:0.3

                    }

                ]

            },



            options:{


                responsive:true,


                maintainAspectRatio:false,


                animation:false


            }


        }

    );



}









// ======================================================
// HISTORY
// ======================================================


async function loadHistory(){


    try{


        const response =
        await fetch(

            API + "/history",

            {
                cache:"no-store"
            }

        );




        if(!response.ok){

            return;

        }





        const data =
        await response.json();





        const table =
        document.getElementById(
            "history"
        );





        if(!table){

            return;

        }





        table.innerHTML="";






        if(!Array.isArray(data)){

            return;

        }





        data.forEach(item=>{


            table.innerHTML +=

            `

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


        });





    }


    catch(error){


        console.error(
            "History Error",
            error
        );


    }


}









// ======================================================
// DASHBOARD STATS
// ======================================================


async function loadStats(){



    try{


        const response =
        await fetch(

            API + "/stats",

            {
                cache:"no-store"
            }

        );





        const data =
        await response.json();






        console.log(
            "Stats:",
            data
        );






        setText(

            "totalPredictions",

            data.total_predictions ?? 0

        );





        setText(

            "leakageCases",

            data.leakage_detected ?? 0

        );






        setText(

            "normalCases",

            data.normal_cases ?? 0

        );






        setText(

            "averageRisk",

            `${data.average_probability ?? 0}%`

        );








        if(

            data.recent_predictions &&
            data.recent_predictions.length

        ){



            const latest =
            data.recent_predictions[0];





            setText(

                "latestFile",

                latest.filename

            );





            setText(

                "latestStatus",

                latest.status

            );





            setText(

                "latestProbability",

                latest.probability+"%"

            );





            setText(

                "latestSeverity",

                latest.severity

            );



        }





        if(data.severity_count){


            createSeverityChart(

                data.severity_count

            );


        }





    }


    catch(error){


        console.error(
            "Stats Error",
            error
        );


    }



}









// ======================================================
// SEVERITY CHART
// ======================================================


function createSeverityChart(data){



    const canvas =
    document.getElementById(
        "severityChart"
    );



    if(
        !canvas ||
        !data
    ){

        return;

    }





    if(severityChart){

        severityChart.destroy();

    }






    severityChart =
    new Chart(

        canvas,

        {


            type:"doughnut",



            data:{


                labels:[

                    "LOW",

                    "MEDIUM",

                    "HIGH"

                ],




                datasets:[


                    {


                        data:[

                            data.LOW || 0,

                            data.MEDIUM || 0,

                            data.HIGH || 0

                        ],



                        borderWidth:2


                    }


                ]



            },





            options:{


                responsive:true,


                maintainAspectRatio:false,


                cutout:"55%"


            }


        }

    );



}
// ======================================================
// LIVE SENSOR GRAPH
// ======================================================


// ======================================================
// LIVE SENSOR GRAPH
// ======================================================

async function loadLiveSensorGraph(){

    console.log("📈 LIVE SENSOR GRAPH STARTED");


    try{

        const response = await fetch(
            API + "/sensor/history",
            {
                cache:"no-store"
            }
        );


        const data = await response.json();


        console.log(
            "GRAPH DATA:",
            data
        );


        const canvas =
        document.getElementById(
            "liveSensorChart"
        );


        if(!canvas){

            console.log(
                "Canvas Missing"
            );

            return;

        }



        const labels = data.map(
            item => 
            item.timestamp.slice(11,19)
        );


        const pressure = data.map(
            item =>
            Number(item.pressure)
        );


        const flow = data.map(
            item =>
            Number(item.flow_rate)
        );


        const temperature = data.map(
            item =>
            Number(item.temperature)
        );



        if(liveSensorChart){

            liveSensorChart.destroy();

        }



        liveSensorChart =
        new Chart(
            canvas,
            {

                type:"line",

                data:{

                    labels:labels,


                    datasets:[


                    {
                        label:"Pressure",

                        data:pressure,

                        borderWidth:2

                    },


                    {
                        label:"Flow",

                        data:flow,

                        borderWidth:2

                    },


                    {
                        label:"Temperature",

                        data:temperature,

                        borderWidth:2

                    }


                    ]

                },


                options:{

                    responsive:true,

                    maintainAspectRatio:false

                }


            }
        );


        console.log(
            "✅ LIVE CHART CREATED"
        );


    }


    catch(error){

        console.error(
            "GRAPH ERROR",
            error
        );

    }


}


// ======================================================
// AUTO REFRESH
// ======================================================


// Sensor update
// 30 sec

// setInterval(

// updateSensor,

// 30000

// );





// // History update
// // 30 sec

// setInterval(

// loadHistory,

// 30000

// );





// // Dashboard stats
// // 30 sec

// setInterval(

// loadStats,

// 30000

// );





// // Live graph
// // 60 sec

// setInterval(

// loadLiveSensorGraph,

// 60000

// );





// // Alert check
// // 10 sec

// setInterval(

// checkAlert,

// 10000

// ======================================================
// ALERT CHECK
// ======================================================

async function checkAlert(){


    try{


        const response =
        await fetch(

            API + "/alert/status",

            {
                cache:"no-store"
            }

        );



        const data =
        await response.json();



        console.log(
            "Alert:",
            data
        );



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



        if(!box || !msg)
            return;



        if(data.alert){


            msg.textContent =
            "⚠️ Water Leakage Alert";


            if(action){

                action.textContent =
                "Inspect pipeline immediately";

            }


            box.className =
            "alert-card card alert-danger";


        }

        else{


            msg.textContent =
            "✅ System Normal";


            if(action){

                action.textContent =
                "No action required";

            }


            box.className =
            "alert-card card alert-normal";


        }


    }


    catch(error){


        console.error(
            "Alert Error",
            error
        );


    }


}

// ======================================================
// AUTO UPDATE
// ======================================================


setInterval(
    updateSensor,
    5000
);


setInterval(
    loadLiveSensorGraph,
    5000
);


setInterval(
    checkAlert,
    5000
);
setInterval(
    loadAlerts,
    10000
);
// ======================================================
// PAGE LOAD
// ======================================================

window.addEventListener(
"load",
async function(){

    console.log(
        "💧 Dashboard Started"
    );


    await loadStats();

    await loadHistory();

    await updateSensor();

    await loadLiveSensorGraph();

    await checkAlert();
    await loadAlerts();


});
// ======================================
// ALERT HISTORY
// ======================================

async function loadAlerts(){

    try{

        const response = await fetch(
            API + "/alerts",
            {
                cache: "no-store"
            }
        );

        if(!response.ok){

            throw new Error(
                "Alert API Error"
            );

        }

        const data = await response.json();

        console.log(
            "Alert History:",
            data
        );

        const box =
            document.getElementById(
                "alertHistory"
            );

        if(!box){
            return;
        }

        box.innerHTML = "";

        if(!Array.isArray(data)){
            return;
        }

        data.forEach(alert => {

            box.innerHTML += `
                <div class="alert-item">

                    <h4>
🚨 ${alert.alert_type}
</h4>

<p>
${alert.message}
</p>

<span>
Severity: ${alert.severity}
</span>

<span>
Probability: ${alert.probability}%
</span>

<small>
${alert.timestamp}
</small>

                </div>
            `;

        });

    }

    catch(error){

        console.error(
            "Alert History Error:",
            error
        );

    }

}