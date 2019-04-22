// $(document).ready(function(){
  let loc = window.location
  let wsStart = 'ws://'
  if (loc.protocol == "https:") {
    wsStart = 'wss://'
  }
let endpoint = wsStart + loc.host + loc.pathname

console.log(loc);

let socket = new WebSocket(endpoint);
socket.onmessage = function(e){
    console.log('message', e);
}

socket.onopen = function(e) {
      console.log('open',e);
}

// })
