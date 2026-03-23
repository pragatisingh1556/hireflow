// dashboard script - loads jobs and shows them in table
// jobs come from the json file that the scraper creates

var allJobs = [];

// sample data for demo - in real use, scraper fills this
var sampleJobs = [
  {
    title: "Python Developer",
    company: "TCS",
    location: "Bangalore",
    source: "LinkedIn",
    link: "https://linkedin.com",
    status: "new",
    scraped_date: "2026-03-23"
  },
  {
    title: "Junior Software Engineer",
    company: "Infosys",
    location: "Hyderabad",
    source: "Naukri",
    link: "https://naukri.com",
    status: "applied",
    scraped_date: "2026-03-23"
  },
  {
    title: "Full Stack Developer Intern",
    company: "Wipro",
    location: "Pune",
    source: "Internshala",
    link: "https://internshala.com",
    status: "new",
    scraped_date: "2026-03-23"
  },
  {
    title: "Backend Developer",
    company: "Zoho",
    location: "Chennai",
    source: "Indeed",
    link: "https://indeed.co.in",
    status: "interview",
    scraped_date: "2026-03-22"
  },
  {
    title: "React Native Developer",
    company: "Flipkart",
    location: "Bangalore",
    source: "LinkedIn",
    link: "https://linkedin.com",
    status: "new",
    scraped_date: "2026-03-22"
  },
  {
    title: "Data Analyst Fresher",
    company: "Accenture",
    location: "Mumbai",
    source: "Naukri",
    link: "https://naukri.com",
    status: "rejected",
    scraped_date: "2026-03-21"
  },
  {
    title: "Software Developer Trainee",
    company: "HCL Technologies",
    location: "Noida",
    source: "Indeed",
    link: "https://indeed.co.in",
    status: "new",
    scraped_date: "2026-03-21"
  },
  {
    title: "Web Developer Intern",
    company: "Paytm",
    location: "Noida",
    source: "Internshala",
    link: "https://internshala.com",
    status: "applied",
    scraped_date: "2026-03-20"
  },
  {
    title: "Java Developer - Fresher",
    company: "Cognizant",
    location: "Chennai",
    source: "Naukri",
    link: "https://naukri.com",
    status: "new",
    scraped_date: "2026-03-20"
  },
  {
    title: "DevOps Engineer Intern",
    company: "Amazon",
    location: "Hyderabad",
    source: "LinkedIn",
    link: "https://linkedin.com",
    status: "applied",
    scraped_date: "2026-03-19"
  }
];


// load jobs when page opens
window.onload = function() {
  loadJobs();
};

// refresh button
document.getElementById("refreshBtn").onclick = function() {
  loadJobs();
};

// export button
document.getElementById("exportBtn").onclick = function() {
  exportToCSV();
};

// search filter
document.getElementById("searchInput").oninput = function() {
  filterAndDisplay();
};

// source filter
document.getElementById("sourceFilter").onchange = function() {
  filterAndDisplay();
};

// status filter
document.getElementById("statusFilter").onchange = function() {
  filterAndDisplay();
};


// load jobs from json file or use sample data
function loadJobs() {
  // try to load from jobs.json (created by scraper)
  fetch("jobs.json")
    .then(function(response) {
      if (response.ok) {
        return response.json();
      }
      // if no json file, use sample data
      throw new Error("no json file");
    })
    .then(function(data) {
      allJobs = data;
      filterAndDisplay();
    })
    .catch(function(err) {
      // use sample data for demo
      console.log("using sample data -", err.message);
      allJobs = sampleJobs;
      filterAndDisplay();
    });
}


// filter jobs based on search and dropdowns
function filterAndDisplay() {
  var searchText = document.getElementById("searchInput").value.toLowerCase();
  var sourceVal = document.getElementById("sourceFilter").value;
  var statusVal = document.getElementById("statusFilter").value;

  var filtered = [];

  for (var i = 0; i < allJobs.length; i++) {
    var job = allJobs[i];

    // search filter
    if (searchText !== "") {
      var title = (job.title || "").toLowerCase();
      var company = (job.company || "").toLowerCase();
      var location = (job.location || "").toLowerCase();

      if (title.indexOf(searchText) === -1 &&
          company.indexOf(searchText) === -1 &&
          location.indexOf(searchText) === -1) {
        continue;
      }
    }

    // source filter
    if (sourceVal !== "all" && job.source !== sourceVal) {
      continue;
    }

    // status filter
    if (statusVal !== "all" && job.status !== statusVal) {
      continue;
    }

    filtered.push(job);
  }

  displayJobs(filtered);
  updateStats();
}


