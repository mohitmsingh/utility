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

export default async function handler(req, res) {
  const { company_name, items } = req.body;

  const response = await fetch(
    "https://api.github.com/repos/mohitmsingh/utility/dispatches",
    {
      method: "POST",
      headers: {
        "Authorization": `token ${process.env.GITHUB_PAT}`,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        event_type: "generate-invoice",
        client_payload: { company_name, items }
      })
    }
  );

  if (response.ok) res.status(200).json({ success: true });
  else res.status(500).json({ success: false, message: await response.text() });
}
