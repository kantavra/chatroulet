let localStream;
let peerConnection;
const websocket = new WebSocket("ws://localhost:8000/ws");

const configuration = {
    iceServers: [
        { urls: "stun:stun.l.google.com:19302" } // STUN-сервер для получения ICE-кандидатов
    ]
};

websocket.onopen = function() {
    console.log("Соединение с сервером установлено");
};

websocket.onmessage = async function(event) {
    const message = JSON.parse(event.data);
    if (message.offer) {
        await handleOffer(message.offer);
    } else if (message.answer) {
        await handleAnswer(message.answer);
    } else if (message.iceCandidate) {
        await handleICECandidate(message.iceCandidate);
    }
};

async function startChat() {
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    document.getElementById('localVideo').srcObject = localStream;

    peerConnection = new RTCPeerConnection(configuration);
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

    peerConnection.onicecandidate = event => {
        if (event.candidate) {
            websocket.send(JSON.stringify({ iceCandidate: event.candidate }));
        }
    };

    peerConnection.ontrack = event => {
        const remoteVideo = document.getElementById('remoteVideo');
        if (remoteVideo.srcObject !== event.streams[0]) {
            remoteVideo.srcObject = event.streams[0];
        }
    };

    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    websocket.send(JSON.stringify({ offer: offer }));
}

async function handleOffer(offer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    websocket.send(JSON.stringify({ answer: answer }));
}

async function handleAnswer(answer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
}

async function handleICECandidate(candidate) {
    await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
}
