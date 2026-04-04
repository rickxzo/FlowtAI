(function () {
  const script = document.currentScript;
  const agentId = script.getAttribute("data-agent-id");

  // Chat Button
  const button = document.createElement("div");
  button.innerHTML = `
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
      <path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z"
        stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `;

  Object.assign(button.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    width: "56px",
    height: "56px",
    background: "#18181b", // zinc-900
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    zIndex: "9999",
    boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
    transition: "all 0.2s ease"
  });

  // Hover effect
  button.onmouseenter = () => {
    button.style.transform = "scale(1.05)";
  };
  button.onmouseleave = () => {
    button.style.transform = "scale(1)";
  };

  document.body.appendChild(button);

  // Iframe
  const iframe = document.createElement("iframe");
  iframe.src = `https://flowtai-1.onrender.com/chat-widget?agent_id=${agentId}`;

  Object.assign(iframe.style, {
    position: "fixed",
    bottom: "90px",
    right: "20px",
    width: "360px",
    height: "520px",
    border: "1px solid #e4e4e7", // subtle border
    borderRadius: "20px",
    display: "none",
    zIndex: "9999",
    background: "#fff",
    boxShadow: "0 20px 50px rgba(0,0,0,0.15)",
    overflow: "hidden"
  });

  document.body.appendChild(iframe);

  // Toggle
  let isOpen = false;

  button.onclick = () => {
    isOpen = !isOpen;
    iframe.style.display = isOpen ? "block" : "none";

    // subtle animation
    if (isOpen) {
      iframe.style.transform = "translateY(10px)";
      iframe.style.opacity = "0";

      setTimeout(() => {
        iframe.style.transition = "all 0.2s ease";
        iframe.style.transform = "translateY(0)";
        iframe.style.opacity = "1";
      }, 10);
    }
  };
})();
