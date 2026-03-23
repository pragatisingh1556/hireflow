// content.js - runs on job portal pages
// listens for fill command from popup
// finds form fields and fills them with user profile data

// mapping of common field names to profile keys
// i found these by inspecting forms on linkedin, naukri, indeed, internshala
var fieldMappings = {
  // name fields
  "name": "fullName",
  "full_name": "fullName",
  "fullname": "fullName",
  "first_name": "fullName",
  "firstname": "fullName",
  "applicant_name": "fullName",
  "candidate_name": "fullName",

  // email fields
  "email": "email",
  "email_address": "email",
  "emailaddress": "email",
  "user_email": "email",

  // phone fields
  "phone": "phone",
  "mobile": "phone",
  "phone_number": "phone",
  "contact": "phone",
  "mobile_number": "phone",
  "contact_number": "phone",

  // city fields
  "city": "city",
  "location": "city",
  "current_city": "city",
  "current_location": "city",

  // college fields
  "college": "college",
  "university": "college",
  "institution": "college",
  "school": "college",

  // degree fields
  "degree": "degree",
  "qualification": "degree",
  "education": "degree",

  // year fields
  "graduation_year": "gradYear",
  "grad_year": "gradYear",
  "passing_year": "gradYear",
  "year": "gradYear",
  "batch": "gradYear",

  // skills fields
  "skills": "skills",
  "key_skills": "skills",
  "technical_skills": "skills",

  // linkedin fields
  "linkedin": "linkedin",
  "linkedin_url": "linkedin",
  "linkedin_profile": "linkedin",

  // github fields
  "github": "github",
  "github_url": "github",
  "github_profile": "github",
  "portfolio": "github"
};


// listen for messages from popup
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "fill_form") {
    var result = fillFormFields(message.profile);
    sendResponse(result);
  }
  return true; // keeps the message channel open
});


// main function - finds and fills form fields
function fillFormFields(profile) {
  var filledCount = 0;

  // get all input fields on the page
  var inputs = document.querySelectorAll("input, textarea, select");

  for (var i = 0; i < inputs.length; i++) {
    var input = inputs[i];

    // skip hidden and submit fields
    if (input.type === "hidden" || input.type === "submit" || input.type === "button") {
      continue;
    }

    // skip fields that already have values
    if (input.value && input.value.trim() !== "") {
      continue;
    }

    // try to match this field to our profile data
    var profileKey = findMatchingKey(input);

    if (profileKey && profile[profileKey]) {
      // fill the field
      input.value = profile[profileKey];

      // trigger events so the page knows the value changed
      // without this some sites dont register the input
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
      input.dispatchEvent(new Event("blur", { bubbles: true }));

      // highlight filled fields so user can see what we changed
      input.style.backgroundColor = "#E8F5E9";
      input.style.borderColor = "#4CAF50";

      filledCount = filledCount + 1;
    }
  }

  return { filled: filledCount };
}


// try to figure out which profile field matches this input
function findMatchingKey(input) {
  // check multiple attributes for clues
  var checkStrings = [
    (input.name || "").toLowerCase(),
    (input.id || "").toLowerCase(),
    (input.placeholder || "").toLowerCase(),
    (input.getAttribute("aria-label") || "").toLowerCase(),
    (input.getAttribute("data-testid") || "").toLowerCase()
  ];

  // also check the label if there is one
  var label = findLabel(input);
  if (label) {
    checkStrings.push(label.toLowerCase());
  }

  // go through all our mappings and see if any match
  for (var fieldName in fieldMappings) {
    for (var j = 0; j < checkStrings.length; j++) {
      var str = checkStrings[j];
      if (str.indexOf(fieldName) !== -1) {
        return fieldMappings[fieldName];
      }
    }
  }

  // special check for email type inputs
  if (input.type === "email") return "email";
  if (input.type === "tel") return "phone";
  if (input.type === "url") {
    // check if its linkedin or github
    for (var k = 0; k < checkStrings.length; k++) {
      if (checkStrings[k].indexOf("linkedin") !== -1) return "linkedin";
      if (checkStrings[k].indexOf("github") !== -1) return "github";
    }
  }

  return null;
}


// find the label element for an input
function findLabel(input) {
  // method 1: label with for attribute
  if (input.id) {
    var label = document.querySelector("label[for='" + input.id + "']");
    if (label) return label.textContent;
  }

  // method 2: parent label
  var parent = input.parentElement;
  if (parent && parent.tagName === "LABEL") {
    return parent.textContent;
  }

  // method 3: previous sibling label
  var prev = input.previousElementSibling;
  if (prev && prev.tagName === "LABEL") {
    return prev.textContent;
  }

  return null;
}
