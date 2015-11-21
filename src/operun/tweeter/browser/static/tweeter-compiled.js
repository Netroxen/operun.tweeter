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

  $('.counter').click(function() {
    alert( "Handler for .click() called." );
  });

  $('.counter').counterUp({
    delay: 10,
    time: 1000
  });

});
