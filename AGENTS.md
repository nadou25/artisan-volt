# VitrinePro Studio — Agence de Création de Sites Vitrines

## Mission

Système de workflow professionnel pour la création de sites vitrines sur mesure.
Chaque commande `/creation-site` déclenche un pipeline complet d'agence digitale.

---

## Commande Principale : Création de Site

Quand l'utilisateur demande une **création de site**, exécuter ce protocole :

### Etape 0 — Brief Client Interactif

Poser les questions suivantes dans l'ordre (attendre les réponses) :

```
1. DOMAINE D'ACTIVITE
   → Restaurant, Avocat, Médecin, Artisan, Immobilier, Coach,
     Photographe, Architecte, Salon de coiffure, Auto-école,
     Consultant, Autre (préciser)

2. NOM DU PROJET / ENTREPRISE
   → Nom commercial + slogan si existant

3. STYLE VISUEL (choisir 1-2)
   → Minimaliste | Luxe/Premium | Moderne/Tech | Chaleureux/Artisanal
     Corporate/Sérieux | Créatif/Artistique | Eco/Nature | Bold/Impact

4. PALETTE DE COULEURS (choisir ou laisser proposer)
   → Couleur principale souhaitée ou "proposer selon le domaine"

5. PAGES SOUHAITEES (cocher)
   → [x] Accueil  [x] A propos  [x] Services  [x] Contact
     [ ] Portfolio/Galerie  [ ] Tarifs  [ ] Blog  [ ] Temoignages
     [ ] FAQ  [ ] Reservation en ligne  [ ] Equipe

6. FONCTIONNALITES
   → Formulaire de contact | Google Maps | Galerie photos
     Reservation/Calendrier | Chat en direct | Newsletter
     Avis clients | Reseaux sociaux | Multi-langue

7. CONTENU
   → "J'ai mon contenu" | "Generez du contenu de demo"
     | "Je fournirai plus tard"

8. REFERENCES / INSPIRATION
   → URLs de sites que le client aime (optionnel)

9. DEADLINE / URGENCE
   → Standard | Urgent (48h) | Express (24h)
```

### Etape 1 — Validation du Brief

Generer un fichier `.workflow/briefs/[nom-projet].md` avec le resume du brief.
Presenter au client pour validation avant de continuer.

### Etape 2 — Lancement du Pipeline

Une fois le brief valide, lancer le pipeline complet (voir phases ci-dessous).

---

## Pipeline de Production — 8 Phases

### Phase 1 : STRATEGIE & RECHERCHE
**Agent** : `planner` + `architect`
**Roles** : Directeur de Projet, Strategiste Digital

- Analyse du domaine et de la concurrence
- Definition de la strategie SEO initiale
- Architecture de l'information (sitemap)
- Choix technologiques (stack)
- Planning de production

**Livrable** : `.workflow/phases/01-strategie.md`

---

### Phase 2 : UX DESIGN
**Agent** : `planner`
**Roles** : UX Designer, Architecte de l'Information

- Wireframes de chaque page (structure)
- Parcours utilisateur (user flows)
- Hierarchie de contenu
- Points de conversion (CTA)
- Responsive breakpoints strategy

**Livrable** : `.workflow/phases/02-ux-design.md`

---

### Phase 3 : UI DESIGN & DIRECTION ARTISTIQUE
**Agent** : `architect` + browser automation
**Roles** : Directeur Artistique, UI Designer

- Palette de couleurs definitive (5 couleurs)
- Typographies (titres + corps)
- Systeme de composants (boutons, cards, formulaires)
- Style des images et illustrations
- Design responsive (mobile-first)
- Animations et micro-interactions

**Livrable** : `.workflow/phases/03-ui-design.md` + design tokens CSS

---

### Phase 4 : DEVELOPPEMENT FRONTEND
**Agent** : `code-reviewer` + `build-error-resolver`
**Roles** : Developpeur Frontend, Integrateur Web

- Setup du projet (HTML/CSS/JS ou framework)
- Integration du design system
- Developpement page par page
- Responsive / Mobile-first
- Animations CSS/JS
- Optimisation des assets (images, fonts)

**Stack par defaut** : HTML5 + CSS3 + Vanilla JS (leger, rapide, pas de dependances)
**Stack avancee** : Astro / Next.js / Nuxt.js (si besoin SSR/SSG)

**Livrable** : Code source fonctionnel

---

### Phase 5 : CONTENU & SEO
**Agent** : `doc-updater`
**Roles** : Redacteur Web, Specialiste SEO

- Redaction / Integration du contenu
- Optimisation SEO on-page (meta, headings, alt)
- Schema.org / donnees structurees
- Open Graph / Twitter Cards
- Sitemap XML + robots.txt
- Google My Business (si local)

**Livrable** : Contenu integre + checklist SEO

---

### Phase 6 : QA & TESTING
**Agent** : `tdd-guide` + `e2e-runner` + `security-reviewer`
**Roles** : QA Engineer, Testeur, Expert Securite

- Tests cross-browser (Chrome, Firefox, Safari, Edge)
- Tests responsive (mobile, tablet, desktop)
- Tests de performance (Lighthouse > 90)
- Tests d'accessibilite (WCAG 2.1 AA)
- Tests de securite (HTTPS, headers, formulaires)
- Validation W3C (HTML + CSS)
- Tests des formulaires et interactions

**Livrable** : `.workflow/phases/06-qa-report.md`

---

### Phase 7 : DEPLOIEMENT
**Agent** : `build-error-resolver`
**Roles** : DevOps, Administrateur Systeme

