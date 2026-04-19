/* ============================================
   WOW TECH — Artisan Volt
   Particle network (hero + page-hero), counters,
   gradient orbs, text reveal, parallax, dropdown
   ============================================ */
(function () {
  'use strict';
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;

  /* ── Utilitaire rAF throttle ─────────────── */
  function rafThrottle(fn) {
    var pending = false;
    return function (e) {
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () { fn(e); pending = false; });
    };
  }

  document.addEventListener('DOMContentLoaded', function () {

    /* ────────────────────────────────────────────
       1. HEADER glassmorphism au scroll
    ──────────────────────────────────────────── */
    var header = document.getElementById('header');
    if (header) {
      function onScroll() {
        header.classList.toggle('header--scrolled', window.scrollY > 60);
      }
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }

    /* ────────────────────────────────────────────
       2. PARTICLE NETWORK — hero ET page-hero
    ──────────────────────────────────────────── */
    if (!reduceMotion) {
      document.querySelectorAll('.hero, .page-hero').forEach(function (section) {
        if (section.querySelector('canvas.particle-net')) return;

        var canvas = document.createElement('canvas');
        canvas.className = 'particle-net';
        canvas.setAttribute('aria-hidden', 'true');
        canvas.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:1;';
        section.style.position = 'relative';
        section.insertBefore(canvas, section.firstChild);

        var ctx = canvas.getContext('2d');
        var W, H, dpr, pts;
        var mx = -9999, my = -9999;
        var imgZone = null; /* zone photo hero à exclure */

        function resize() {
          dpr = Math.min(window.devicePixelRatio || 1, 2);
          var r = section.getBoundingClientRect();
          W = r.width || window.innerWidth;
          H = r.height || 500;
          canvas.width = W * dpr; canvas.height = H * dpr;
          canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
          ctx.setTransform(1,0,0,1,0,0);
          ctx.scale(dpr, dpr);
          var n = Math.max(20, Math.min(55, Math.floor((W * H) / 20000)));
          pts = Array.from({ length: n }, function () {
            return {
              x: Math.random() * W, y: Math.random() * H,
              vx: (Math.random() - 0.5) * 0.3,
              vy: (Math.random() - 0.5) * 0.3,
              r: 1.4 + Math.random()
            };
          });
          /* Calcule la zone de la photo (hero__image) relative à la section */
          var imgEl = section.querySelector('.hero__image');
          if (imgEl) {
            var ir = imgEl.getBoundingClientRect();
            imgZone = {
              x: ir.left - r.left,
              y: ir.top  - r.top,
              w: ir.width,
              h: ir.height
            };
          }
        }
        resize();
        window.addEventListener('resize', rafThrottle(resize));

        section.addEventListener('mousemove', rafThrottle(function (e) {
          var r = section.getBoundingClientRect();
          mx = e.clientX - r.left; my = e.clientY - r.top;
        }));
        section.addEventListener('mouseleave', function () { mx = -9999; my = -9999; });

        /* Renvoie true si le point (x,y) est dans la zone photo */
        function inPhoto(x, y) {
          return imgZone &&
            x > imgZone.x && x < imgZone.x + imgZone.w &&
            y > imgZone.y && y < imgZone.y + imgZone.h;
        }

        var alive = true;
        (function frame() {
          if (!alive) return;
          ctx.clearRect(0, 0, W, H);
          for (var i = 0; i < pts.length; i++) {
            var p = pts[i];
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0 || p.x > W) p.vx *= -1;
            if (p.y < 0 || p.y > H) p.vy *= -1;

            /* Ne pas dessiner le dot s'il est sur la photo */
            if (inPhoto(p.x, p.y)) continue;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(0,102,255,0.55)';
            ctx.fill();

            for (var j = i + 1; j < pts.length; j++) {
              var q = pts[j];
              /* Ne pas tracer de ligne si l'un des deux points est sur la photo */
              if (inPhoto(q.x, q.y)) continue;
              var dx = p.x - q.x, dy = p.y - q.y;
              var d2 = dx * dx + dy * dy;
              if (d2 < 18000) {
                var d = Math.sqrt(d2);
                ctx.strokeStyle = 'rgba(0,102,255,' + ((1 - d / 135) * 0.22) + ')';
                ctx.lineWidth = 0.6;
                ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
              }
            }
          }
          /* ── Lignes électriques curseur → page 1, hors zone photo ── */
          var overImg = imgZone &&
            mx > imgZone.x && mx < imgZone.x + imgZone.w &&
            my > imgZone.y && my < imgZone.y + imgZone.h;
          if (mx > 0 && !overImg) {
            ctx.save();
            ctx.shadowColor = 'rgba(100, 200, 255, 0.9)';
            ctx.shadowBlur = 8;
            for (var k = 0; k < pts.length; k++) {
              var pk = pts[k];
              var cdx = mx - pk.x, cdy = my - pk.y;
              var cd2 = cdx * cdx + cdy * cdy;
              if (cd2 < 28000) {
                var cd = Math.sqrt(cd2);
                var alpha = (1 - cd / 168) * 0.92;
                ctx.strokeStyle = 'rgba(210, 240, 255,' + alpha + ')';
                ctx.lineWidth = 1.6;
                ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(pk.x, pk.y); ctx.stroke();
              }
            }
            ctx.restore();
          }
          requestAnimationFrame(frame);
        })();
      });
    }

    /* gradient-orb parallax supprimé (user request) */

    /* ────────────────────────────────────────────
       4. TEXT GRADIENT REVEAL au scroll
    ──────────────────────────────────────────── */
    var gradTexts = document.querySelectorAll('.text-reveal-grad');
    if (gradTexts.length) {
      var grObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add('revealed');
            grObs.unobserve(e.target);
          }
        });
      }, { threshold: 0.4 });
      gradTexts.forEach(function (el) { grObs.observe(el); });
    }

    /* ────────────────────────────────────────────
       6. PARALLAX MOUSE — hero content
    ──────────────────────────────────────────── */
    if (!reduceMotion && !isTouch) {
      var heroContent = document.querySelector('.hero__content');
      var heroImage  = document.querySelector('.hero__image');
      if (heroContent && heroImage) {
        document.addEventListener('mousemove', rafThrottle(function (e) {
          var x = e.clientX / window.innerWidth  - 0.5;
          var y = e.clientY / window.innerHeight - 0.5;
          heroContent.style.transform = 'translate(' + (x * 8) + 'px,' + (y * 5) + 'px)';
          heroImage.style.transform   = 'translate(' + (x * -12) + 'px,' + (y * -8) + 'px)';
        }));
      }

      /* Parallax générique sur [data-parallax] */
      document.querySelectorAll('[data-parallax]').forEach(function (el) {
        var speed = parseFloat(el.getAttribute('data-parallax')) || 12;
        document.addEventListener('mousemove', rafThrottle(function (e) {
          var x = (e.clientX / window.innerWidth  - 0.5) * speed;
          var y = (e.clientY / window.innerHeight - 0.5) * speed;
          el.style.transform = 'translate(' + x + 'px,' + y + 'px)';
        }));
      });
    }

    /* ────────────────────────────────────────────
       8. 3D TILT — toutes les cards
    ──────────────────────────────────────────── */
    if (!reduceMotion && !isTouch) {
      var tiltEls = document.querySelectorAll(
        '.card-service, .card-pricing, .post-card, .team-card, ' +
        '.testimonial-card, .portfolio-item, .hero__image, .zoom-img, ' +
        '.contact-card'
      );
      tiltEls.forEach(function (card) {
        var bounds = null;

        card.addEventListener('mouseenter', function () {
          bounds = card.getBoundingClientRect();
          card.style.transition =
            'transform 80ms linear, box-shadow 380ms ease, border-color 300ms ease';
          card.style.willChange = 'transform';
        });

        card.addEventListener('mousemove', rafThrottle(function (e) {
          if (!bounds) return;
          var x = e.clientX - bounds.left;
          var y = e.clientY - bounds.top;
          var rx = ((y / bounds.height) - 0.5) * -14; /* ±7 deg */
          var ry = ((x / bounds.width)  - 0.5) *  14;
          card.style.transform =
            'perspective(900px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)' +
            ' translateY(-6px) scale(1.02)';
        }));

        card.addEventListener('mouseleave', function () {
          card.style.transition =
            'transform 500ms cubic-bezier(.2,.7,.2,1), box-shadow 380ms ease, border-color 300ms ease';
          card.style.transform = '';
          setTimeout(function () {
            card.style.willChange = '';
            card.style.transition = '';
          }, 520);
          bounds = null;
        });
      });
    }

    /* ────────────────────────────────────────────
       8. DROPDOWN NAV
    ──────────────────────────────────────────── */
    document.querySelectorAll('.nav__dropdown').forEach(function (dd) {
      var toggle = dd.querySelector('.nav__dropdown-toggle');
      var menu   = dd.querySelector('.nav__dropdown-menu');
      if (!toggle || !menu) return;

      toggle.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = dd.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(open));
      });
      document.addEventListener('click', function () {
        dd.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
      menu.addEventListener('click', function (e) { e.stopPropagation(); });
      toggle.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
          dd.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
          toggle.focus();
        }
      });
    });

  });
})();
