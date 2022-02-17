const searchField=document.querySelector('#searchField');

const tableSearchOutput=document.querySelector(".table-search-output");
tableSearchOutput.style.display ="none";

const tableAllOutput=document.querySelector(".table-all-output");

const paginationContainer = document.querySelector(".pagination-container");

const tableSearchBody=document.querySelector(".table-search-body");

const noResults = document.querySelector(".no-results");

searchField.addEventListener('keyup',(e)=>{
    const searchValue=e.target.value;

    if(searchValue.trim().length >0) {
        paginationContainer.style.display = "none";
        tableSearchBody.innerHTML="";
        fetch("/income/search-incomes",{
            body:JSON.stringify({searchText: searchValue}),
            method: "POST",
        }).then((res) => res.json())
          .then((data) => {
           console.log("data",data);
           tableAllOutput.style.display="none";
           tableSearchOutput.style.display="block";

           if(data.length == 0){
            noResults.style.display = "block";
            tableSearchOutput.style.display="none";

           }else{
            noResults.style.display = "none";
            data.forEach((item)=>{
                tableSearchBody.innerHTML += `
                <tr>
                <td>${item.id}</td>
                <td>${item.amount}</td>
                <td>${item.source}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
               
                </tr>`;
               });
           }
                });
            }else{
           tableAllOutput.style.display="block";
           paginationContainer.style.display = "block";
           tableSearchOutput.style.display="none";

            }
        });
                   
