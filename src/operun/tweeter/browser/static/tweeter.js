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
    delay: 5,
    time: 500
  });

});
