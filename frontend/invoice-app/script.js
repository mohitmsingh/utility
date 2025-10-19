async function generateInvoice() {
  const companyName = document.getElementById("company_name").value;
  const items = JSON.parse(document.getElementById("items").value);

  const response = await fetch("https://YOUR-BACKEND-URL/generate-invoice", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ company_name: companyName, items })
  });

  const data = await response.json();
  document.getElementById("output").innerText = JSON.stringify(data, null, 2);
}
