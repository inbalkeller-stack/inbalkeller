/* =========================================================
   INBAL KELLER — PORTFOLIO
   Loader · mobile hamburger · desktop "projects" dropdown
   ========================================================= */

(function () {
  /* ---------- Loader ----------
     Plays the loader video once, start to end, then reveals the site.
     Only on the first visit in a browser session. */
  var loader = document.getElementById('loader');
  var loaderVideo = document.getElementById('loaderVideo');
  var SAFETY = 20000;    // never block the page longer than this
  var done = false;

  function hideLoader() {
    if (done || !loader) return;
    done = true;
    loader.classList.add('is-hidden');
    document.body.classList.remove('is-loading');
  }

  var seen = document.documentElement.classList.contains('loader-seen');
  if (seen || !loader) {
    done = true;
    document.body.classList.remove('is-loading');
    if (loaderVideo) loaderVideo.removeAttribute('src');
  } else {
    try { sessionStorage.setItem('loaderSeen', '1'); } catch (e) {}
    if (loaderVideo) {
      loaderVideo.addEventListener('ended', hideLoader);
      loaderVideo.addEventListener('error', function () { setTimeout(hideLoader, 1500); });
      var p = loaderVideo.play();
      if (p && p.catch) p.catch(function () { setTimeout(hideLoader, 2500); });
    } else {
      window.addEventListener('load', hideLoader);
    }
    setTimeout(hideLoader, SAFETY);
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

    // Hovering a project tile also highlights its name in the list
    document.querySelectorAll('.tile').forEach(function (tile) {
      var item = projectList.querySelector('a[href="' + tile.getAttribute('href') + '"]');
      if (!item) return;
      tile.addEventListener('mouseenter', function () { item.classList.add('is-hover'); });
      tile.addEventListener('mouseleave', function () { item.classList.remove('is-hover'); });
    });

    projectsToggle.addEventListener('click', function () {
      pinned = !pinned;
      setOpen(pinned);
    });
  }
})();
