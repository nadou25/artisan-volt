/**
 * Hero Electric — effet curseur electrique premium
 * - Arcs zigzag entre curseur et elements [data-spark]
 * - Etincelles dorees aux extremites
 * - 60fps, pause si onglet cache, desactive mobile/reduce-motion
 *
 * Usage : <canvas class="hero__fx" data-hero-fx></canvas> dans .hero
 *         Ajouter data-spark sur h1, CTA, logo visibles dans le hero
 */
(function () {
  'use strict';

  const REDUCE_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const IS_TOUCH = window.matchMedia('(hover: none)').matches;
  if (REDUCE_MOTION || IS_TOUCH) return;

  const canvas = document.querySelector('canvas[data-hero-fx]');
  if (!canvas) return;

  const hero = canvas.closest('.hero, .page-hero, [data-electric-zone]');
  if (!hero) return;

  const ctx = canvas.getContext('2d');
  const DPR = Math.min(2, window.devicePixelRatio || 1);

  // Minimaliste : une seule ligne doree fine, pas de double halo
  const CONFIG = {
    triggerDistance: 260,
    arcSegments: 7,
    arcJitter: 5,
    arcLifetime: 260,
    arcCooldown: 110,
    lineWidth: 1,
    sparkMax: 12,
    sparkLifetime: 520,
    colorLine: '217, 119, 6',
    colorSpark: '251, 191, 36'
  };

  let width = 0;
  let height = 0;
  let mouse = { x: -9999, y: -9999, active: false };
  let anchors = [];
  let arcs = [];
  let sparks = [];
  let lastArcTime = 0;
  let rafId = null;

  function resize() {
    const rect = hero.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    canvas.width = width * DPR;
    canvas.height = height * DPR;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    refreshAnchors();
  }

  function refreshAnchors() {
    const heroRect = hero.getBoundingClientRect();
    const nodes = hero.querySelectorAll('[data-spark]');
    anchors = Array.from(nodes).map((node) => {
      const r = node.getBoundingClientRect();
      return {
        x: r.left - heroRect.left + r.width / 2,
        y: r.top - heroRect.top + r.height / 2
      };
    });
  }

  function onMove(event) {
    const rect = hero.getBoundingClientRect();
    mouse.x = event.clientX - rect.left;
    mouse.y = event.clientY - rect.top;
    mouse.active = true;
    maybeSpawnArc(performance.now());
  }

  function onLeave() {
    mouse.active = false;
  }

  function dist(ax, ay, bx, by) {
    const dx = ax - bx;
    const dy = ay - by;
    return Math.sqrt(dx * dx + dy * dy);
  }

  function maybeSpawnArc(now) {
    if (!mouse.active) return;
    if (now - lastArcTime < CONFIG.arcCooldown) return;

    let closest = null;
    let closestDist = CONFIG.triggerDistance;
    for (const a of anchors) {
      const d = dist(mouse.x, mouse.y, a.x, a.y);
      if (d < closestDist) {
        closestDist = d;
        closest = a;
      }
    }
    if (!closest) return;

    arcs.push({
      startX: mouse.x,
      startY: mouse.y,
      endX: closest.x,
      endY: closest.y,
      born: now,
      seed: Math.random()
    });
    spawnSparks(closest.x, closest.y, 2);
    spawnSparks(mouse.x, mouse.y, 1);
    lastArcTime = now;
  }

  function spawnSparks(x, y, count) {
    for (let i = 0; i < count; i++) {
      if (sparks.length >= CONFIG.sparkMax) sparks.shift();
      const angle = Math.random() * Math.PI * 2;
      const speed = 0.3 + Math.random() * 0.9;
      sparks.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 0.2,
        born: performance.now(),
        size: 1 + Math.random() * 1.5
      });
    }
  }

  function drawArc(arc, progress) {
    const { startX, startY, endX, endY, seed } = arc;
    const alpha = 1 - progress;

    ctx.save();
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.shadowBlur = 6;
    ctx.shadowColor = `rgba(${CONFIG.colorLine}, ${0.4 * alpha})`;
    ctx.strokeStyle = `rgba(${CONFIG.colorLine}, ${0.85 * alpha})`;
    ctx.lineWidth = CONFIG.lineWidth;
    drawZigzag(startX, startY, endX, endY, CONFIG.arcSegments, CONFIG.arcJitter, seed);
    ctx.restore();
  }

  function drawZigzag(x1, y1, x2, y2, segments, jitter, seed) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    for (let i = 1; i < segments; i++) {
      const t = i / segments;
      const baseX = x1 + (x2 - x1) * t;
      const baseY = y1 + (y2 - y1) * t;
      const offset = (pseudoRandom(seed + i) - 0.5) * jitter * 2;
      const perpX = -(y2 - y1);
      const perpY = (x2 - x1);
      const len = Math.sqrt(perpX * perpX + perpY * perpY) || 1;
      ctx.lineTo(baseX + (perpX / len) * offset, baseY + (perpY / len) * offset);
    }
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  function pseudoRandom(n) {
    const x = Math.sin(n * 9301 + 49297) * 10000;
    return x - Math.floor(x);
  }

  function drawSpark(spark, progress) {
    const alpha = 1 - progress;
    const radius = spark.size * (1 + progress * 0.3);
    const gradient = ctx.createRadialGradient(spark.x, spark.y, 0, spark.x, spark.y, radius * 3);
    gradient.addColorStop(0, `rgba(${CONFIG.colorSpark}, ${alpha * 0.85})`);
    gradient.addColorStop(1, `rgba(${CONFIG.colorLine}, 0)`);
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(spark.x, spark.y, radius * 3, 0, Math.PI * 2);
    ctx.fill();
  }

  function tick() {
    if (document.hidden) {
      rafId = requestAnimationFrame(tick);
      return;
    }
    const now = performance.now();
    ctx.clearRect(0, 0, width, height);

    arcs = arcs.filter((arc) => {
      const progress = (now - arc.born) / CONFIG.arcLifetime;
      if (progress >= 1) return false;
      drawArc(arc, progress);
      return true;
    });

    sparks = sparks.filter((spark) => {
      const progress = (now - spark.born) / CONFIG.sparkLifetime;
      if (progress >= 1) return false;
      spark.x += spark.vx;
      spark.y += spark.vy;
      spark.vy += 0.018;
      drawSpark(spark, progress);
      return true;
    });

    rafId = requestAnimationFrame(tick);
  }

  resize();
  let resizeRaf = null;
  window.addEventListener('resize', () => {
    if (resizeRaf) cancelAnimationFrame(resizeRaf);
    resizeRaf = requestAnimationFrame(resize);
  });
  window.addEventListener('scroll', () => {
    if (resizeRaf) cancelAnimationFrame(resizeRaf);
    resizeRaf = requestAnimationFrame(refreshAnchors);
  }, { passive: true });

  hero.addEventListener('mousemove', onMove);
  hero.addEventListener('mouseleave', onLeave);

  rafId = requestAnimationFrame(tick);
})();
