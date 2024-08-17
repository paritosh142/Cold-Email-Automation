// Save form data to local storage
function saveFormData() {
  const formData = new FormData(document.getElementById("emailForm"));
  const data = {};
  formData.forEach((value, key) => {
    data[key] = value;
  });
  chrome.storage.local.set({ formData: data });
}

// Restore form data from local storage
function restoreFormData() {
  chrome.storage.local.get("formData", (result) => {
    const data = result.formData || {};
    Object.keys(data).forEach((key) => {
      const input = document.querySelector(`[name="${key}"]`);
      if (input) {
        input.value = data[key];
      }
    });
  });
}

// Event listener for form submission
document
  .getElementById("emailForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    // Save form data before sending
    saveFormData();

    // Gather form data
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    // Send data to Flask backend
    fetch("http://localhost:5000/generate-email", {
      // Adjust the URL if your Flask server is deployed elsewhere
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams(data),
    })
      .then((response) => response.text())
      .then((text) => {
        // Open Gmail with the generated email details
        chrome.tabs.create({
          url: `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(
            data.email
          )}&su=${encodeURIComponent(
            text.split("\n")[0]
          )}&body=${encodeURIComponent(text.split("\n")[1])}`,
        });
      })
      .catch((error) => console.error("Error:", error));
  });

// Restore form data when the popup opens
restoreFormData();

// Save form data on any input change
document.querySelectorAll("input, textarea").forEach((element) => {
  element.addEventListener("input", saveFormData);
});
