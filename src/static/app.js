
(function() {
  var socket, scenario, nextScenario;

  function action(id) {
    return JSON.stringify({scenario: scenario, action: id});
  }

  function onMessage(evt) {
    var data = JSON.parse(evt.data);
    console.log(data);
    switch (data.status) {
      case 'scenario-ready':
        break;
      case 'scenario-done':
        if (nextScenario) {
          location.replace("/"+nextScenario);
        }
        break;
    }
  }

  function onOpen(evt) {
    socket.send(action("start"))
  }

  function changeScenario(sc) {
    nextScenario = sc;
    socket.send(action("stop"));
  }

  function openConnection() {
    socket = new WebSocket("ws://" + location.host + "/gator");
    socket.onopen = onOpen;
    socket.onmessage = onMessage;
  }

  function onActionButtonClick(evt) {
    socket.send(action(evt.target.id));
  }

  function init() {
    actions = document.getElementsByClassName('kgc-action-button');
    for (var i = 0; i < actions.length; i++)
      actions[i].onclick = onActionButtonClick;
    if (actions.length > 0) {
      scenario = actions[0].id.replace(/-.*$/,'');
      openConnection();
    }
  }

  init();
})();
