function myFunction(){
    var x = document.getElementById("navigationid");
    if (x.className === "navigationclass") {
        x.className += " responsive";
    } else {
        x.className = "navigationclass";
    }
}
function clickFunction(date){
    document.getElementById('details').style.display = "table";
    document.getElementById('detailstitle').innerHTML = "Details for " + date + " (still in development)";
    document.getElementById('paragraphinfo').innerHTML = "Data descriptions will be shown here"
    document.getElementById('paragraphdata').innerHTML = "Weather data will be shown here"
}
function getDate(){
    return document.getElementById('date').innerHTML;
}