// show jobs in the table
function displayJobs(jobs) {
  var tbody = document.getElementById("jobTableBody");
  var emptyState = document.getElementById("emptyState");
  var table = document.getElementById("jobTable");

  // clear old rows
  tbody.innerHTML = "";

  if (jobs.length === 0) {
    table.style.display = "none";
    emptyState.style.display = "block";
    return;
  }

  table.style.display = "table";
  emptyState.style.display = "none";

  for (var i = 0; i < jobs.length; i++) {
    var job = jobs[i];
    var row = document.createElement("tr");

    // title column
    var titleCell = document.createElement("td");
    titleCell.style.fontWeight = "600";
    titleCell.textContent = job.title || "N/A";
    row.appendChild(titleCell);

    // company column
    var companyCell = document.createElement("td");
    companyCell.textContent = job.company || "N/A";
    row.appendChild(companyCell);

    // location column
    var locationCell = document.createElement("td");
    locationCell.textContent = job.location || "N/A";
    row.appendChild(locationCell);

    // source badge
    var sourceCell = document.createElement("td");
    var sourceBadge = document.createElement("span");
    sourceBadge.className = "source-badge source-" + (job.source || "").toLowerCase();
    sourceBadge.textContent = job.source || "N/A";
    sourceCell.appendChild(sourceBadge);
    row.appendChild(sourceCell);

    // status badge (clickable to change)
    var statusCell = document.createElement("td");
    var statusBadge = document.createElement("span");
    statusBadge.className = "status-badge status-" + (job.status || "new");
    statusBadge.textContent = job.status || "new";
    statusBadge.setAttribute("data-index", i);
    statusBadge.onclick = function() {
      var idx = this.getAttribute("data-index");
      cycleStatus(idx);
    };
    statusCell.appendChild(statusBadge);
    row.appendChild(statusCell);

    // action buttons
    var actionCell = document.createElement("td");

    // apply button - opens job link
    if (job.link) {
      var applyBtn = document.createElement("button");
      applyBtn.className = "action-btn apply-btn";
      applyBtn.textContent = "Apply";
      applyBtn.setAttribute("data-link", job.link);
      applyBtn.onclick = function() {
        var link = this.getAttribute("data-link");
        window.open(link, "_blank");
      };
      actionCell.appendChild(applyBtn);
    }

    row.appendChild(actionCell);
    tbody.appendChild(row);
  }
}


// cycle through status: new -> applied -> interview -> rejected -> new
function cycleStatus(index) {
  var statusOrder = ["new", "applied", "interview", "rejected"];

  var currentStatus = allJobs[index].status || "new";
  var currentIdx = statusOrder.indexOf(currentStatus);
  var nextIdx = (currentIdx + 1) % statusOrder.length;

  allJobs[index].status = statusOrder[nextIdx];

  // save to localstorage so status persists
  localStorage.setItem("hireflow_jobs", JSON.stringify(allJobs));

  filterAndDisplay();
}


// update the stats cards
function updateStats() {
  var total = allJobs.length;
  var newCount = 0;
  var appliedCount = 0;
  var interviewCount = 0;
  var rejectedCount = 0;

  for (var i = 0; i < allJobs.length; i++) {
    var status = allJobs[i].status || "new";
    if (status === "new") newCount++;
    if (status === "applied") appliedCount++;
    if (status === "interview") interviewCount++;
    if (status === "rejected") rejectedCount++;
  }

  document.getElementById("totalJobs").textContent = total;
  document.getElementById("newJobs").textContent = newCount;
  document.getElementById("appliedJobs").textContent = appliedCount;
  document.getElementById("interviewJobs").textContent = interviewCount;
  document.getElementById("rejectedJobs").textContent = rejectedCount;
}


// export to csv
function exportToCSV() {
  if (allJobs.length === 0) {
    alert("no jobs to export");
    return;
  }

  var csvContent = "Title,Company,Location,Source,Status,Link\n";

  for (var i = 0; i < allJobs.length; i++) {
    var job = allJobs[i];
    var row = '"' + (job.title || "") + '","' +
              (job.company || "") + '","' +
              (job.location || "") + '","' +
              (job.source || "") + '","' +
              (job.status || "") + '","' +
              (job.link || "") + '"';
    csvContent = csvContent + row + "\n";
  }

  // download the csv
  var blob = new Blob([csvContent], { type: "text/csv" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url;
  a.download = "hireflow_jobs.csv";
  a.click();
  URL.revokeObjectURL(url);
}
