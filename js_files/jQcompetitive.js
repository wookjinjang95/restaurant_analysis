//this is for the positive review bar transition..
var total = 1226+193;
var p_total = 1226;
var n_total = 193;

$({ Counter: 0 }).animate({
  Counter: p_total
  },{
    duration: 1000,
    easing: 'swing',
    step: function() {
      $('.p_total_ticker_right').text(this.Counter.toFixed(0));
      var percentage = this.Counter/total;
      $('.p_total_ticker_right').width(percentage*415);
    }
});

//this is for negative review bar transition
$({ Counter: 0 }).animate({
  Counter: n_total
  },{
    duration: 1000,
    easing: 'swing',
    step: function() {
      $('.n_total_ticker_right').text(this.Counter.toFixed(0));
      var percentage = this.Counter/total;
      $('.n_total_ticker_right').width(percentage*415);
    }
});

//this is for expectin review bar transition
var max = 5;
var expect = 4.34;

$({ Counter: 0 }).animate({
  Counter: expect
  },{
    duration: 1000,
    easing: 'swing',
    step: function() {
      $('.expecting_reviews_right').text(this.Counter.toFixed(2));
      var percentage = this.Counter/max;
      $('.expecting_reviews_right').width(percentage*415);
    }
});

//this is for average rating bar transition
var average = 4.5;

$({ Counter: 0 }).animate({
  Counter: average
  },{
    duration: 1000,
    easing: 'swing',
    step: function() {
      $('.average_rating_right').text(this.Counter.toFixed(2));
      var percentage = this.Counter/max;
      $('.average_rating_right').width(percentage*415);
    }
});
