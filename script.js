// Add initial row on load dummy
window.onload = () => addRow();

function addRow() {
  const tbody = document.getElementById("items-body");
  const row = document.createElement("tr");

  row.innerHTML = `
    <td><input type="text" placeholder="Item Name" class="item-name"></td>
    <td><input type="number" placeholder="Quantity" class="item-qty" min="1"></td>
    <td><input type="number" placeholder="Price" class="item-price" min="0" step="0.01"></td>
    <td>
      <button type="button" onclick="removeRow(this)">-</button>
    </td>
  `;
  tbody.appendChild(row);
}

function removeRow(button) {
  const row = button.closest("tr");
  row.remove();
}

async function generateInvoice() {
  const companyName = document.getElementById("company_name").value;
  
  // Collect all items from your dynamic table
  const items = [];
  document.querySelectorAll(".item-row").forEach(row => {
    items.push({
      name: row.querySelector(".item-name").value,
      quantity: Number(row.querySelector(".item-quantity").value),
      price: Number(row.querySelector(".item-price").value)
    });
  });

  try {
    const response = await fetch("https://invoice-worker.mohit-itsector.workers.dev", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company_name: companyName, items })
    });

    if (response.ok) {
      alert("Invoice generation job triggered. Check 'orders/' folder once workflow finishes.");
    } else {
      const text = await response.text();
      alert("Failed to trigger invoice generation: " + text);
    }

  } catch (err) {
    console.error(err);
    alert("Error triggering invoice generation.");
  }
}
