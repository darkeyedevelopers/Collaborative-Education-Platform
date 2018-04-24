var wsaddr = window.location.host;
var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
var path = window.location.pathname.replace(/\/$/, "");
var wsUri = ws_scheme + "://" + wsaddr + path + "/ws/?rohit";
var websocket;
var name;
var targetname;

function start() {
    name = document.getElementById('username').value;
    wsaddr = window.location.host;
    ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    path = window.location.pathname.replace(/\/$/, "");
    wsUri = ws_scheme + "://" + wsaddr + path + "/ws/?"+name;
}

function setupWebSocket() {
  websocket = new WebSocket(wsUri);
  websocket.onopen = function(evt) { onOpen(evt) };
  websocket.onmessage = function(evt) { onMessage(evt) };
}

function onMessage(evt) {
    var msg = JSON.parse(evt.data);
    var time = new Date(msg.date);
    var timeStr = time.toLocaleTimeString();

    switch(msg.type) {
      case "video-offer":
        handleVideoOfferMsg(msg);
        break;
      case "video-answer":
          handleVideoAnswerMsg(msg);
          break;
      case "new-ice-candidate":
        handleNewICECandidateMsg(msg);
        break;
      case "hang-up":
        closeVideoCall();
        break;
    }
}

function onOpen (evt) {
  console.log("Connected to websocket!");
}
