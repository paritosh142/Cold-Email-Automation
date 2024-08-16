// background.js
chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: () => {
      // Get input values from popup (we'll implement this later)
      const recipientEmail = document.getElementById("recipient_email").value;
      const jobDescription = document.getElementById("job_description").value;
      const hiringTeam = document.getElementById("hiring_team").value;
      const prompt = document.getElementById("prompt").value;

      // Create a prompt for Gemini API
      const geminiPrompt = `Write a professional email to ${recipientEmail} applying for a ${jobDescription} position on the ${hiringTeam} team. Use the following guidelines: ${prompt}`;

      // Call Gemini API (we'll implement this later)
      const generatedEmail = callGeminiAPI(geminiPrompt);

      // Parse Gemini response (we'll implement this later)
      const subject = extractSubject(generatedEmail);
      const body = extractBody(generatedEmail);

      // Open Gmail draft (we'll implement this later)
      openGmailDraft(subject, body);
    },
  });
});
