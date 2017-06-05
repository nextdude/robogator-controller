(function(){
  var socket, scenario, actions;

  function _incomingMessage(evt) {
    var data = JSON.parse(evt.data);
    onMessage(data);
  }

  function _openConnection() {
    socket = new WebSocket("ws://" + location.host + "/gator");
    socket.onopen = onOpen;
    socket.onmessage = onMessage;
  }

  window.sendMessage = function(data) {
    data.scenario = scenario;
    socket.send(JSON.stringify(data));
  }

  window.connect = function () {
    scenario = document.getElementsByClassName('kgc-scenario')[0].id;
    actions = document.getElementsByClassName('kgc-action-button');
    if (actions.length > 0 && typeof onAction == 'function') {
      for (var i = 0; i < actions.length; i++) {
        _.forEach(['click','mousedown','mouseup','keydown','keyup',
              'touchstart','touchend','touchcancel','touchmove'], function(etype){
          actions[i].addEventListener(etype, onAction)
        });
      }
      _openConnection();
    }
  };

  window.disableActions = function() {
    _.forEach(action, function(btn) {
      btn.disabled = true;
    });
  };

  window.enableActions = function() {
    _.forEach(action, function(btn) {
      btn.disabled = false;
    });
  };

  window.toggleActions = function(onOff) {
    _.forEach(action, function(btn) {
      btn.disabled = !!onOff;
    });
  };


  _init();

})();
