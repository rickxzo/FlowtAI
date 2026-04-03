
(function () {
  const script = document.currentScript;
  const agentId = script.getAttribute("data-agent-id");

  // Create chat button
  const button = document.createElement("div");
  button.innerText = "💬";
  button.style.position = "fixed";
  button.style.bottom = "20px";
  button.style.right = "20px";
  button.style.width = "60px";
  button.style.height = "60px";
  button.style.background = "#000";
  button.style.color = "#fff";
  button.style.borderRadius = "50%";
  button.style.display = "flex";
  button.style.alignItems = "center";
  button.style.justifyContent = "center";
  button.style.cursor = "pointer";
  button.style.zIndex = "9999";

  document.body.appendChild(button);

  // Create iframe (hidden initially)
  const iframe = document.createElement("iframe");
  iframe.src = `https://flowtai-1.onrender.com/chat-widget?agent_id=${agentId}`;
  iframe.style.position = "fixed";
  iframe.style.bottom = "90px";
  iframe.style.right = "20px";
  iframe.style.width = "350px";
  iframe.style.height = "500px";
  iframe.style.border = "none";
  iframe.style.display = "none";
  iframe.style.zIndex = "9999";

  document.body.appendChild(iframe);

  // Toggle on click
  button.onclick = () => {
    iframe.style.display =
      iframe.style.display === "none" ? "block" : "none";
  };
})();
