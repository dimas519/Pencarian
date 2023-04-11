
const inputQuery = document.getElementById("query");
inputQuery.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        doQuery();
    }
});

var numberResult=0;


function doQuery(){
    let strQuery=inputQuery.value;
    document.getElementById("tagPencarian").hidden=false

    let box=document.getElementById("kotakTabel");
    box.classList.add("d-none")
    box.classList.remove("d-flex")



    let spinner=document.getElementById("spinner")
    spinner.classList.toggle("d-none")
    spinner.classList.toggle("d-flex")
    let time=document.getElementById("timePencarian");
    time.hidden=true;



    fetch(`${window.location.origin}/search?query=${strQuery}`).then(response => response.text()) .then(response=>{
        


        let json=JSON.parse(response);
        let data=json['data']

        numberResult=Object.keys(data).length

        for (let i = 0; i < numberResult ; i++) {
            let allClass=document.getElementsByClassName(i)
            


            let judul= `${data[i]['Judul']} - Paragraf ${data[i]['noParagraf']}`
            allClass[0].textContent=judul;
            allClass[1].textContent=data[i]['Teks'];


            allClass=allClass[0].parentNode;
            allClass=allClass.parentNode;
            allClass.hidden=false;
            spinner.hidden=true;

        }

        
        time.textContent=`(${json['time']} seconds)`;
        time.hidden=false;
        spinner.classList.toggle("d-flex")
        spinner.classList.toggle("d-none")

        let box=document.getElementById("kotakTabel");
        box.classList.remove("d-none")
        box.classList.add("d-flex")








  

    });



}