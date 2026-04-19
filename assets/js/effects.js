/* ============================================
   Artisan Volt — Effects (premium interactions)
   Parallax, tilt, magnetic, ripple, spotlight, progress
   ============================================ */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.addEventListener('DOMContentLoaded', function () {

    /* ── Scroll progress bar ─────────────── */
    var progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    document.body.appendChild(progressBar);

    function updateProgress() {
      var h = document.documentElement;
      var scrolled = h.scrollTop;
      var height = h.scrollHeight - h.clientHeight;
      var pct = height > 0 ? (scrolled / height) * 100 : 0;
      progressBar.style.width = pct + '%';
    }
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();

    if (reduceMotion) return;

    /* ── Tilt 3D cards ───────────────────── */
    var tilts = document.querySelectorAll('.tilt');
    tilts.forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(900px) rotateX(' + (-y * 8).toFixed(2) + 'deg) rotateY(' + (x * 10).toFixed(2) + 'deg)';
      });
      el.addEventListener('mouseleave', function () {
        el.style.transform = 'perspective(900px) rotateX(0) rotateY(0)';
      });
    });

    /* ── Magnetic buttons ────────────────── */
    var magnets = document.querySelectorAll('.magnetic');
    magnets.forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2;
        var y = e.clientY - r.top - r.height / 2;
        el.style.transform = 'translate(' + (x * 0.2).toFixed(1) + 'px, ' + (y * 0.25).toFixed(1) + 'px)';
      });
      el.addEventListener('mouseleave', function () {
        el.style.transform = 'translate(0, 0)';
      });
    });

    /* ── Ripple on click ─────────────────── */
    document.querySelectorAll('.btn, .ripple').forEach(function (el) {
      el.classList.add('ripple');
      el.addEventListener('click', function (e) {
        var r = el.getBoundingClientRect();
        var size = Math.max(r.width, r.height);
        var wave = document.createElement('span');
        wave.className = 'ripple__wave';
        wave.style.width = wave.style.height = size + 'px';
        wave.style.left = (e.clientX - r.left - size / 2) + 'px';
        wave.style.top = (e.clientY - r.top - size / 2) + 'px';
        el.appendChild(wave);
        setTimeout(function () { wave.remove(); }, 700);
      });
    });

    /* ── Cursor spotlight ────────────────── */
    document.querySelectorAll('.spotlight').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
        el.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
      });
    });

    /* ── Parallax images ─────────────────── */
    var parallaxEls = document.querySelectorAll('[data-parallax]');
    if (parallaxEls.length) {
      window.addEventListener('scroll', function () {
        var y = window.scrollY;
        parallaxEls.forEach(function (el) {
          var speed = parseFloat(el.getAttribute('data-parallax')) || 0.3;
          el.style.transform = 'translate3d(0,' + (y * speed).toFixed(1) + 'px,0)';
        });
      }, { passive: true });
    }

    /* ── Header hide on scroll down, show up  */
    var header = document.getElementById('header');
    var lastY = window.scrollY;
    if (header) {
      window.addEventListener('scroll', function () {
        var y = window.scrollY;
        if (y > 200 && y > lastY) {
          header.classList.add('header--hidden');
        } else {
          header.classList.remove('header--hidden');
        }
        lastY = y;
      }, { passive: true });
    }
  });
})();
