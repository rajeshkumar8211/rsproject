const root = document.getElementById("results");
let data = null;

try {
  data = JSON.parse(sessionStorage.getItem("cpResults"));
} catch (e) {
  data = null;
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[c]));
}

if (!data || !Array.isArray(data.recommendations) || data.recommendations.length === 0) {
  root.innerHTML = `
    <div class="col-12">
      <div class="cp-card text-center">
        <p class="mb-3">No results yet. Take the assessment to see your matches.</p>
        <a class="btn btn-cp" href="/assess">Start assessment</a>
      </div>
    </div>`;
} else {
  root.innerHTML = data.recommendations.map((r, i) => `
    <div class="col-lg-${i === 0 ? "12" : "6"}">
      <article class="cp-card result ${i === 0 ? "top" : ""} h-100">
        ${i === 0 ? '<span class="badge-top">Top recommendation</span>' : `<span class="rank">#${esc(r.rank)}</span>`}
        <h2 class="h3 mt-2">${esc(r.career)}</h2>
        <div class="d-flex justify-content-between align-items-end mb-1">
          <span class="text-muted small">Match</span>
          <strong class="pct">${esc(r.match_percentage)}%</strong>
        </div>
        <div class="progress" role="progressbar" aria-label="Match for ${esc(r.career)}"
             aria-valuenow="${esc(r.match_percentage)}" aria-valuemin="0" aria-valuemax="100">
          <div class="progress-bar" data-w="${esc(r.match_percentage)}" style="width:0"></div>
        </div>
        <p class="mt-3">${esc(r.description)}</p>
        <p class="mb-2 fw-bold small">Important skills</p>
        <div class="mb-3">${(r.key_skills || []).map((s) => `<span class="chip">${esc(s)}</span>`).join("")}</div>
        <details>
          <summary>Learn more</summary>
          <p class="mt-2 mb-0">${esc(r.learn_more)}</p>
        </details>
      </article>
    </div>`).join("");

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.querySelectorAll(".progress-bar").forEach((b) => {
        b.style.width = b.dataset.w + "%";
      });
    });
  });
}
