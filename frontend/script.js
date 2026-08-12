const API = "http://127.0.0.1:8000";

let chart = null;


// =================================
// LIVE SENSOR MONITORING
// =================================

async function updateSensor(){


try{


let response = await fetch(
API + "/sensor/live"
);


let data = await response.json();


console.log("Live Sensor:",data);



// Flow Rate

let flow =
document.getElementById("flowRate");


if(flow){

flow.innerHTML =
data.flow_rate + " L/min";

}



// Pressure

let pressure =
document.getElementById("pressure");


if(pressure){

pressure.innerHTML =
data.pressure + " Pa";

}



// Temperature

let temperature =
document.getElementById("temperature");


if(temperature){

temperature.innerHTML =
data.temperature + " °C";

}



// Live Status

let liveStatus =
document.getElementById("sensorAIStatus");

if(liveStatus){


let result =
await predictLive(data);



liveStatus.innerHTML =

result.status +
"<br>" +
result.leakage_probability +
"%";


}



}


catch(error){

console.log(
"Sensor Error:",
error
);


}


}





// =================================
// LIVE AI PREDICTION
// =================================

async function predictLive(data){


let response = await fetch(

API+"/sensor/predict",

{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify(data)

}

);



let result = await response.json();



// ===============================
// Live AI Prediction Update
// ===============================


let liveStatus =
document.getElementById(
"liveStatus"
);



let liveProbability =
document.getElementById(
"liveProbability"
);



let liveSeverity =
document.getElementById(
"liveSeverity"
);





if(liveStatus){

liveStatus.innerHTML =
result.status;

}




if(liveProbability){

liveProbability.innerHTML =
result.leakage_probability + "%";

}





if(liveSeverity){

liveSeverity.innerHTML =
result.severity;

}





return result;


}
// =================================
// CSV PREDICTION
// =================================


async function predict(){


let file =
document.getElementById("file").files[0];



if(!file){

alert(
"Please select CSV file"
);

return;

}



let formData =
new FormData();


formData.append(
"file",
file
);



try{


let response =
await fetch(

API+"/predict",

{

method:"POST",

body:formData

}

);



let data =
await response.json();



console.log(
"Prediction:",
data
);





// Status


document.getElementById("status").innerHTML =

"Status: "
+
data.status;



// Probability


document.getElementById("probability").innerHTML =

"Leakage Probability: "
+
data.leakage_probability
+
"%";



// Severity


document.getElementById("severity").innerHTML =

"Severity: "
+
data.severity;





// Risk Meter


updateRiskMeter(
data.leakage_probability
);






// Alert


updateAlert(
data.status
);







// Explanation


let explanation =
document.getElementById(
"explanation"
);


if(explanation){


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
✔ Leakage severity calculated
</li>


`;



}





// Graph


if(data.signal){

drawChart(
data.signal
);

}




loadHistory();



}


catch(error){


console.log(error);


alert(
"Backend connection error"
);


}



}









// =================================
// RISK METER
// =================================


function updateRiskMeter(value){


let circle =
document.getElementById(
"riskCircle"
);


let text =
document.getElementById(
"gaugeValue"
);



if(text){

text.innerHTML =
value+"%";

}




if(circle){



if(value < 50){

circle.style.borderColor="green";

}


else if(value < 80){

circle.style.borderColor="orange";

}


else{

circle.style.borderColor="red";

}


}



}









// =================================
// ALERT SYSTEM
// =================================


function updateAlert(status){


let box =
document.getElementById(
"alertBox"
);


let msg =
document.getElementById(
"alertMessage"
);


let action =
document.getElementById(
"action"
);



if(status==="Leakage Detected"){


msg.innerHTML =
"⚠️ Water Leakage Alert";


action.innerHTML =
"Action: Inspect pipeline immediately";


box.className =
"card alert-card alert-danger";


}


else{


msg.innerHTML =
"✅ System Normal";


action.innerHTML =
"No action required";


box.className =
"card alert-card alert-normal";


}



}









// =================================
// GRAPH
// =================================


function drawChart(signal){



let canvas =
document.getElementById(
"sensorChart"
);



if(!canvas){

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



datasets:[{


label:"Pressure Signal",


data:signal,


borderWidth:2,


pointRadius:0,


tension:0.3


}]


},



options:{


responsive:true,


maintainAspectRatio:false,


animation:false


}


}


);



}









// =================================
// HISTORY
// =================================


async function loadHistory(){


try{


let response =
await fetch(

API+"/history"

);



let data =
await response.json();



let table =
document.getElementById(
"history"
);



if(!table){

return;

}



table.innerHTML="";



data.forEach(item=>{


table.innerHTML +=

`

<tr>

<td>${item.filename}</td>

<td>${item.status}</td>

<td>${item.probability}%</td>

<td>${item.severity}</td>

<td>${item.timestamp}</td>


</tr>

`;



});



}


catch(error){


console.log(
"History Error",
error
);


}



}









// =================================
// AUTO ALERT CHECK
// =================================


async function checkAlert(){


try{


let response =
await fetch(

API+"/alert/status"

);



let data =
await response.json();



let msg =
document.getElementById(
"alertMessage"
);


let box =
document.getElementById(
"alertBox"
);



if(data.alert){


msg.innerHTML =
data.message;


box.className =
"card alert-card alert-danger";


}

else{


msg.innerHTML =
data.message;


box.className =
"card alert-card alert-normal";


}



}


catch(error){


console.log(
"Alert Error",
error
);


}



}









// =================================
// PAGE LOAD
// =================================



window.onload=function(){


loadHistory();


updateSensor();


checkAlert();


};




// Refresh Live Data

setInterval(

updateSensor,

5000

);



// Refresh Alert

setInterval(

checkAlert,

5000

);