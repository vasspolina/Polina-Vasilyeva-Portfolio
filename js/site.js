/* masonry spans + filters + theme toggle */
(function () {
  // ---- theme ----
  var toggle = document.querySelector(".theme-toggle");
  function currentDark() {
    var t = document.documentElement.dataset.theme;
    if (t) return t === "dark";
    return true; // the site lands dark until the visitor flips it
  }
  function reflect() {
    if (toggle) {
      toggle.setAttribute("aria-checked", String(currentDark()));
      toggle.setAttribute("aria-label", currentDark() ? "Light mode" : "Dark mode");
      var label = toggle.querySelector(".switch-label");
      if (label) label.textContent = currentDark() ? "Light mode" : "Dark mode";
    }
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = currentDark() ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) {}
      reflect();
    });
    reflect();
  }

  // ---- index grid ----
  // The grid sets in true rows now (css grid-auto-rows: auto), so nothing
  // here packs it; the filters and the view switch below still need the
  // grid element.
  var grid = document.querySelector(".grid");
  if (grid) {
    // ---- filters ----
    // Clicking changes what is on the page in place, without scrolling. The
    // project overview narrows to the projects that work in that discipline
    // and the tiles below narrow with it, so the two halves always agree.
    var buttons = document.querySelectorAll(".filter");
    var heading = document.getElementById("all");
    var empty = document.querySelector(".empty");

    function matches(el, key) {
      if (key === "all") return true;
      return (el.dataset.tags || "").split(",").indexOf(key) !== -1;
    }

    function apply(key, label) {
      var shown = 0;
      grid.querySelectorAll(".grid-item").forEach(function (item) {
        var hide = !matches(item, key);
        item.classList.toggle("is-hidden", hide);
        if (!hide) shown++;
      });
      // A group with nothing left in it takes its heading and rule away with
      // it, rather than leaving a brown line over an empty stretch of page.
      document.querySelectorAll(".idx-row").forEach(function (row) {
        row.classList.toggle("is-hidden", !matches(row, key));
      });
      document.querySelectorAll(".ov-group").forEach(function (group) {
        var live = 0;
        group.querySelectorAll(".ov-card").forEach(function (card) {
          var hide = !matches(card, key);
          card.classList.toggle("is-hidden", hide);
          if (!hide) live++;
        });
        group.classList.toggle("is-hidden", live === 0);
      });
      if (heading) {
        heading.textContent = key === "all" ? "Everything" : label;
      }
      if (empty) empty.hidden = shown > 0;
    }

    // ---- covers or index ----
    // Both views hold the same projects and the same tags, so the filter runs
    // over whichever is showing and the choice of view is independent of it.
    var views = document.querySelectorAll(".view");
    var overview = document.querySelector(".overview");
    var indexView = document.querySelector(".index-view");
    var allHeading = document.getElementById("all");

    function showView(kind) {
      views.forEach(function (v) {
        var on = v.dataset.view === kind;
        v.classList.toggle("is-on", on);
        v.setAttribute("aria-pressed", String(on));
      });
      if (overview) overview.hidden = kind !== "grid";
      if (indexView) indexView.hidden = kind !== "index";
      if (allHeading) allHeading.hidden = kind === "index";
      if (grid) grid.hidden = kind === "index";
    }
    views.forEach(function (v) {
      v.addEventListener("click", function () { showView(v.dataset.view); });
    });

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        buttons.forEach(function (b) {
          var on = b === btn;
          b.classList.toggle("is-active", on);
          b.setAttribute("aria-pressed", String(on));
        });
        apply(btn.dataset.filter, btn.textContent.trim());
      });
    });
  }
})();

/* Type specimen: the size slider drives the editable stage. */
(function () {
  var slider = document.getElementById("spec-size");
  var stage = document.getElementById("spec-stage");
  var out = document.getElementById("spec-size-out");
  if (!slider || !stage) return;
  function apply() {
    stage.style.fontSize = slider.value + "px";
    if (out) out.textContent = slider.value + "px";
    // the travelled part of the track, for the hand-drawn range
    var pct = (slider.value - slider.min) / (slider.max - slider.min) * 100;
    slider.style.setProperty("--fill", pct + "%");
  }
  slider.addEventListener("input", apply);
  apply();
})();
