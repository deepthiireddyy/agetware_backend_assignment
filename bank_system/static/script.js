document.addEventListener("DOMContentLoaded", () => {
  const formatCurrency = (amount) => `₹${Number(amount).toLocaleString("en-IN")}`;
  const formatDate = (isoDate) => new Date(isoDate).toLocaleDateString("en-IN");

  const handleForm = (formId, endpoint, responseBoxId, method = "POST") => {
    document.getElementById(formId).addEventListener("submit", async (e) => {
      e.preventDefault();

      const form = e.target;
      const data = Object.fromEntries(new FormData(form));
      const responseBox = document.getElementById(responseBoxId);

      responseBox.innerText = "⏳ Sending request...";
      responseBox.className = "response-box";

      try {
        let res;
        if (method === "GET") {
          const query = new URLSearchParams(data).toString();
          res = await fetch(`${endpoint}?${query}`, { method: "GET" });
        } else {
          res = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          });
        }

        const response = await res.json();

        if (res.ok) {
          responseBox.classList.add("success");

          let formatted = "";

          if (formId === "lend-form") {
            formatted = `
${response.message}
Loan ID: ${response.loan_id}
Bank: ${response.bank_name}
Customer: ${response.customer_name}
Created At: ${formatDate(response.created_at)}

Principal: ${formatCurrency(response.principal)}
Interest: ${formatCurrency(response.total_interest)}
Total: ${formatCurrency(response.total_amount)}
EMI: ${formatCurrency(response.emi_amount)} for ${response.num_emis} months
EMIs Remaining: ${response.emis_remaining}
`;
          }

          else if (formId === "payment-form") {
            formatted = `
${response.message}
Payment ID: ${response.payment_id}
Loan ID: ${response.loan_id}
Bank: ${response.bank_name}
Customer: ${response.customer_name}
Paid At: ${formatDate(response.created_at)}

EMI Paid: ${response.emi_number_paid}
Lump Sum Paid Now: ${formatCurrency(response.lump_sum_paid_now)}
EMI/month: ${formatCurrency(response.emi_amount)}

Total Paid Till Now: ${formatCurrency(response.total_paid_till_now)}
Remaining Amount: ${formatCurrency(response.amount_remaining)}
EMIs Remaining: ${response.emis_remaining}
Loan Closed: ${response.loan_closed ? "Yes" : "No"}
`;
          }

          else if (formId === "ledger-form") {
            formatted = `
Bank: ${response.bank_name}
Customer: ${response.customer_name}
Loan ID: ${response.loan_id}

Principal: ${formatCurrency(response.principal)}
Total Interest: ${formatCurrency(response.total_interest)}
Total Amount: ${formatCurrency(response.total_amount)}
EMI: ${formatCurrency(response.emi_amount)} for ${response.num_emis} months

Transactions:
${response.transactions.map(t => `• EMI #${t.emi_number} | ₹${t.lump_sum_amount} | ${formatDate(t.paid_at)}`).join('\n')}

Loan Closed: ${response.loan_closed ? "Yes" : "No"}
`;
          }

          else if (formId === "overview-form") {
            formatted = response.loans.map(loan => `
Bank: ${loan.bank_name}
Loan ID: ${loan.loan_id}
Customer: ${loan.customer_name}

Principal: ${formatCurrency(loan.principal)}
Interest: ${formatCurrency(loan.total_interest)}
Total: ${formatCurrency(loan.total_amount)}
EMI: ${formatCurrency(loan.emi_amount)} for ${loan.num_emis} months

EMIs Paid: ${loan.emis_paid}
EMIs Left: ${loan.emis_remaining}
Amount Paid: ${formatCurrency(loan.amount_paid_till_date)}
Loan Closed: ${loan.loan_closed ? "Yes" : "No"}
`).join("\n------------------\n");
          }

          responseBox.innerText = formatted;
        } else {
          responseBox.classList.add("error");
          responseBox.innerText = JSON.stringify(response, null, 2);
        }

        form.reset();
      } catch (err) {
        responseBox.classList.add("error");
        responseBox.innerText = "Error: Could not connect to server.";
      }
    });
  };

  handleForm("lend-form", "/lend", "lend-response");
  handleForm("payment-form", "/payment", "payment-response");
  handleForm("ledger-form", "/ledger", "ledger-response", "GET");
  handleForm("overview-form", "/account/overview", "overview-response", "GET");
});
