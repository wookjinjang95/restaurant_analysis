labels = [
  "megabyte (Small Storage)",
  "gigabyte (USB Storage)",
  "terabyte (Computer Storage)",
  "petabyte (Server Storage)",
  "zettabytes (Global Storage)"
]

var data = [
  1,
  1000,
  1000000,
  1000000000,
  1000000000000000
]

var data_comp_bar = document.getElementById("dcb").getContext('2d');

var data_bar_config = {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: "data size comparison",
      data: data,
      backgroundColor: [
            'rgba(252, 0, 0, 0.6)',
            'rgba(252, 0, 0, 0.7)',
            'rgba(252, 0, 0, 0.8)',
            'rgba(252, 0, 0, 0.9)',
            'rgba(252, 0, 0, 1)'
      ]
    }],
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          min: 0,
          max: 1000000000000000,
       },
       type: "logarithmic",
       afterFit: function(scale) {
         scale.width = 100 //<-- set value as you wish
       }
      }]
    }
  }
};

var display_data_bar = new Chart(data_comp_bar, data_bar_config);
