Promise.all([
  fetch("summary.json").then(res => res.json()),
  fetch("languages.json").then(res => res.json())
]).then(([data, languages]) => {
  const container = document.getElementById("dashboard");
  container.innerHTML = "";

  for (const [file, info] of Object.entries(data.files)) {
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    thead.innerHTML = `<tr><th colspan="4"><a href="${info.url}">${file}</a></th></tr><tr><th>Language</th><th>Completed</th><th>Missing Keys</th><th>%</th></tr>`;
    table.appendChild(thead);

    const tbody = document.createElement("tbody");

    for (const [lang, stat] of Object.entries(info.translations)) {
      const row = document.createElement("tr");
      let className = "complete";
      if (stat.percent < 100 && stat.percent > 0) className = "partial";
      if (stat.percent === 0) className = "missing";
      row.className = className;

      const languageName = languages[lang]?.display_name || lang;

      row.innerHTML = `
        <td><a href="${stat.url}">${languageName}</a></td>
        <td>${stat.completed}</td>
        <td>${stat.missing.join(", ")}</td>
        <td>${stat.percent}%</td>
      `;
      tbody.appendChild(row);
    }

    table.appendChild(tbody);
    container.appendChild(table);
  }
});
