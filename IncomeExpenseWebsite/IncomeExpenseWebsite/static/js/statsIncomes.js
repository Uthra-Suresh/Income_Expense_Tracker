const timelimit = document.getElementById("timelimit");

timelimit.addEventListener('change',(e)=>{
    const days = e.target.value;
    console.log("days",days);
    getSourceChartData(days);
});

const getSourceChartData=(days)=>{
    fetch("/income/sourcesummary-incomes",{
        body:JSON.stringify({timelimit: days}),
        method: "POST",})
    .then(res=>res.json())
    .then((results)=>{
        console.log("results",results);
        const source_data = results.income_source_data;
        const [label, data] =[Object.keys(source_data),
            Object.values(source_data)];
    renderSourceChart(data,label);
});
}


const renderSourceChart=(data,labels)=>{
    const ctx = document.getElementById('ChartSource').getContext('2d');
    const ChartSource = new Chart(ctx, {
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
                      'rgba(255, 159, 64, 0.2)'
                  ],
                  borderColor: [
                      'rgba(255, 99, 132, 1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)',
                      'rgba(255, 159, 64, 1)'
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              title:{
                  display:true,
                  text:'Incomes per source'
              }
          }
      });
}

const getMonthChartData=()=>{
    
    fetch("/income/monthsummary-incomes")
    .then(res=>res.json())
    .then((results)=>{
        console.log("results",results);
        const month_data = results.income_month_data;
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
                  text:'Incomes per month'
              }
          }
      });
}


document.onload = getMonthChartData();
