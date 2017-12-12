$(document).ready(function(){

    var fullpath =window.location.pathname;

    $('.navigationclass').find('a').each(function() {
        $(this).toggleClass('active', $(this).attr('href') == fullpath);
    });
});

function myFunction(){
    var x = document.getElementById("navigationid");
    if (x.className === "navigationclass") {
        x.className += " responsive";
    } else {
        x.className = "navigationclass";
    }
}
function clickFunction(date,cloudiness,pressure,humidity,cloudpercentage){
    document.getElementById('details').style.display = "table";
    document.getElementById('detailstitle').innerHTML = "Details for " + date.toLowerCase();
    document.getElementById('paragraphcloudsinfo').innerHTML = "Cloudiness";
    document.getElementById('paragraphcloudsdata').innerHTML = cloudiness;

    document.getElementById('paragraphcloudspinfo').innerHTML = "Cloudiness, %";
    document.getElementById('paragraphcloudspdata').innerHTML = cloudpercentage;

    document.getElementById('paragraphpressureinfo').innerHTML = "Pressure";
    document.getElementById('paragraphpressuredata').innerHTML = pressure;

    document.getElementById('paragraphhumidityinfo').innerHTML = "Humidity";
    document.getElementById('paragraphhumiditydata').innerHTML = humidity;

    document.getElementById('details').scrollIntoView();
}
