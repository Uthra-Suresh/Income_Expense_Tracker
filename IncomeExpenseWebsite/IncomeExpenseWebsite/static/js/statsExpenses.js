const timelimit = document.getElementById("timelimit");

timelimit.addEventListener('change',(e)=>{
    const days = e.target.value;
    console.log("days",days);
    getCategoryChartData(days);
});

const getCategoryChartData=(days)=>{
    console.log("days",days);
    
    fetch("/categorysummary-expenses",{
        body:JSON.stringify({timelimit: days}),
        method: "POST",})
    .then(res=>res.json())
    .then((results)=>{
        console.log("results",results);
        const category_data = results.expense_category_data;
        const [label, data] =[Object.keys(category_data),
            Object.values(category_data)];
    renderCategoryChart(data,label);
});
}

const renderCategoryChart=(data,labels)=>{
    const ctx = document.getElementById('ChartCategory').getContext('2d');
    const ChartCategory = new Chart(ctx, {
          type: 'doughnut',
          data: {
              labels: labels,
              datasets: [{
                  data: data,
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(255, 206, 86, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(153, 102, 255, 0.2)',
                      'rgba(255, 159, 64, 0.2)',
                      'rgba(153, 102, 255, 0.2)',
                      'rgba(245, 184, 217, 0.2)',
                      'rgba(199, 105, 105, 0.2)',

                  ],
                  borderColor: [
                      'rgba(255, 99, 132, 1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)',
                      'rgba(255, 159, 64, 1)',
                      'rgba(245, 184, 217, 1)',
                      'rgba(199, 105, 105, 1)',
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              title:{
                  display:true,
                  text:'Expenses per category'
              }
          }
      });
}


const getMonthChartData=()=>{
    
    fetch("/monthsummary-expenses")
    .then(res=>res.json())
    .then((results)=>{
        console.log("results",results);
        const month_data = results.expense_month_data;
        const [label, data] =[Object.keys(month_data),
            Object.values(month_data)];
    renderMonthChart(data,label);
});
}

const renderMonthChart=(data,labels)=>{
    const ctx = document.getElementById('ChartMonth').getContext('2d');
    const ChartMonth = new Chart(ctx, {
          type: 'line',
          data: {
              labels: labels,
              datasets: [{
                  data: data,
                  label: "Amount Spent",
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                  ],
                  borderColor: [
                      'rgba(255, 99, 132, 1)',
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              title:{
                  display:true,
                  text:'Expenses per month'
              }
          }
      });
}


document.onload = getMonthChartData();
