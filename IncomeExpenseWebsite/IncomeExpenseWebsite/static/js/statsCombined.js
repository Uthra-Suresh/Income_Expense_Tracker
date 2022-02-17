

document.onload = getCombinedMonthChartData();
function getCombinedMonthChartData(){

    fetch("/monthsummary-expenses")
    .then(res=>res.json())
    .then((results)=>{
        //console.log("results",results);
        const month_data = results.expense_month_data;
        const [label_expense,data_expense] =[Object.keys(month_data),
            Object.values(month_data)];
        // label_expense = label;
        // data_expense = data;
        //console.log("data_expense",data_expense)
        //console.log("label_expense",label_expense)
        fetch("/income/monthsummary-incomes")
        .then(res=>res.json())
        .then((results)=>{
        console.log("results",results);
        const month_data = results.income_month_data;
        const[label_income, data_income] =[Object.keys(month_data),
            Object.values(month_data)];
        // label_income=label;
        // data_income=data;
        renderCombinedMonthChart(label_expense,data_expense,label_income, data_income);
        });
        });
     
    
        
    
    }

function renderCombinedMonthChart(label_expense,data_expense,label_income, data_income){
    if(label_expense.length > label_income.length){
        labels_c= label_expense;
    }else{
        labels_c= label_income;
    }
    console.log("data_expense",data_expense)
    //console.log("label_c",label_c)


    const ctx = document.getElementById('ChartMonthCombined').getContext('2d');
    const ChartMonth = new Chart(ctx, {
        type:'line',
          data: {
              
              datasets: [{
                  data: data_expense,
                  label: "Expenses",
                  backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',

                ],
                  borderColor: [
                      'rgba(255, 99, 132, 1)',
                  ],
                  borderWidth: 1
              },{
                  data: data_income,
                  label: "Incomes",
                  backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',

                ],
                  borderColor: [
                    'rgba(54, 162, 235, 1)',
                  ],
                  borderWidth: 1  
              }],
              labels: label_expense,
             
          },
          options: {
              title:{
                  display:true,
                  text:'Expenses vs Income'
              }
          }
      });
}


