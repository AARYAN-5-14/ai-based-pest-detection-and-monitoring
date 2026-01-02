// Example: load alerts count
fetch("http://127.0.0.1:5000/api/alerts")
  .then(r => r.json())
  .then(data => {
    document.getElementById("alerts").innerText = data.length;
  });
