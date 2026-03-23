// popup.js - handles the extension popup
// saves user profile to chrome storage
// sends fill command to content script

// all the input field ids
var fieldIds = [
  "fullName", "email", "phone", "city",
  "college", "degree", "gradYear", "skills",
  "linkedin", "github"
];

// load saved profile when popup opens
window.onload = function() {
  loadProfile();
  loadStats();
};

// save button click
document.getElementById("saveBtn").onclick = function() {
  saveProfile();
};

// fill button click
document.getElementById("fillBtn").onclick = function() {
  fillCurrentPage();
};


// save profile to chrome storage
function saveProfile() {
  var profile = {};

  for (var i = 0; i < fieldIds.length; i++) {
    var id = fieldIds[i];
    var value = document.getElementById(id).value.trim();
    profile[id] = value;
  }

  // check if at least name and email are filled
  if (profile.fullName === "" || profile.email === "") {
    showStatus("please fill name and email at least", "red");
    return;
  }

  // save to chrome storage
  chrome.storage.local.set({ "hireflow_profile": profile }, function() {
    showStatus("profile saved!", "green");
  });
}


// load profile from chrome storage
function loadProfile() {
  chrome.storage.local.get("hireflow_profile", function(data) {
    var profile = data.hireflow_profile;
    if (!profile) return;

    // fill all fields with saved values
    for (var i = 0; i < fieldIds.length; i++) {
      var id = fieldIds[i];
      if (profile[id]) {
        document.getElementById(id).value = profile[id];
      }
    }
  });
}


// send fill command to the current tab
function fillCurrentPage() {
  chrome.storage.local.get("hireflow_profile", function(data) {
    var profile = data.hireflow_profile;
    if (!profile) {
      showStatus("save your profile first!", "red");
      return;
    }

    // send message to content script
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      if (tabs.length === 0) return;

      chrome.tabs.sendMessage(tabs[0].id, {
        action: "fill_form",
        profile: profile
      }, function(response) {
        if (chrome.runtime.lastError) {
          showStatus("cant fill on this page. open a job portal first", "red");
          return;
        }

        if (response && response.filled) {
          showStatus("filled " + response.filled + " fields!", "green");
          updateFillCount();
        } else {
          showStatus("no fillable fields found on this page", "orange");
        }
      });
    });
  });
}


// show status message
function showStatus(msg, color) {
  var statusEl = document.getElementById("statusMsg");
  statusEl.textContent = msg;
  statusEl.style.color = color;

  // clear after 3 seconds
  setTimeout(function() {
    statusEl.textContent = "";
  }, 3000);
}


// load stats from storage
function loadStats() {
  chrome.storage.local.get(["hireflow_fills", "hireflow_saves"], function(data) {
    var fills = data.hireflow_fills || 0;
    var saves = data.hireflow_saves || 0;

    document.getElementById("fillCount").textContent = fills;
    document.getElementById("saveCount").textContent = saves;
  });
}


// increment fill count
function updateFillCount() {
  chrome.storage.local.get("hireflow_fills", function(data) {
    var count = (data.hireflow_fills || 0) + 1;
    chrome.storage.local.set({ "hireflow_fills": count });
    document.getElementById("fillCount").textContent = count;
  });
}
