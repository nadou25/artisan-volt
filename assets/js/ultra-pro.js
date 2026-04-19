/* ============================================
   ULTRA-PRO JS — Artisan Volt
   Validation formulaires + micro-interactions
   ============================================ */

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /**
   * Marque une image comme chargee (supprime le shimmer).
   * @param {HTMLImageElement} img
   */
  function markImageLoaded(img) {
    img.classList.add('loaded');
  }

  /* ── Image loading state ─────────────────── */
  document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
    if (img.complete) {
      markImageLoaded(img);
    } else {
      img.addEventListener('load', function () { markImageLoaded(img); }, { once: true });
      img.addEventListener('error', function () { markImageLoaded(img); }, { once: true });
    }
  });

  /* ── Validation formulaire accessible ────── */
  /**
   * @param {HTMLInputElement | HTMLTextAreaElement} field
   * @param {string} message
   */
  function showFieldError(field, message) {
    field.setAttribute('aria-invalid', 'true');
    const id = field.id || field.name;
    let errorEl = document.getElementById(`err-${id}`);
    if (!errorEl) {
      errorEl = document.createElement('span');
      errorEl.id = `err-${id}`;
      errorEl.className = 'form-error-message';
      errorEl.setAttribute('role', 'alert');
      errorEl.setAttribute('aria-live', 'polite');
      field.insertAdjacentElement('afterend', errorEl);
    }
    errorEl.textContent = message;
    field.setAttribute('aria-describedby', errorEl.id);
  }

  /**
   * @param {HTMLInputElement | HTMLTextAreaElement} field
   */
  function clearFieldError(field) {
    field.setAttribute('aria-invalid', 'false');
    const id = field.id || field.name;
    const errorEl = document.getElementById(`err-${id}`);
    if (errorEl) {
      errorEl.textContent = '';
    }
  }

  /**
   * @param {HTMLInputElement | HTMLTextAreaElement} field
   * @returns {boolean}
   */
  function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');

    if (required && !value) {
      showFieldError(field, 'Ce champ est obligatoire.');
      return false;
    }

    if (value && type === 'email') {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        showFieldError(field, 'Veuillez saisir une adresse email valide.');
        return false;
      }
    }

    if (value && type === 'tel') {
      const phoneRegex = /^[+\d\s().-]{6,20}$/;
      if (!phoneRegex.test(value)) {
        showFieldError(field, 'Veuillez saisir un numero de telephone valide.');
        return false;
      }
    }

    if (value && field.minLength > 0 && value.length < field.minLength) {
      showFieldError(field, `Minimum ${field.minLength} caracteres requis.`);
      return false;
    }

    clearFieldError(field);
    return true;
  }

  document.querySelectorAll('form').forEach(function (form) {
    const fields = form.querySelectorAll('input, textarea, select');

    fields.forEach(function (field) {
      if (field.type === 'submit' || field.type === 'button' || field.type === 'hidden') return;

      field.addEventListener('blur', function () { validateField(field); });
      field.addEventListener('input', function () {
        if (field.getAttribute('aria-invalid') === 'true') {
          validateField(field);
        }
      });
    });

    form.addEventListener('submit', function (e) {
      let valid = true;
      let firstInvalid = null;

      fields.forEach(function (field) {
        if (field.type === 'submit' || field.type === 'button' || field.type === 'hidden') return;
        if (!validateField(field)) {
          valid = false;
          if (!firstInvalid) firstInvalid = field;
        }
      });

      if (!valid) {
        e.preventDefault();
        if (firstInvalid) {
          firstInvalid.focus();
          if (!prefersReducedMotion) {
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
      }
    });
  });

  /* ── Ripple effect boutons ──────────────── */
  if (!prefersReducedMotion) {
    document.querySelectorAll('.btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        const rect = btn.getBoundingClientRect();
        const ripple = document.createElement('span');
        const size = Math.max(rect.width, rect.height);
        ripple.style.cssText = `
          position: absolute;
          left: ${e.clientX - rect.left - size / 2}px;
          top: ${e.clientY - rect.top - size / 2}px;
          width: ${size}px;
          height: ${size}px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.4);
          transform: scale(0);
          animation: ripple-anim 0.6s ease-out;
          pointer-events: none;
          z-index: 0;
        `;
        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.appendChild(ripple);
        setTimeout(function () { ripple.remove(); }, 600);
      });
    });

    if (!document.getElementById('ripple-keyframes')) {
      const style = document.createElement('style');
      style.id = 'ripple-keyframes';
      style.textContent = '@keyframes ripple-anim { to { transform: scale(2.5); opacity: 0; } }';
      document.head.appendChild(style);
    }
  }

  /* ── Header shadow au scroll ────────────── */
  const header = document.querySelector('.header');
  if (header) {
    let scrolled = false;
    const updateHeader = function () {
      const shouldBeScrolled = window.scrollY > 20;
      if (shouldBeScrolled !== scrolled) {
        scrolled = shouldBeScrolled;
        header.classList.toggle('header--scrolled', scrolled);
      }
    };
    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();
  }

  /* ── External links security ────────────── */
  document.querySelectorAll('a[target="_blank"]').forEach(function (link) {
    const rel = link.getAttribute('rel') || '';
    if (!rel.includes('noopener')) {
      link.setAttribute('rel', (rel + ' noopener noreferrer').trim());
    }
  });

})();
