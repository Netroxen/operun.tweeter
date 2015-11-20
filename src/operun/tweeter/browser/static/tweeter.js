if (window.jQuery) {
  define('jquery', [], function() {
    return window.jQuery;
  });
}

require([
  'jquery',
  'counterup',
  'waypoints'
], function($) {
  'use strict';

  // Enter Content Here
  $('.counter').counterUp({
    delay: 10,
    time: 1000
  });

});
