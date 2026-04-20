const BASE_URL = "http://127.0.0.1:8000";

// 🔐 LOGIN


async function login() {
  console.log("Login clicked");

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("http://127.0.0.1:8000/accounts/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: email,
        password: password
      })
    });

    console.log("Response received:", res);

    const data = await res.json();
    console.log("Data:", data);

    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      window.location.href = "dashboard.html";
    } else {
      alert("Login failed: " + JSON.stringify(data));
    }

  } catch (err) {
    console.error("FULL ERROR:", err);  // 🔥 IMPORTANT
    alert("Check console (F12)");
  }
}

// 📝 REGISTER
async function register() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${BASE_URL}/accounts/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  });

  if (res.ok) {
    alert("Registered successfully");
    window.location.href = "login.html";
  } else {
    alert("Registration failed");
  }
}

// 🔐 CHECK AUTH
function checkAuth() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "login.html";
  }
}

// 🚪 LOGOUT
function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

// 💸 ADD EXPENSE
async function addExpense() {
  const amount = document.getElementById("amount").value;
  const category = document.getElementById("category").value;
  const date = document.getElementById("date").value;

  const token = localStorage.getItem("token");

  const res = await fetch(`${BASE_URL}/expenses/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ amount, category, date })
  });

  if (res.ok) {
    alert("Expense added");
    window.location.href = "dashboard.html";
  } else {
    alert("Error adding expense");
  }
}

// 📊 LOAD EXPENSES
async function loadExpenses() {
  checkAuth();

  const token = localStorage.getItem("token");

  const res = await fetch(`${BASE_URL}/expenses/`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();

  const list = document.getElementById("list");
  list.innerHTML = "";

  data.forEach(e => {
    const div = document.createElement("div");
    div.className = "expense";
    div.innerHTML = `
      <span>₹${e.amount}</span>
      <span>${e.category}</span>
      <span>${e.date}</span>
    `;
    list.appendChild(div);
  });
}