const bodyRoot = () => document.body.dataset.root || "./";

async function findRoot() {
  if (!document.querySelector("[data-404]")) return bodyRoot();
  for (const prefix of ["./","../","../../"]) {
    try {
      const response = await fetch(prefix + "dates.json");
      if (response.ok) {
        const css = document.querySelector('link[rel="stylesheet"]');
        if (css) css.href = prefix + "assets/style.css";
        const home = document.getElementById("home-link");
        const dates = document.getElementById("dates-link");
        if (home) home.href = prefix;
        if (dates) dates.href = prefix + "dates/";
        document.body.dataset.root = prefix;
        return prefix;
      }
    } catch (err) {
      // try the next candidate
    }
  }
  return bodyRoot();
}

async function loadDates() {
  const response = await fetch((document.body.dataset.root || "./") + "dates.json");
  if (!response.ok) throw new Error("dates.json missing");
  return response.json();
}

async function initDatePicker() {
  await findRoot();
  const input = document.querySelector("[data-date-picker]");
  if (!input) return;

  let dates = [];
  try {
    dates = await loadDates();
  } catch (err) {
    console.warn(err);
    return;
  }
  if (!dates.length) return;

  input.max = dates[0];
  input.min = dates[dates.length - 1];

  input.addEventListener("input", () => input.setCustomValidity(""));
  input.addEventListener("change", () => {
    const day = input.value;
    if (!day) return;
    if (dates.includes(day)) {
      window.location.href = bodyRoot() + day + "/";
      return;
    }
    input.setCustomValidity("No digest for this date.");
    input.reportValidity();
  });
}

initDatePicker();
