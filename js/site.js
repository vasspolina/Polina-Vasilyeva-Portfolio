/* masonry spans + filters + theme toggle */
(function () {
  // ---- theme ----
  var toggle = document.querySelector(".theme-toggle");
  function currentDark() {
    var t = document.documentElement.dataset.theme;
    if (t) return t === "dark";
    return matchMedia("(prefers-color-scheme: dark)").matches;
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
      localStorage.setItem("theme", next);
      reflect();
    });
    reflect();
  }

  // ---- masonry (index grid) ----
  var grid = document.querySelector(".grid");
  if (grid) {
    var ROW = 8; // matches grid-auto-rows
    function layout() {
      var items = [].filter.call(
        grid.querySelectorAll(".grid-item"),
        function (i) { return !i.classList.contains("is-hidden"); }
      );
      // A single column packs nothing, so leave the rows alone: on a phone
      // the browser fires resize on every scroll as its bar shows and hides,
      // and laying out every tile each time made the page stick.
      if (getComputedStyle(grid).gridAutoRows === "auto") {
        items.forEach(function (i) { i.style.gridRowEnd = ""; });
        return;
      }
      // collapse all tracks first so scrollHeight reports content height
      items.forEach(function (i) { i.style.gridRowEnd = "span 1"; });
      var heights = items.map(function (i) { return i.scrollHeight; });
      items.forEach(function (i, k) {
        i.style.gridRowEnd = "span " + Math.ceil(heights[k] / ROW);
      });
    }
    var pending;
    function schedule() {
      cancelAnimationFrame(pending);
      pending = requestAnimationFrame(layout);
    }
    // Only a change of width can change the packing; a height-only resize
    // is the mobile address bar and happens on every scroll.
    var lastWidth = innerWidth;
    addEventListener("resize", function () {
      if (innerWidth === lastWidth) return;
      lastWidth = innerWidth;
      schedule();
    });
    addEventListener("load", layout);
    grid.querySelectorAll("img").forEach(function (img) {
      if (img.complete) return;
      img.addEventListener("load", schedule);
    });
    layout();

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
      layout();
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
      if (kind === "grid") layout();
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
  }
  slider.addEventListener("input", apply);
  apply();
})();
