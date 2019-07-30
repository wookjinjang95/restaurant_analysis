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
