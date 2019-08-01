var p_reviews = {"positive":[
    {"time": "7 years ago", "count": 1},
    {"time": "6 years ago", "count": 4},
    {"time": "5 years ago", "count": 10},
    {"time": "4 years ago", "count": 6},
    {"time": "3 years ago", "count": 17},
    {"time": "2 years ago", "count": 48},
    {"time": "1 years ago", "count": 122},
    {"time": "0 years ago", "count": 114}
]};

var n_reviews = {"negative":
[{"time": "7 years ago", "count": 0},
  {"time": "6 years ago", "count": 1},
  {"time": "5 years ago", "count": 0},
  {"time": "4 years ago", "count": 0},
  {"time": "3 years ago", "count": 2},
  {"time": "2 years ago", "count": 1},
  {"time": "1 years ago", "count": 14},
  {"time": "0 years ago", "count": 22}]
};

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

var pos_yelp_reviews =
  {"8 years ago": 41,
    "7 years ago": 79,
    "6 years ago": 78,
    "5 years ago": 129,
    "4 years ago": 125,
    "3 years ago": 110,
    "2 years ago": 157,
    "1 years ago": 115,
    "0 years ago": 73
};

var neg_yelp_reviews =
  {"8 years ago": 6,
    "7 years ago": 14,
    "6 years ago": 15,
    "5 years ago": 14,
    "4 years ago": 28,
    "3 years ago": 14,
    "2 years ago": 29,
    "1 years ago": 18,
    "0 years ago": 15
};


var yelp_labels = [];
var yelp_p_data = [];
var yelp_n_data = [];

for(var key in pos_yelp_reviews){
  yelp_labels.push(key);
  yelp_p_data.push(pos_yelp_reviews[key]);
  yelp_n_data.push(neg_yelp_reviews[key]);
}

var ctxY = document.getElementById("yelpChart").getContext('2d');
var ctxG = document.getElementById("googleChart").getContext('2d');

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
  },
  options: {
    responsive: true
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

var yelp_line_config = {
  type: "line",
  data: {
    labels: yelp_labels,
    datasets: [{
      label: 'positive reviews',
      backgroundColor: 'rgb(135,206,250, 0.3)',
      borderColor: "blue",
      fill: true,
      data: yelp_p_data
    },{
      label: 'negative reviews',
      backgroundColor: 'rgb(255,99,71, 0.7)',
      borderColor: "red",
      fill: true,
      data: yelp_n_data
    }]
  },
  options: {
    responsive: true
  }
};

var myLineChart = new Chart(ctxY, yelp_line_config);
var myLineChart = new Chart(ctxG, line_config);
//var myPieChart = new Chart(ctxP, pie_config);

//the below code is JQuery for total positive and negative reviews

var yelp_pos_total = p_data_total;
var yelp_neg_total = n_data_total;

for(var key in pos_yelp_reviews){
  yelp_pos_total += pos_yelp_reviews[key];
}
for(var key in neg_yelp_reviews){
  yelp_neg_total += neg_yelp_reviews[key];
}

$({ Counter: 0 }).animate({
  Counter: yelp_pos_total
  },{
    duration: 1000,
    easing: 'swing',
    step: function() {
      $('.posTicker').text(this.Counter.toFixed(0));
      var value = this.Counter;
      if( value < 10){
        $('.posTicker').css('color', 'red');
      }else if( value >= 10 && value < 100){
        $('.posTicker').css('color', 'orange');
      }else if( value >= 100 && value < 500){
        $('.posTicker').css('color', 'brown');
      }else if( value >= 500){
        $('.posTicker').css('color', 'green');
      }
    }
});

$({ Counter: 0 }).animate({
  Counter: yelp_neg_total
  },{
    duration: 1000,
    easing: 'swing',
    step: function() {
      $('.negTicker').text("/"+this.Counter.toFixed(0));
      var value = this.Counter;
      if( value < 10){
        $('.negTicker').css('color', 'green');
      }else if( value >= 10 && value < 100){
        $('.negTicker').css('color', 'brown');
      }else if( value >= 100 && value < 500){
        $('.negTicker').css('color', 'orange');
      }else if( value >= 500){
        $('.negTicker').css('color', 'red');
      }
    }
});

//here remember that the number 4.34 is fixed..
$({ Counter: 0 }).animate({
  Counter: $('.numTicker').text()
  },{
    duration: 3000,
    easing: 'swing',
    step: function() {
      $('.numTicker').text(this.Counter.toFixed(2));
      var value = parseInt($('.numTicker').text());
      if( value < 1){
        $('.numTicker').css('color', 'red');
      }else if( value >= 1 && value < 2){
        $('.numTicker').css('color', 'orange');
      }else if( value >= 2 && value < 3){
        $('.numTicker').css('color', 'brown');
      }else if( value >= 3){
        $('.numTicker').css('color', 'green');
      }
    }
});
