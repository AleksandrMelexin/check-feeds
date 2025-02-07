function getReport(){
//    const xhr = new XMLHttpRequest();
//    xhr.open("GET", "/report", true);
//    xhr.send();
//    alert("Отчёт готов!");
fetch("/report")
  .then( res => res.blob() )
  .then( blob => {
    const file = window.URL.createObjectURL(blob);
    window.location.assign(file);
  });
}