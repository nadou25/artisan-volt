# Artisan Volt — Site Vitrine

Site vitrine professionnel pour **Artisan Volt**, électricien à Versailles (78) et dans les Yvelines.

Site statique HTML5 / CSS3 / Vanilla JavaScript — aucune dépendance, ultra-rapide, responsive, accessible WCAG 2.1 AA.

## Aperçu

- **14 pages** : Accueil, Services, Réalisations, Tarifs, À propos, Équipe, Témoignages, FAQ, Blog, Contact, Réservation, Mentions légales, Politique de confidentialité, 404
- **Design system** : palette "Versailles Voltage" (bleu nuit royal + or signalétique + cuivre artisan)
- **Typographies** : Montserrat (titres) + Inter (corps)
- **Header glass sticky** avec backdrop-blur au style moderne
- **Animations** CSS premium et interactions au scroll
- **SEO optimisé** : Schema.org LocalBusiness, Open Graph, sitemap.xml, robots.txt
- **Accessibilité** : navigation clavier, contrastes WCAG AA, `prefers-reduced-motion`
- **Performance** : images WebP, preload fonts, CSS/JS minimal

## Structure

```
├── index.html              # Accueil
├── services.html           # Services
├── portfolio.html          # Réalisations
├── pricing.html            # Tarifs
├── about.html              # À propos
├── team.html               # Équipe
├── testimonials.html       # Témoignages
├── faq.html                # FAQ
├── blog.html               # Blog
├── contact.html            # Contact
├── booking.html            # Réservation
├── legal.html              # Mentions légales
├── privacy.html            # Politique de confidentialité
├── 404.html                # Page d'erreur
├── assets/
│   ├── css/                # Design system + composants + polish
│   ├── js/                 # Navigation, animations, interactions
│   ├── images/             # Photos WebP, logos SVG
│   └── fonts/              # (Google Fonts via CDN)
├── sitemap.xml
└── robots.txt
```

## Lancer en local

```bash
python -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Déploiement

Compatible GitHub Pages / Netlify / Vercel / tout hébergeur statique.

### GitHub Pages

1. Pousser sur la branche `main`
2. Settings → Pages → Source : `main` / `/ (root)`
3. Site disponible à `https://<user>.github.io/<repo>/`

## Contact

**Artisan Volt** — Électricien à Versailles
- 24 rue André Campra, 78000 Versailles
- 07 84 86 82 07
- contact@artisanvolt.fr

---

© 2026 Artisan Volt — Tous droits réservés
