(function () {
  const script = document.currentScript;
  const agentId = script.getAttribute("data-agent-id");

  // BUTTON
  const button = document.createElement("div");
  button.innerHTML = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
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
    background: "#18181b",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    zIndex: "9999",
    boxShadow: "0 8px 20px rgba(0,0,0,0.2)",
    transition: "all 0.2s ease"
  });

  button.onmouseenter = () => {
    button.style.transform = "scale(1.06)";
  };
  button.onmouseleave = () => {
    button.style.transform = "scale(1)";
  };

  document.body.appendChild(button);

  // ✅ CREATE IFRAME FIRST
  const iframe = document.createElement("iframe");
  iframe.src = `https://flowtai-1.onrender.com/chat-widget?agent_id=${agentId}`;

  // ✅ APPLY STYLE ONCE
  Object.assign(iframe.style, {
    position: "fixed",
    bottom: "90px",
    right: "20px",

    width: "380px",
    height: "560px",

    border: "1px solid rgba(255,255,255,0.25)",
    borderRadius: "24px",

    // glass shell
    background: "rgba(255,255,255,0.08)",
    backdropFilter: "blur(16px)",
    WebkitBackdropFilter: "blur(16px)",

    boxShadow: "0 25px 60px rgba(0,0,0,0.25)",

    display: "none",
    zIndex: "9999",
    overflow: "hidden",

    transform: "translateY(20px) scale(0.98)",
    opacity: "0",
    transition: "all 0.25s ease"
  });

  document.body.appendChild(iframe);

  // TOGGLE
  let isOpen = false;

  button.onclick = () => {
    isOpen = !isOpen;

    if (isOpen) {
      iframe.style.display = "block";

      requestAnimationFrame(() => {
        iframe.style.transform = "translateY(0) scale(1)";
        iframe.style.opacity = "1";
      });

    } else {
      iframe.style.transform = "translateY(20px) scale(0.98)";
      iframe.style.opacity = "0";

      setTimeout(() => {
        iframe.style.display = "none";
      }, 200);
    }
  };
})();
