/* =========================================================
   INBAL KELLER — PORTFOLIO
   Loader · mobile hamburger · desktop "projects" dropdown
   ========================================================= */

(function () {
  /* ---------- Loader ---------- */
  var loader = document.getElementById('loader');
  var MIN_TIME = 1200;   // ms the loader stays visible at minimum
  var MAX_TIME = 6000;   // safety: never block the page longer than this
  var start = Date.now();
  var done = false;

  function hideLoader() {
    if (done || !loader) return;
    done = true;
    var wait = Math.max(0, MIN_TIME - (Date.now() - start));
    setTimeout(function () {
      loader.classList.add('is-hidden');
      document.body.classList.remove('is-loading');
    }, wait);
  }

  var seen = document.documentElement.classList.contains('loader-seen');
  if (seen || !loader) {
    // Loader only plays when the portfolio is first opened
    done = true;
    document.body.classList.remove('is-loading');
  } else {
    try { sessionStorage.setItem('loaderSeen', '1'); } catch (e) {}
    window.addEventListener('load', hideLoader);
    setTimeout(hideLoader, MAX_TIME);
  }

  /* ---------- Mobile hamburger ---------- */
  var menuToggle = document.getElementById('menuToggle');
  var mobileMenu = document.getElementById('mobileMenu');

  function setMenu(open) {
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    mobileMenu.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
  }

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', function () {
      setMenu(menuToggle.getAttribute('aria-expanded') !== 'true');
    });
    mobileMenu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMenu(false);
    });
    window.matchMedia('(min-width: 900px)').addEventListener('change', function (mq) {
      if (mq.matches) setMenu(false);
    });
  }

  /* ---------- Desktop "projects" list ----------
     Hovering the "projects" tab, the list itself or any project tile
     shows the project names in place of the welcome text.
     Clicking "projects" pins it open (for touch screens). */
  var projectsToggle = document.getElementById('projectsToggle');
  var projectList = document.getElementById('projectList');
  var welcome = document.getElementById('welcome');
  var tiles = document.querySelector('.tiles');

  if (projectsToggle && projectList && welcome) {
    var pinned = false;
    var closeTimer = null;

    function setOpen(open) {
      projectsToggle.setAttribute('aria-expanded', String(open));
      projectList.hidden = !open;
      welcome.hidden = open;
      document.body.classList.toggle('projects-open', open);
    }
    function open() {
      clearTimeout(closeTimer);
      setOpen(true);
    }
    function closeSoon() {
      if (pinned) return;
      clearTimeout(closeTimer);
      closeTimer = setTimeout(function () { setOpen(false); }, 200);
    }

    [projectsToggle, projectList, tiles].forEach(function (el) {
      if (!el) return;
      el.addEventListener('mouseenter', open);
      el.addEventListener('mouseleave', closeSoon);
      el.addEventListener('focusin', open);
      el.addEventListener('focusout', closeSoon);
    });

    projectsToggle.addEventListener('click', function () {
      pinned = !pinned;
      setOpen(pinned);
    });
  }
})();
