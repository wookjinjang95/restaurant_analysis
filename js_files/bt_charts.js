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
]};

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
};

var pos_fd = [
  {"word": "food", "count": 57},
  {"word": "great", "count": 51},
  {"word": "japanese", "count": 41},
  {"word": "place", "count": 38},
  {"word": "restaurant", "count": 32},
  {"word": "wait", "count": 30},
  {"word": "good", "count": 30},
  {"word": "izakaya", "count": 28},
  {"word": "service", "count": 28},
  {"word": "get", "count": 26}
];

var neg_fd = [
  {"word": "wait", "count": 7},
  {"word": "food", "count": 7},
  {"word": "really", "count": 4},
  {"word": "rice", "count": 3},
  {"word": "much", "count": 3},
  {"word": "service", "count": 3},
  {"word": "sign", "count": 3},
  {"word": "waiting", "count": 3},
  {"word": "salmon", "count": 2},
  {"word": "collar", "count": 2}
];

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
};
for(var i = 0; i < n_reviews.negative.length; i++){
  n_data_total += n_reviews.negative[i].count;
};

//this is where the data for negative frequent Dist..
var negative_freq_words = neg_fd.map(function(e){
  return e.word;
});

var negative_freq_words_count = neg_fd.map(function(e){
  return e.count;
});

var positive_freq_words = pos_fd.map(function(e){
  return e.word;
});

var positive_freq_words_count = pos_fd.map(function(e){
  return e.count;
})

//var ctxL = document.getElementById("lineChart").getContext('2d');
var ctxP = document.getElementById("pieChart").getContext('2d');

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
      backgroundColor: ['rgba(54, 162, 235, 0.8)','rgba(255, 99, 132, 0.8 )'],
      fill: true
    }]
  }
};

//var myLineChart = new Chart(ctxL, line_config);
var myPieChart = new Chart(ctxP, pie_config);

//these are for the horizontalbar
var ctxNeg_Bar = document.getElementById("negBarChart");
var ctxPos_Bar = document.getElementById("posBarChart");

var neg_bar_config = {
  type: 'horizontalBar',
  data: {
    labels: negative_freq_words,
    datasets: [{
      label: "# of Words in Negative Comments",
      data: negative_freq_words_count,
      backgroundColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(255, 99, 132, 0.9)',
            'rgba(255, 99, 132, 0.8)',
            'rgba(255, 99, 132, 0.7)',
            'rgba(255, 99, 132, 0.6)',
            'rgba(255, 99, 132, 0.5)',
            'rgba(255, 99, 132, 0.4)',
            'rgba(255, 99, 132, 0.3)',
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 99, 132, 0.1)'
      ]
    }],
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  }
};

var pos_bar_config = {
  type: 'horizontalBar',
  data: {
    labels: positive_freq_words,
    datasets: [{
      label: "# of Words in Positive Comments",
      data: positive_freq_words_count,
      backgroundColor: [
            'rgba(54, 162, 235, 1)',
            'rgba(54, 162, 235, 0.9)',
            'rgba(54, 162, 235, 0.8)',
            'rgba(54, 162, 235, 0.7)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(54, 162, 235, 0.5)',
            'rgba(54, 162, 235, 0.4)',
            'rgba(54, 162, 235, 0.3)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(54, 162, 235, 0.1)'
      ]
    }]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  }
};

//this is is setup for horizontal frequency bar
var myNegFreqBar = new Chart(ctxNeg_Bar, neg_bar_config);
var myNegFreqBar = new Chart(ctxPos_Bar, pos_bar_config);

//this is a text for the report on home
var total_reviews = p_data_total + n_data_total;

var p_desc = "After scraping data of your reviews, we found out that you have totla of " + total_reviews
+ " reviews. Out of " + total_reviews + " reviews, " + p_data_total + " reviews are positive and " +
n_data_total + " reviews are negative reviews."

$("#pie_description").text(p_desc);
//var text_canvas = document.getElementById("pie_description").getContext("2d");
//text_canvas.font = "12px Arial";
//text_canvas.fillText(p_desc, 10, 50)
