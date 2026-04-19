/* ============================================
   Artisan Volt — Main JavaScript
   Navigation, Scroll Reveal, Counters
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ── Mobile Navigation (robust tactile) ──── */
  var menuToggle = document.getElementById('menu-toggle');
  var nav = document.getElementById('nav');
  var navOverlay = document.getElementById('nav-overlay');

  function openMenu() {
    if (!nav) return;
    nav.classList.add('nav--open');
    if (menuToggle) {
      menuToggle.classList.add('menu-toggle--active');
      menuToggle.setAttribute('aria-expanded', 'true');
    }
    if (navOverlay) navOverlay.classList.add('nav-overlay--visible');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    if (!nav) return;
    nav.classList.remove('nav--open');
    if (menuToggle) {
      menuToggle.classList.remove('menu-toggle--active');
      menuToggle.setAttribute('aria-expanded', 'false');
    }
    if (navOverlay) navOverlay.classList.remove('nav-overlay--visible');
    document.body.style.overflow = '';
  }

  function toggleMenu(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    if (!nav) return;
    if (nav.classList.contains('nav--open')) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  if (menuToggle && nav) {
    // Click (desktop + tap iOS)
    menuToggle.addEventListener('click', toggleMenu);
    // Pointerup (plus reactif sur certains Android)
    menuToggle.addEventListener('pointerup', function (e) {
      if (e.pointerType === 'touch') toggleMenu(e);
    });

    // Overlay ferme le menu
    if (navOverlay) {
      navOverlay.addEventListener('click', closeMenu);
      navOverlay.addEventListener('touchend', function (e) { e.preventDefault(); closeMenu(); }, { passive: false });
    }

    // Fermer au clic sur un lien (sauf dropdown toggle)
    var navLinks = nav.querySelectorAll('a.nav__link, .nav__dropdown-link');
    navLinks.forEach(function (link) {
      link.addEventListener('click', function () { closeMenu(); });
    });

    // Dropdown "Plus" dans le menu mobile
    var dropdownToggles = nav.querySelectorAll('.nav__dropdown-toggle');
    dropdownToggles.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var parent = btn.closest('.nav__dropdown');
        if (parent) parent.classList.toggle('nav__dropdown--open');
        var expanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!expanded));
      });
    });

    // Echap ferme
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  /* ── Header Scroll Effect ───────────────── */
  var header = document.getElementById('header');
  if (header) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        header.classList.add('header--scrolled');
      } else {
        header.classList.remove('header--scrolled');
      }
    }, { passive: true });
  }

  /* ── Scroll Reveal ──────────────────────── */
  var reveals = document.querySelectorAll('.reveal');

  if (reveals.length > 0 && 'IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal--visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '0px 0px -50px 0px'
    });

    reveals.forEach(function (el) {
      revealObserver.observe(el);
    });
  } else {
    // Fallback: show all elements
    reveals.forEach(function (el) {
      el.classList.add('reveal--visible');
    });
  }

  /* ── Animated Counters ──────────────────── */
  var counters = document.querySelectorAll('[data-count]');

  if (counters.length > 0 && 'IntersectionObserver' in window) {
    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(function (counter) {
      counterObserver.observe(counter);
    });
  }

  function animateCounter(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var suffix = el.getAttribute('data-suffix');
    if (suffix === null) suffix = '+';
    var duration = 2000;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.floor(eased * target);

      el.textContent = current + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target + suffix;
      }
    }

    requestAnimationFrame(step);
  }

  /* ── FAQ Accordion ──────────────────────── */
  var accordionTriggers = document.querySelectorAll('.accordion__trigger');

  accordionTriggers.forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      var item = this.closest('.accordion__item');
      var isActive = item.classList.contains('accordion__item--active');

      // Close all items
      document.querySelectorAll('.accordion__item--active').forEach(function (active) {
        active.classList.remove('accordion__item--active');
      });

      // Open clicked if it was closed
      if (!isActive) {
        item.classList.add('accordion__item--active');
      }
    });
  });

  /* ── Lightbox ───────────────────────────── */
  var lightbox = document.getElementById('lightbox');
  var lightboxImg = document.getElementById('lightbox-img');
  var lightboxClose = document.getElementById('lightbox-close');
  var portfolioItems = document.querySelectorAll('.portfolio-item');

  portfolioItems.forEach(function (item) {
    item.addEventListener('click', function () {
      var img = this.querySelector('img');
      if (lightbox && lightboxImg && img) {
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightbox.classList.add('lightbox--active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
  }

  if (lightbox) {
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lightbox.classList.contains('lightbox--active')) {
        closeLightbox();
      }
    });
  }

  function closeLightbox() {
    if (lightbox) {
      lightbox.classList.remove('lightbox--active');
      document.body.style.overflow = '';
    }
  }

  /* ── Portfolio Filters ──────────────────── */
  var filterButtons = document.querySelectorAll('.portfolio-filter');
  var portfolioGridItems = document.querySelectorAll('.portfolio-item');

  filterButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var filter = this.getAttribute('data-filter');

      filterButtons.forEach(function (b) {
        b.classList.remove('portfolio-filter--active');
      });
      this.classList.add('portfolio-filter--active');

      portfolioGridItems.forEach(function (item) {
        if (filter === 'all' || item.getAttribute('data-category') === filter) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  /* ── Form Validation ────────────────────── */
  var forms = document.querySelectorAll('form[data-validate]');

  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      var isValid = true;
      var requiredFields = form.querySelectorAll('[required]');

      requiredFields.forEach(function (field) {
        if (!field.value.trim()) {
          isValid = false;
          field.style.borderColor = 'var(--color-error)';
        } else {
          field.style.borderColor = '';
        }
      });

      // Email validation
      var emailField = form.querySelector('input[type="email"]');
      if (emailField && emailField.value) {
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailField.value)) {
          isValid = false;
          emailField.style.borderColor = 'var(--color-error)';
        }
      }

      if (!isValid) {
        e.preventDefault();
      }
    });
  });

  /* ── Smooth scroll for anchor links ─────── */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── Header scroll state (glass plus dense au scroll) ─── */
  var header = document.querySelector('.header');
  if (header) {
    var updateHeader = function () {
      var scrolled = window.scrollY > 8;
      header.classList.toggle('is-scrolled', scrolled);
      header.setAttribute('data-scrolled', String(scrolled));
    };
    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });
  }

  /* ── Bulb interactive toggle ──────────────── */
  var bulb = document.querySelector('[data-bulb]');
  if (bulb) {
    var toggle = function () {
      var on = bulb.getAttribute('aria-pressed') === 'true';
      bulb.setAttribute('aria-pressed', String(!on));
      bulb.setAttribute('aria-label', !on ? 'Eteindre l\'ampoule' : 'Allumer l\'ampoule');
    };
    bulb.addEventListener('click', toggle);
    bulb.addEventListener('touchend', function (e) { e.preventDefault(); toggle(); }, { passive: false });
    bulb.addEventListener('keydown', function (e) {
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); }
    });
    setTimeout(function () { if (bulb.getAttribute('aria-pressed') !== 'true') bulb.setAttribute('aria-pressed', 'true'); }, 1200);
  }

});
