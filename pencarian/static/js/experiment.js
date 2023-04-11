
const inputQuery = document.getElementById("query");
inputQuery.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        doQuery();
    }
});

var numberResult=0;



function  saveJson(){
    let json=new Object();
    let query=document.getElementById("query").value;
    json.query=query

    let result=[]
    for(let i = 0; i < numberResult; i++){
        let row=document.getElementsByClassName(i);

        let dict = {
            noFile: row[0].textContent.trim(),
            noParagraf: row[1].textContent.trim(),
            relevan: row[4].checked
          };

          result.push(dict)
    }

    console.log(result)

    json.result=result


    let jsonString= JSON.stringify(json,null,null);

    fetch(`${window.location.origin}/save?save=${jsonString}`).then(response => response.text()) .then(response=>{
        
        let json=JSON.parse(response);

        let hasil=json['result']

        if(hasil){
            document.getElementById("notifSave").hidden=false
            document.getElementById("kotakTabel").hidden=true
        }else{
            alert("gagal menyimpan! harap kirimkan file ini")
            const a = document.createElement("a");
            const file = new Blob([jsonString], { type: "application/json" });
            a.href = URL.createObjectURL(file);
            a.download = query+".json"; // max 256 mungkin problem (?)
            a.click();
        }


    });

    


    // const a = document.createElement("a");
    // const file = new Blob([jsonString], { type: "application/json" });
    // a.href = URL.createObjectURL(file);
    // a.download = query+".json"; // max 256 mungkin problem (?)
    // a.click();

}

function openDetail(element){
    let clickedClass=element.className
    
    let content=document.getElementsByClassName(clickedClass)
    let judul=content[2].textContent+" - Paragraf "+content[1].textContent
   
    let header=document.getElementById("modalLabel")
    header.innerHTML=judul

    let isi=document.getElementById("isi-modal")
    isi.innerHTML=content[3].textContent

    document.getElementById("btnModal").click()
    }


    function doQuery(){
        let strQuery=inputQuery.value;
    

        document.getElementById("notifSave").hidden=true
        let box=document.getElementById("kotakTabel");
        box.hidden=true
        let spinner=document.getElementById("spinner")
        spinner.classList.toggle("d-none")
        spinner.classList.toggle("d-flex")
    
    
        fetch(`${window.location.origin}/search?query=${strQuery}`).then(response => response.text()) .then(response=>{
            
            let json=JSON.parse(response);
            let data=json['data']

            numberResult=Object.keys(data).length
    
            for (let i = 0; i < numberResult ; i++) {
                let allClass=document.getElementsByClassName(i)
                
                
    
                allClass[0].firstElementChild .textContent=data[i]['noFile'];
                allClass[1].firstElementChild .textContent=data[i]['noParagraf'];
                allClass[2].firstElementChild .textContent=data[i]['Judul'];
                allClass[3].firstElementChild .textContent=data[i]['Teks'];
    
                

                allClass[4].checked = false;
    
                allClass=allClass[0].parentNode;
                allClass.hidden=false;
            }
    
    
    
    
        document.getElementById("disclaimer").textContent=(`**tabel berisi top ${numberResult} pencarian`);
        box.removeAttribute("hidden"); 
        spinner.classList.toggle("d-flex")
        spinner.classList.toggle("d-none")
    
    
    
    
    
    
      
    
        });
    
    
    
    }