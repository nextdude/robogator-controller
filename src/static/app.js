(function(){
  var socket, scenario, actions;

  function _incomingMessage(evt) {
    var data = JSON.parse(evt.data);
    onMessage(data);
  }

  function _openConnection() {
    socket = new WebSocket("ws://" + location.host + "/gator");
    socket.onopen = onOpen;
    socket.onmessage = _incomingMessage;
  }

  window.sendMessage = function(data) {
    data.scenario = scenario;
    console.log('sending',data);
    socket.send(JSON.stringify(data));
  }

  function _init() {
    scenario = document.getElementsByClassName('kgc-scenario')[0].id;
    actions = document.getElementsByTagName('button');
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
