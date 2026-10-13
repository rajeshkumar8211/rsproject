const KEYS = ["programming", "communication", "creativity", "mathematics", "problem_solving"];
const form = document.getElementById("skillForm");
const errBox = document.getElementById("formError");

KEYS.forEach((k) => {
  const el = document.getElementById(k);
  const out = document.getElementById(k + "_out");
  el.addEventListener("input", () => {
    out.textContent = el.value;
  });
});

form.addEventListener("reset", () => {
  setTimeout(() => {
    KEYS.forEach((k) => {
      document.getElementById(k + "_out").textContent = "5";
      document.getElementById(k + "_err").textContent = "";
    });
  }, 0);
  errBox.classList.add("d-none");
});

function setLoading(on) {
  document.getElementById("submitBtn").disabled = on;
  document.getElementById("spin").classList.toggle("d-none", !on);
  document.getElementById("submitText").textContent = on ? "Finding matches…" : "Get My Recommendations";
}

function showError(msg) {
  errBox.textContent = msg;
  errBox.classList.remove("d-none");
}

function isValidSkill(raw) {
  if (!/^[0-9]+$/.test(raw)) return false;
  const n = Number(raw);
  return Number.isInteger(n) && n >= 1 && n <= 10;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errBox.classList.add("d-none");
  const payload = {};
  let bad = false;

  KEYS.forEach((k) => {
    const raw = document.getElementById(k).value;
    const err = document.getElementById(k + "_err");
    err.textContent = "";
    if (!isValidSkill(raw)) {
      err.textContent = "Choose a whole number from 1 to 10.";
      bad = true;
      return;
    }
    payload[k] = Number(raw);
  });

  if (bad) {
    showError("Please fix the highlighted skills and try again.");
    return;
  }

  setLoading(true);
  try {
    const res = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      if (data.details) {
        Object.entries(data.details).forEach(([k, m]) => {
          const el = document.getElementById(k + "_err");
          if (el) el.textContent = m;
        });
      }
      throw new Error(data.error || "Request failed.");
    }
    sessionStorage.setItem("cpResults", JSON.stringify(data));
    window.location.href = "/results";
  } catch (err) {
    showError(err instanceof TypeError ? "Can't reach the server. Check that Flask is running and try again." : err.message);
    setLoading(false);
  }
});
