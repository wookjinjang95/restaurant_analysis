var p_reviews = {"positive":[
    {"time": "7 years", "count": 1},
    {"time": "6 years", "count": 4},
    {"time": "5 years", "count": 10},
    {"time": "4 years", "count": 6},
    {"time": "3 years", "count": 17},
    {"time": "2 years", "count": 48},
    {"time": "a year", "count": 122},
    {"time": "11 months", "count": 12},
    {"time": "10 months", "count": 7},
    {"time": "9 months", "count": 7},
    {"time": "8 months", "count": 6},
    {"time": "7 months", "count": 11},
    {"time": "6 months", "count": 7},
    {"time": "5 months", "count": 11},
    {"time": "4 months", "count": 12},
    {"time": "3 months", "count": 7},
    {"time": "2 months", "count": 11},
    {"time": "a month", "count": 15},
    {"time": "4 weeks", "count": 2},
    {"time": "3 weeks", "count": 3},
    {"time": "2 weeks", "count": 1},
    {"time": "a week", "count": 2}
]}

var n_reviews = {"negative":
[{"time": "7 years", "count": 0},
  {"time": "6 years", "count": 1},
  {"time": "5 years", "count": 0},
  {"time": "4 years", "count": 0},
  {"time": "3 years", "count": 2},
  {"time": "2 years", "count": 1},
  {"time": "a year", "count": 14},
  {"time": "11 months", "count": 0},
  {"time": "10 months", "count": 1},
  {"time": "9 months", "count": 3},
  {"time": "8 months", "count": 1},
  {"time": "7 months", "count": 0},
  {"time": "6 months", "count": 1},
  {"time": "5 months", "count": 7},
  {"time": "4 months", "count": 2},
  {"time": "3 months", "count": 2},
  {"time": "2 months", "count": 1},
  {"time": "a month", "count": 3},
  {"time": "4 weeks", "count": 0},
  {"time": "3 weeks", "count": 1},
  {"time": "2 weeks", "count": 0},
  {"time": "a week", "count": 0}]
}

var labels = p_reviews.positive.map(function(e){
  return e.time;
});

var p_data = p_reviews.positive.map(function(e){
  return e.count;
});

var n_data = n_reviews.negative.map(function(e){
  return e.count;
});

var p_data_total = 0;
var n_data_total = 0;

for(var i = 0; i < p_reviews.positive.length; i++){
  p_data_total += p_reviews.positive[i].count;
}
for(var i = 0; i < n_reviews.negative.length; i++){
  n_data_total += n_reviews.negative[i].count;
}

var ctxL = document.getElementById("lineChart").getContext('2d');
//var ctxP = document.getElementById("pieChart").getContext('2d');

var line_config = {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{
      label: 'positive reviews',
      backgroundColor: 'rgb(135,206,250, 0.3)',
      borderColor: "blue",
      fill: true,
      data: p_data
    },{
      label: 'negative reviews',
      backgroundColor: 'rgb(255,99,71, 0.7)',
      borderColor: "red",
      fill: true,
      data: n_data
    }]
  }
};

var pie_config = {
  type: 'pie',
  data: {
    labels: ['positive reviews', 'negative reviews'],
    datasets: [{
      data: [p_data_total, n_data_total],
      backgroundColor: ['rgb(135,206,250, 0.3)','rgb(255,99,71, 0.7)'],
      fill: true,
      borderColor: 'black'
    }]
  }
};

var myLineChart = new Chart(ctxL, line_config);
//var myPieChart = new Chart(ctxP, pie_config);
