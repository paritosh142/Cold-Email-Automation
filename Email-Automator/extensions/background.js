// Example background script

// This script is optional but can be used for additional background processing

// Listen for messages from the popup or other parts of the extension
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Received message:", message);

  // Handle different types of messages here
  if (message.type === "emailGenerated") {
    // Example: Log the generated email details
    console.log("Generated Email:", message.emailDetails);
  }

  // Send a response back to the sender if needed
  sendResponse({ status: "received" });
});

// Example: Handle a browser action click event (like clicking the extension icon)
chrome.action.onClicked.addListener((tab) => {
  // Perform an action when the extension icon is clicked
  console.log("Extension icon clicked.");
});
