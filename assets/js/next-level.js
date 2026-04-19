/* ============================================
   NEXT LEVEL — Interactions Ultra Pro
   - Disponibilite temps reel
   - Validation formulaire inline
   - Feedback soumission
   - Annee copyright
   ============================================ */

(function () {
  'use strict';

  // ── 1. Disponibilite temps reel ────────────
  function updateAvailability() {
    const badges = document.querySelectorAll('[data-availability]');
    if (!badges.length) return;

    const now = new Date();
    const day = now.getDay();
    const hour = now.getHours();

    // Horaires : Lun-Ven 8-18h, Sam 9-12h, Dim ferme (mais urgences 24/7)
    let status, label;
    const isWeekday = day >= 1 && day <= 5;
    const isSaturday = day === 6;

    if (isWeekday && hour >= 8 && hour < 18) {
      status = 'open';
      label = 'Disponible maintenant';
    } else if (isSaturday && hour >= 9 && hour < 12) {
      status = 'open';
      label = 'Disponible maintenant';
    } else {
      status = 'closed';
      label = 'Urgences 24h/7j - Appel prioritaire';
    }

    badges.forEach(badge => {
      badge.dataset.status = status;
      const labelEl = badge.querySelector('.availability-badge__label');
      if (labelEl) labelEl.textContent = label;
    });
  }

  // ── 2. Validation formulaire inline ─────────
  function setupFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
      const fields = form.querySelectorAll('input, textarea, select');

      fields.forEach(field => {
        if (field.type === 'hidden' || field.name === '_honey') return;

        field.addEventListener('blur', () => validateField(field));
        field.addEventListener('input', () => {
          const wrapper = field.closest('.form-field') || field.parentElement;
          if (wrapper && wrapper.classList.contains('is-invalid')) {
            validateField(field);
          }
        });
      });

      form.addEventListener('submit', (e) => {
        let allValid = true;
        fields.forEach(field => {
          if (field.type === 'hidden' || field.name === '_honey') return;
          if (!validateField(field)) allValid = false;
        });

        if (!allValid) {
          e.preventDefault();
          const firstInvalid = form.querySelector('.is-invalid input, .is-invalid textarea, .is-invalid select');
          if (firstInvalid) firstInvalid.focus();

          announce(form, 'Le formulaire contient des erreurs. Merci de verifier les champs en rouge.');
        } else {
          announce(form, 'Envoi en cours...');
        }
      });
    });
  }

  function validateField(field) {
    const wrapper = field.closest('.form-field') || field.parentElement;
    if (!wrapper) return true;

    const value = (field.value || '').trim();
    let valid = true;
    let message = '';

    if (field.required && !value) {
      valid = false;
      message = 'Ce champ est obligatoire.';
    } else if (field.type === 'email' && value) {
      const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRe.test(value)) {
        valid = false;
        message = 'Format d\'email invalide.';
      }
    } else if (field.type === 'tel' && value) {
      const telRe = /^[\d\s+().-]{8,}$/;
      if (!telRe.test(value)) {
        valid = false;
        message = 'Numero de telephone invalide.';
      }
    } else if (field.minLength && value.length > 0 && value.length < field.minLength) {
      valid = false;
      message = `Minimum ${field.minLength} caracteres (${value.length} actuels).`;
    }

    wrapper.classList.toggle('is-invalid', !valid);
    wrapper.classList.toggle('is-valid', valid && value.length > 0);

    let errEl = wrapper.querySelector('.form-error-msg');
    if (!valid) {
      if (!errEl) {
        errEl = document.createElement('span');
        errEl.className = 'form-error-msg';
        errEl.setAttribute('role', 'alert');
        wrapper.appendChild(errEl);
      }
      errEl.textContent = message;
      field.setAttribute('aria-invalid', 'true');
    } else {
      if (errEl) errEl.textContent = '';
      field.removeAttribute('aria-invalid');
    }

    return valid;
  }

  function announce(form, message) {
    let status = form.querySelector('[role="status"]');
    if (!status) {
      status = document.createElement('div');
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      status.className = 'visually-hidden';
      form.prepend(status);
    }
    status.textContent = message;
  }

  // ── 3. Annee copyright automatique ─────────
  function updateYear() {
    const yearEls = document.querySelectorAll('[data-year]');
    yearEls.forEach(el => el.textContent = new Date().getFullYear());
  }

  // ── 4. Smooth scroll pour ancres ───────────
  function setupSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const id = this.getAttribute('href').slice(1);
        const target = document.getElementById(id);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          target.setAttribute('tabindex', '-1');
          target.focus({ preventScroll: true });
        }
      });
    });
  }

  // ── 5. FAQ recherche ───────────────────────
  function setupFaqSearch() {
    const searchInput = document.querySelector('[data-faq-search]');
    if (!searchInput) return;

    const items = document.querySelectorAll('.accordion__item, .faq-item');
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.toLowerCase().trim();
      items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = (!query || text.includes(query)) ? '' : 'none';
      });
    });
  }

  // ── Init ──────────────────────────────────
  function init() {
    updateAvailability();
    setupFormValidation();
    updateYear();
    setupSmoothAnchors();
    setupFaqSearch();
    // Refresh dispo toutes les minutes
    setInterval(updateAvailability, 60000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
