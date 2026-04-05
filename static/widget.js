(function () {
  const script = document.currentScript;
  const agentId = script.getAttribute("data-agent-id");

  // BUTTON
  const button = document.createElement("div");
  button.innerHTML = `💬`;

  Object.assign(button.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    width: "56px",
    height: "56px",
    background: "#18181b",
    color: "white",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    zIndex: "9999"
  });

  document.body.appendChild(button);

  // IFRAME (ONLY SIZE + POSITION)
  const iframe = document.createElement("iframe");
  iframe.src = `https://flowtai-1.onrender.com/chat-widget?agent_id=${agentId}`;

  Object.assign(iframe.style, {
    position: "fixed",
    bottom: "90px",
    right: "20px",
    width: "380px",
    height: "560px",
    border: "none",
    borderRadius: "24px",
    display: "none",
    zIndex: "9999"
  });

  document.body.appendChild(iframe);

  // TOGGLE
  let isOpen = false;

  button.onclick = () => {
    isOpen = !isOpen;
    iframe.style.display = isOpen ? "block" : "none";
  };
})();