- Build de production optimise
- Configuration hebergement (Vercel / Netlify / VPS)
- Configuration DNS + SSL
- Redirections et .htaccess
- Configuration CDN
- Monitoring et alertes

**Livrable** : Site en ligne + documentation deploiement

---

### Phase 8 : POST-LANCEMENT
**Agent** : `doc-updater` + `security-reviewer`
**Roles** : Chef de Projet, Analyste

- Configuration Google Analytics / Search Console
- Documentation de maintenance
- Guide d'utilisation client
- Plan de suivi et optimisation
- Rapport de performance initial

**Livrable** : Documentation complete + acces client

---

## Organigramme de l'Agence — Roles & Agents

```
                    DIRECTEUR GENERAL
                    (Orchestrateur principal)
                           |
          +----------------+----------------+
          |                |                |
   DIRECTEUR          DIRECTEUR        DIRECTEUR
   CREATIF           TECHNIQUE         COMMERCIAL
   (architect)       (code-reviewer)   (planner)
     |                    |                |
  +--+--+           +----+----+       +---+---+
  |     |           |    |    |       |       |
  UX    UI        Front Back DevOps  SEO   Contenu
  Designer Designer Dev  Dev Engineer Spec  Redacteur
```

### Mapping Agents Codex ↔ Metiers

| Metier | Agent Codex | Responsabilite |
|--------|-------------|----------------|
| Directeur de Projet | `planner` | Planification, coordination, brief |
| Directeur Creatif | `architect` | Vision artistique, decisions design |
| UX Designer | `planner` | Wireframes, parcours, architecture info |
| UI Designer | `architect` + browser | Design visuel, composants, tokens |
| Dev Frontend | `code-reviewer` | Integration, HTML/CSS/JS |
| Dev Backend | `code-reviewer` | API, formulaires, CMS |
| DevOps | `build-error-resolver` | Build, deploiement, CI/CD |
| QA Engineer | `tdd-guide` + `e2e-runner` | Tests, qualite, performance |
| Expert Securite | `security-reviewer` | Audit securite, HTTPS, headers |
| Redacteur Web | `doc-updater` | Contenu, copywriting |
| Specialiste SEO | `doc-updater` | SEO on-page, donnees structurees |
| Nettoyeur Code | `refactor-cleaner` | Optimisation, dead code, performance |

---

## Standards de Qualite

### Performance (Lighthouse)
- Performance : > 90
- Accessibilite : > 90
- Best Practices : > 90
- SEO : > 90

### Code
- HTML5 semantique et valide W3C
- CSS organise (BEM ou utility-first)
- JS minimal, pas de jQuery
- Images optimisees (WebP, lazy loading)
- Fonts optimisees (preload, subset)

### SEO Minimum
- Balises title et meta description uniques par page
- Headings hierarchiques (h1 unique par page)
- URLs propres et descriptives
- Images avec attribut alt
- Schema.org LocalBusiness (si applicable)
- Sitemap XML + robots.txt

### Accessibilite (WCAG 2.1 AA)
- Contraste suffisant (4.5:1 minimum)
- Navigation au clavier
- Attributs ARIA si necessaire
- Textes alternatifs sur les images
- Focus visible

### Securite
- HTTPS obligatoire
- Headers securite (CSP, X-Frame-Options, etc.)
- Formulaires avec protection CSRF + honeypot
- Pas de donnees sensibles dans le code source
- Dependencies a jour

---

## Conventions de Nommage

```
projet/
├── index.html                  # Page d'accueil
├── about.html                  # A propos
├── services.html               # Services
├── contact.html                # Contact
├── assets/
│   ├── css/
│   │   ├── variables.css       # Design tokens (couleurs, typo, espacements)
│   │   ├── reset.css           # CSS Reset
│   │   ├── base.css            # Styles de base
│   │   ├── components.css      # Composants reutilisables
│   │   ├── layout.css          # Grille et mise en page
│   │   └── pages/              # Styles specifiques par page
│   ├── js/
│   │   ├── main.js             # JS principal
│   │   ├── navigation.js       # Menu mobile
│   │   └── animations.js       # Animations scroll
│   ├── images/
│   │   ├── hero/               # Images hero/banner
│   │   ├── icons/              # Icones SVG
│   │   └── content/            # Images de contenu
│   └── fonts/                  # Polices locales
├── .workflow/
│   ├── briefs/                 # Briefs clients
│   ├── phases/                 # Livrables par phase
│   ├── agents/                 # Config agents
│   └── templates/              # Templates reutilisables
└── docs/                       # Documentation
```

---

## Execution Parallele

Pour chaque creation de site, lancer en parallele quand possible :

```
PARALLELE 1 (Phase 1) :
  ├── Agent planner    → Strategie + sitemap
  └── Agent architect  → Choix techniques + design direction

PARALLELE 2 (Phase 3-4) :
  ├── Agent architect  → Design tokens + composants
  └── Agent code-reviewer → Setup projet + structure HTML

PARALLELE 3 (Phase 5-6) :
  ├── Agent doc-updater     → Contenu + SEO
  ├── Agent tdd-guide       → Tests performance
  └── Agent security-reviewer → Audit securite
```

---

## Commandes Rapides

| Commande | Action |
|----------|--------|
| `creation-site` | Lance le brief client complet |
| `status` | Affiche l'avancement du projet en cours |
| `phase [N]` | Execute la phase N du pipeline |
| `preview` | Lance le serveur de dev et ouvre le navigateur |
| `deploy` | Lance le deploiement production |
| `audit` | Lance un audit complet (perf + SEO + securite) |
| `export` | Exporte le projet pour livraison client |
