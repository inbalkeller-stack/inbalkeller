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
      loaderVideo.playbackRate = 2;          // play the loader at double speed
      loaderVideo.addEventListener('loadedmetadata', function () { loaderVideo.playbackRate = 2; });
      loaderVideo.addEventListener('ended', hideLoader);
      loaderVideo.addEventListener('error', function () { setTimeout(hideLoader, 1500); });
      var p = loaderVideo.play();
      if (p && p.catch) p.catch(function () { setTimeout(hideLoader, 2500); });
    } else {
      window.addEventListener('load', hideLoader);
    }
    setTimeout(hideLoader, SAFETY);
  }

  /* end the magnetic intro once everything has landed */
  if (document.documentElement.classList.contains('intro')) setTimeout(function () { document.documentElement.classList.remove('intro'); }, 1700);

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
      // the list slides open under "projects" and pushes the welcome text down
      projectList.classList.toggle('is-open', open);
      projectList.setAttribute('aria-hidden', String(!open));
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

  /* ---------- Playground panels: tall panels stick when their bottom
     reaches the bottom of the screen, so the next one slides over ---------- */
  var panels = document.querySelectorAll('.pg-panel');
  function setStick() {
    var bar = document.querySelector('.mobile-bar');
    var off = bar && bar.offsetParent !== null ? bar.offsetHeight : 0;   /* mobile top bar */
    panels.forEach(function (p) {
      p.style.setProperty('--stick', Math.min(off, window.innerHeight - p.offsetHeight) + 'px');
    });
  }
  if (panels.length) { setStick(); window.addEventListener('resize', setStick); window.addEventListener('load', setStick); }


  /* ---------- Going to the Playground: "smart animate" ----------
     From a page with the pottery video (Home, Inbal Keller), the nav tabs grow
     downwards, pushing everything below them away, until the three tabs fill the
     nav area exactly as on the Playground page. The video never moves.
     Then the Playground opens with no second transition. */
  var wide = window.matchMedia('(min-width: 900px)');
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href$="playground.html"]');
    if (!a || !wide.matches || e.metaKey || e.ctrlKey || e.shiftKey || document.body.classList.contains('theme-playground')) return;
    var video = document.querySelector('.side__video, .sidebar .pg-side__video');
    var tabs = Array.prototype.slice.call(document.querySelectorAll('.side__nav > *, .sidebar .snav > *'));
    if (!video || tabs.length !== 3) return;          /* only pages whose nav sits under the video */
    e.preventDefault();
    var col = video.parentElement;
    var free = col.getBoundingClientRect().bottom - video.getBoundingClientRect().bottom;
    var target = free / 3;
    var blue = getComputedStyle(document.documentElement).getPropertyValue('--blue') || '#0004FF';
    var ease = 'cubic-bezier(0.65, 0, 0.35, 1)';
    tabs.forEach(function (t) {
      var h = t.getBoundingClientRect().height;
      t.style.setProperty('height', h + 'px', 'important'); t.style.setProperty('flex', 'none', 'important'); t.style.setProperty('min-height', '0', 'important');
    });
    if (projectList) projectList.classList.remove('is-open');
    col.getBoundingClientRect();                       /* lock the start sizes */
    tabs.forEach(function (t, i) {
      var isPlay = /playground\.html$/.test(t.getAttribute('href') || '');
      t.style.transition = 'height 0.42s ' + ease + ', background-color 0.42s ' + ease + ', color 0.42s ' + ease;
      t.style.setProperty('height', target + 'px', 'important');
      t.style.setProperty('background-color', isPlay ? blue : 'var(--bg)', 'important');
      t.style.setProperty('color', isPlay ? '#FCF8FF' : blue, 'important');
      t.style.borderColor = blue;
    });
    try { sessionStorage.setItem('vtSkip', '1'); } catch (x) {}
    setTimeout(function () { window.location.href = a.href; }, 430);
  });


  /* ---------- Leaving the Playground: the fan closes ----------
     The three tall tabs shrink back up to the normal tab height (like a fan
     folding), the video never moves, then the next page opens in place. */
  document.addEventListener('click', function (e) {
    if (!document.body.classList.contains('theme-playground') || !wide.matches) return;
    var a = e.target.closest && e.target.closest('.sidebar .snav a');
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var tabs = Array.prototype.slice.call(document.querySelectorAll('.sidebar .snav > *'));
    if (tabs.length !== 3) return;
    e.preventDefault();
    var navH = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-sub-h')) * 1.618;
    var probe = document.createElement('div'); probe.style.height = 'var(--nav-h)'; probe.style.position = 'absolute';
    document.body.appendChild(probe); navH = probe.getBoundingClientRect().height || navH; probe.remove();
    var blue = getComputedStyle(document.documentElement).getPropertyValue('--blue') || '#0004FF';
    var ease = 'cubic-bezier(0.65, 0, 0.35, 1)';
    var dest = a.getAttribute('href');
    tabs.forEach(function (t) {
      t.style.setProperty('height', t.getBoundingClientRect().height + 'px', 'important');
      t.style.setProperty('flex', 'none', 'important'); t.style.setProperty('min-height', '0', 'important');
    });
    document.querySelector('.sidebar').getBoundingClientRect();
    tabs.forEach(function (t) {
      var href = t.getAttribute('href') || '';
      /* the tab of the page we are going to becomes the coloured one (Projects stays blue on Home) */
      var active = (dest === 'about.html' && href === 'about.html') || (dest === 'index.html' && href === 'index.html');
      t.style.transition = 'height 0.42s ' + ease + ', background-color 0.42s ' + ease + ', color 0.42s ' + ease;
      t.style.setProperty('height', navH + 'px', 'important');
      t.style.setProperty('background-color', active ? blue : 'var(--bg)', 'important');
      t.style.setProperty('color', active ? '#FCF8FF' : blue, 'important');
    });
    try { sessionStorage.setItem('vtSkip', '1'); } catch (x) {}
    setTimeout(function () { window.location.href = a.href; }, 430);
  });


  /* ---------- Project pages: close / open the whole nav (remembered) ---------- */
  var navBtn = document.querySelector('.nav-close');
  var layout = document.querySelector('.layout');
  if (navBtn && layout) {
    /* the box sits exactly on the nav's edge (no gap, whatever the scrollbar) */
    var sideEl = layout.querySelector('.sidebar');
    var measure = function () {
      if (layout.classList.contains('nav-closed')) return;
      var r = sideEl.getBoundingClientRect();
      document.documentElement.style.setProperty('--nav-edge', r.right + 'px');
      document.documentElement.style.setProperty('--side-px', r.width + 'px');
    };
    measure(); window.addEventListener('resize', measure); window.addEventListener('load', measure);
    sideEl.addEventListener('transitionend', measure);
    var setNav = function (closed) {
      layout.classList.toggle('nav-closed', closed);
      navBtn.setAttribute('aria-expanded', String(!closed));
      navBtn.setAttribute('aria-label', closed ? 'Open the menu' : 'Close the menu');
    };
    var was = false; try { was = sessionStorage.getItem('navClosed') === '1'; } catch (x) {}
    if (was) { layout.classList.add('no-anim'); setNav(true); requestAnimationFrame(function () { requestAnimationFrame(function () { layout.classList.remove('no-anim'); }); }); }
    navBtn.addEventListener('click', function () {
      var closed = !layout.classList.contains('nav-closed');
      setNav(closed);
      try { sessionStorage.setItem('navClosed', closed ? '1' : '0'); } catch (x) {}
    });
  }

  /* ---------- Neighborhology changing data card ---------- */
  document.querySelectorAll('.ncard').forEach(function (card) {
    var imgs = card.querySelectorAll('.ncard__img'), n = imgs.length;
    function show(i) {
      i = Math.max(0, Math.min(n - 1, i));
      card.dataset.i = i;
      imgs.forEach(function (im, k) { im.classList.toggle('is-on', k === i); });
    }
    function cur() { return parseInt(card.dataset.i, 10) || 0; }
    card.querySelector('.ncard__next').addEventListener('click', function () { show(1); });
    card.querySelector('.ncard__prev').addEventListener('click', function () { show(cur() - 1); });
    card.querySelector('.ncard__fwd').addEventListener('click', function () { show(cur() + 1); });
  });

  /* ---------- Only one video plays sound at a time ---------- */
  var vids = Array.prototype.slice.call(document.querySelectorAll('video'));
  vids.forEach(function (v) {
    v.addEventListener('volumechange', function () {
      if (!v.muted && v.volume > 0) {
        vids.forEach(function (o) { if (o !== v && !o.muted) o.muted = true; });
      }
    });
  });
})();
