"""
VitrinePro Studio — Guide d'utilisation du Workflow
Genere un PDF professionnel avec reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --- Couleurs ---
PRIMARY = HexColor("#1e3a5f")
PRIMARY_LIGHT = HexColor("#2563eb")
ACCENT = HexColor("#3b82f6")
BG_LIGHT = HexColor("#f1f5f9")
BG_DARK = HexColor("#0f172a")
TEXT_DARK = HexColor("#1e293b")
TEXT_LIGHT = HexColor("#64748b")
SUCCESS = HexColor("#16a34a")
WARNING = HexColor("#f59e0b")
DANGER = HexColor("#dc2626")
WHITE = white
BLACK = black


class ColorBlock(Flowable):
    """Bloc colore pleine largeur pour les titres de section."""
    def __init__(self, text, width, bg_color=PRIMARY, text_color=WHITE, height=14*mm):
        Flowable.__init__(self)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.block_width = width
        self.block_height = height

    def wrap(self, availWidth, availHeight):
        return self.block_width, self.block_height

    def draw(self):
        self.canv.setFillColor(self.bg_color)
        self.canv.roundRect(0, 0, self.block_width, self.block_height, 3*mm, fill=1, stroke=0)
        self.canv.setFillColor(self.text_color)
        self.canv.setFont("Helvetica-Bold", 13)
        self.canv.drawString(5*mm, 4*mm, self.text)


class PhaseBlock(Flowable):
    """Bloc numerote pour les phases."""
    def __init__(self, number, title, width):
        Flowable.__init__(self)
        self.number = number
        self.title = title
        self.block_width = width
        self.block_height = 10*mm

    def wrap(self, availWidth, availHeight):
        return self.block_width, self.block_height

    def draw(self):
        # Cercle avec numero
        self.canv.setFillColor(ACCENT)
        self.canv.circle(6*mm, 5*mm, 5*mm, fill=1, stroke=0)
        self.canv.setFillColor(WHITE)
        self.canv.setFont("Helvetica-Bold", 12)
        self.canv.drawCentredString(6*mm, 3*mm, str(self.number))
        # Titre
        self.canv.setFillColor(PRIMARY)
        self.canv.setFont("Helvetica-Bold", 12)
        self.canv.drawString(14*mm, 3*mm, self.title)


def build_pdf():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "docs", "Guide-VitrinePro-Studio.pdf")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    usable_width = A4[0] - 40*mm
    styles = getSampleStyleSheet()

    # --- Styles personnalises ---
    s_title = ParagraphStyle("CoverTitle", parent=styles["Title"],
                             fontSize=28, leading=34, textColor=PRIMARY,
                             alignment=TA_CENTER, spaceAfter=5*mm)
    s_subtitle = ParagraphStyle("CoverSubtitle", parent=styles["Normal"],
                                fontSize=14, leading=18, textColor=TEXT_LIGHT,
                                alignment=TA_CENTER, spaceAfter=3*mm)
    s_h1 = ParagraphStyle("H1", parent=styles["Heading1"],
                           fontSize=18, leading=22, textColor=PRIMARY,
                           spaceBefore=8*mm, spaceAfter=4*mm)
    s_h2 = ParagraphStyle("H2", parent=styles["Heading2"],
                           fontSize=14, leading=17, textColor=PRIMARY_LIGHT,
                           spaceBefore=6*mm, spaceAfter=3*mm)
    s_h3 = ParagraphStyle("H3", parent=styles["Heading3"],
                           fontSize=12, leading=15, textColor=TEXT_DARK,
                           spaceBefore=4*mm, spaceAfter=2*mm)
    s_body = ParagraphStyle("Body", parent=styles["Normal"],
                             fontSize=10, leading=14, textColor=TEXT_DARK,
                             alignment=TA_JUSTIFY, spaceAfter=2*mm)
    s_bullet = ParagraphStyle("Bullet", parent=s_body,
                               leftIndent=8*mm, bulletIndent=3*mm,
                               spaceBefore=1*mm, spaceAfter=1*mm)
    s_code = ParagraphStyle("Code", parent=styles["Code"],
                             fontSize=9, leading=12, textColor=HexColor("#334155"),
                             backColor=BG_LIGHT, borderPadding=3*mm,
                             leftIndent=5*mm, spaceAfter=3*mm)
    s_note = ParagraphStyle("Note", parent=s_body,
                             fontSize=9, leading=12, textColor=TEXT_LIGHT,
                             leftIndent=5*mm, borderColor=ACCENT,
                             borderWidth=1, borderPadding=3*mm)
    s_center = ParagraphStyle("Center", parent=s_body, alignment=TA_CENTER)

    story = []

    # =====================================================================
    # PAGE DE COUVERTURE
    # =====================================================================
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("VitrinePro Studio", s_title))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Guide Complet du Workflow", ParagraphStyle(
        "Sub", parent=s_subtitle, fontSize=18, textColor=ACCENT)))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="60%", thickness=2, color=ACCENT,
                              spaceAfter=8*mm, spaceBefore=0, hAlign="CENTER"))
    story.append(Paragraph(
        "Systeme professionnel de creation de sites vitrines<br/>"
        "Pipeline en 8 phases — 6 agents specialises — 6 commandes",
        ParagraphStyle("CoverDesc", parent=s_body, alignment=TA_CENTER,
                       fontSize=12, leading=16, textColor=TEXT_LIGHT)))
    story.append(Spacer(1, 30*mm))

    # Table des specs rapides
    cover_data = [
        ["Agents", "6 agents specialises (Director, UX, UI, Dev, SEO, QA)"],
        ["Skills", "6 commandes (/creation-site, /phase, /audit, /preview, /deploy, /export)"],
        ["Pipeline", "8 phases de production sequentielles"],
        ["Stack", "HTML5 + CSS3 + Vanilla JS (zero dependances)"],
        ["Qualite", "Lighthouse > 90 — WCAG 2.1 AA — SEO optimise"],
    ]
    cover_table = Table(cover_data, colWidths=[35*mm, usable_width - 35*mm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BG_LIGHT),
        ("TEXTCOLOR", (0, 0), (0, -1), PRIMARY),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4*mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4*mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3*mm),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("Version 1.0 — Avril 2026", s_center))
    story.append(PageBreak())

    # =====================================================================
    # TABLE DES MATIERES
    # =====================================================================
    story.append(ColorBlock("TABLE DES MATIERES", usable_width))
    story.append(Spacer(1, 5*mm))

    toc_items = [
        ("1.", "Presentation Generale", "Comment fonctionne VitrinePro Studio"),
        ("2.", "Demarrage Rapide", "Lancer votre premier site en 5 minutes"),
        ("3.", "Le Brief Client", "Les 9 questions du questionnaire interactif"),
        ("4.", "Pipeline de Production", "Les 8 phases detaillees"),
        ("5.", "Les Agents", "6 agents specialises et leurs roles"),
        ("6.", "Les Commandes (Skills)", "6 commandes pour piloter le workflow"),
        ("7.", "Catalogue de Styles", "8 directions artistiques predefinies"),
        ("8.", "Catalogue de Layouts", "Modeles de mise en page"),
        ("9.", "Standards de Qualite", "Performance, accessibilite, SEO, securite"),
        ("10.", "Structure des Fichiers", "Organisation du projet"),
        ("11.", "FAQ & Depannage", "Questions frequentes"),
    ]
    toc_data = [[n, Paragraph(f"<b>{t}</b><br/><font size=8 color='#64748b'>{d}</font>",
                               s_body)] for n, t, d in toc_items]
    toc_table = Table(toc_data, colWidths=[10*mm, usable_width - 10*mm])
    toc_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (0, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2*mm),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, HexColor("#e2e8f0")),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =====================================================================
    # 1. PRESENTATION GENERALE
    # =====================================================================
    story.append(ColorBlock("1. PRESENTATION GENERALE", usable_width))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "<b>VitrinePro Studio</b> est un systeme de workflow professionnel qui transforme "
        "la creation de sites vitrines en un processus structure, reproductible et de haute qualite. "
        "Il fonctionne comme une agence digitale complete avec des agents specialises pour chaque metier.",
        s_body))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("<b>Principe de fonctionnement :</b>", s_body))
    story.append(Paragraph(
        "1. Vous lancez la commande <b>/creation-site</b><br/>"
        "2. Le systeme vous pose 9 questions pour comprendre vos besoins<br/>"
        "3. Un brief client est genere et valide<br/>"
        "4. Le pipeline de 8 phases se lance automatiquement<br/>"
        "5. Chaque phase est executee par un agent specialise<br/>"
        "6. Le site est livre, teste et pret a deployer",
        s_body))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("<b>Organigramme de l'agence :</b>", s_body))
    org_data = [
        ["DIRECTION", "PRODUCTION", "QUALITE"],
        ["Directeur de Projet\n(vitrine-director)",
         "UX Designer\n(vitrine-ux-designer)",
         "QA Engineer\n(vitrine-qa-engineer)"],
        ["Directeur Creatif\n(vitrine-ui-designer)",
         "Dev Frontend\n(vitrine-frontend-dev)",
         "Expert Securite\n(security-reviewer)"],
        ["Directeur Technique\n(code-reviewer)",
         "Redacteur + SEO\n(vitrine-seo-writer)",
         "Code Quality\n(refactor-cleaner)"],
    ]
    org_table = Table(org_data, colWidths=[usable_width/3]*3)
    org_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3*mm),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ("BACKGROUND", (0, 1), (-1, -1), BG_LIGHT),
    ]))
    story.append(org_table)
    story.append(PageBreak())

    # =====================================================================
    # 2. DEMARRAGE RAPIDE
    # =====================================================================
    story.append(ColorBlock("2. DEMARRAGE RAPIDE", usable_width))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "Pour creer votre premier site vitrine, suivez ces etapes :", s_body))
    story.append(Spacer(1, 3*mm))

    quick_steps = [
        ("Ouvrir le projet", "Ouvrez Claude Code dans le dossier du projet vitrine"),
        ("Lancer la creation", "Tapez /creation-site dans le chat"),
        ("Repondre au brief", "Repondez aux 9 questions posees par le systeme"),
        ("Valider le brief", "Verifiez le resume et confirmez"),
        ("Laisser le pipeline tourner", "Les 8 phases s'executent automatiquement"),
        ("Previsualiser", "Tapez /preview pour voir le resultat"),
        ("Ajuster si besoin", "Demandez des modifications specifiques"),
        ("Deployer", "Tapez /deploy pour mettre en ligne"),
    ]

    for i, (title, desc) in enumerate(quick_steps, 1):
        story.append(PhaseBlock(i, title, usable_width))
        story.append(Paragraph(desc, ParagraphStyle("StepDesc", parent=s_body,
                                                     leftIndent=14*mm, spaceBefore=0)))
        story.append(Spacer(1, 2*mm))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "<b>Astuce :</b> Vous pouvez aussi executer une phase specifique avec "
        "<b>/phase N</b> (ex: /phase 3 pour le design UI uniquement).",
        s_note))
    story.append(PageBreak())

    # =====================================================================
    # 3. LE BRIEF CLIENT
    # =====================================================================
    story.append(ColorBlock("3. LE BRIEF CLIENT — LES 9 QUESTIONS", usable_width))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "Le brief client est la fondation de tout projet. Il est declenche automatiquement "
        "par la commande <b>/creation-site</b>. Voici les 9 questions posees :", s_body))
    story.append(Spacer(1, 3*mm))

    questions = [
        ("Q1 — Domaine d'activite",
         "Restaurant, Avocat, Medecin, Artisan, Immobilier, Coach, Photographe, "
         "Architecte, Coiffure, Auto-ecole, Consultant, ou Autre",
         "Determine le ton, les couleurs et la structure recommandes"),
        ("Q2 — Nom du projet",
         "Nom commercial + slogan si existant",
         "Utilise dans le header, le SEO et les meta tags"),
        ("Q3 — Style visuel",
         "Minimaliste, Luxe, Moderne, Chaleureux, Corporate, Creatif, Eco, Bold",
         "Selectionne la palette, les fonts et les composants du catalogue"),
        ("Q4 — Couleurs",
         "Couleur principale souhaitee ou 'proposer selon le domaine'",
         "Genere la palette complete de 10 couleurs CSS"),
        ("Q5 — Pages souhaitees",
         "Accueil, A propos, Services, Contact, Portfolio, Tarifs, Blog, etc.",
         "Definit la structure du sitemap et les fichiers HTML a creer"),
        ("Q6 — Fonctionnalites",
         "Formulaire, Maps, Galerie, Reservation, Chat, Newsletter, etc.",
         "Determine les composants JS et les services tiers a integrer"),
        ("Q7 — Contenu",
         "Fourni par le client, a generer, ou a fournir plus tard",
         "Si 'generer', le redacteur IA cree du contenu de demonstration"),
        ("Q8 — Inspiration",
         "URLs de sites que le client aime",
         "Analyse pour extraire les patterns visuels et structurels"),
        ("Q9 — Deadline",
         "Standard (complet), Urgent (essentiel d'abord), Express (MVP)",
         "Ajuste la profondeur de chaque phase du pipeline"),
    ]

    for q_title, q_options, q_impact in questions:
        story.append(Paragraph(f"<b>{q_title}</b>", s_h3))
        story.append(Paragraph(f"<i>Options :</i> {q_options}", s_bullet))
        story.append(Paragraph(f"<i>Impact :</i> {q_impact}", s_bullet))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "Apres les 9 reponses, un fichier brief est genere dans "
        "<b>.workflow/briefs/[nom-projet].md</b> et presente pour validation.",
        s_note))
    story.append(PageBreak())

    # =====================================================================
    # 4. PIPELINE DE PRODUCTION
    # =====================================================================
    story.append(ColorBlock("4. PIPELINE DE PRODUCTION — 8 PHASES", usable_width))
    story.append(Spacer(1, 5*mm))

    phases = [
        ("Phase 1 : STRATEGIE & RECHERCHE",
         "planner + architect",
         ["Analyse du domaine et de la concurrence",
          "Definition de la strategie SEO initiale",
          "Architecture de l'information (sitemap)",
          "Choix technologiques (stack)",
          "Planning de production"],
         "01-strategie.md"),
        ("Phase 2 : UX DESIGN",
         "vitrine-ux-designer",
         ["Wireframes de chaque page (structure ASCII)",
          "Parcours utilisateur (visitor -> conversion)",
          "Hierarchie de contenu par page",
          "Points de conversion (CTA)",
          "Strategie responsive (breakpoints)"],
         "02-ux-design.md"),
        ("Phase 3 : UI DESIGN & DIRECTION ARTISTIQUE",
         "vitrine-ui-designer",
         ["Palette de couleurs definitive (10 variables CSS)",
          "Typographies (heading + body)",
          "Systeme de composants (boutons, cards, forms)",
          "Animations et micro-interactions",
          "Generation de assets/css/variables.css"],
         "03-ui-design.md"),
        ("Phase 4 : DEVELOPPEMENT FRONTEND",
         "vitrine-frontend-dev",
         ["Setup projet (HTML5 + CSS3 + Vanilla JS)",
          "Integration du design system",
          "Developpement page par page",
          "Responsive mobile-first",
          "Optimisation des assets (images, fonts)"],
         "04-developpement.md"),
        ("Phase 5 : CONTENU & SEO",
         "vitrine-seo-writer",
         ["Redaction ou integration du contenu",
          "Meta tags (title, description) par page",
          "Schema.org JSON-LD (LocalBusiness, etc.)",
          "Open Graph + Twitter Cards",
          "Sitemap XML + robots.txt"],
         "05-contenu-seo.md"),
        ("Phase 6 : QA & TESTING",
         "vitrine-qa-engineer",
         ["Tests cross-browser (Chrome, Firefox, Safari, Edge)",
          "Tests responsive (6 breakpoints)",
          "Audit Lighthouse (perf > 90, a11y > 90, SEO > 90)",
          "Accessibilite WCAG 2.1 AA",
          "Audit securite (headers, HTTPS, formulaires)"],
         "06-qa-testing.md"),
        ("Phase 7 : DEPLOIEMENT",
         "build-error-resolver",
         ["Build de production optimise",
          "Configuration hebergement (Vercel/Netlify/VPS)",
          "DNS + SSL + redirections",
          "Headers de securite",
          "Verification post-deploiement"],
         "07-deploiement.md"),
        ("Phase 8 : POST-LANCEMENT",
         "doc-updater",
         ["Google Analytics + Search Console",
          "Documentation client (GUIDE-CLIENT.md)",
          "Documentation technique (TECHNIQUE.md)",
          "Plan de maintenance",
          "Rapport de performance initial"],
         "08-post-lancement.md"),
    ]

    for i, (title, agent, tasks, file) in enumerate(phases, 1):
        story.append(PhaseBlock(i, title, usable_width))
        story.append(Paragraph(f"<i>Agent : {agent}</i> | <i>Fichier : .workflow/phases/{file}</i>",
                               ParagraphStyle("PhaseAgent", parent=s_body,
                                              leftIndent=14*mm, fontSize=9,
                                              textColor=TEXT_LIGHT, spaceBefore=1*mm)))
        for task in tasks:
            story.append(Paragraph(f"\u2022 {task}",
                                   ParagraphStyle("PhaseTask", parent=s_bullet,
                                                  leftIndent=16*mm, bulletIndent=14*mm,
                                                  spaceBefore=0.5*mm, spaceAfter=0.5*mm)))
        story.append(Spacer(1, 3*mm))

    story.append(PageBreak())

    # =====================================================================
    # 5. LES AGENTS
    # =====================================================================
    story.append(ColorBlock("5. LES AGENTS SPECIALISES", usable_width))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "Chaque agent est un expert dans son domaine. Ils sont definis dans "
        "<b>~/.claude/agents/</b> et s'activent automatiquement selon la phase.", s_body))
    story.append(Spacer(1, 3*mm))

    agents_data = [
        ["Agent", "Role", "Modele", "Phases"],
        ["vitrine-director", "Chef de projet, brief client, coordination", "Opus", "Toutes"],
        ["vitrine-ux-designer", "Wireframes, parcours utilisateur, IA", "Sonnet", "2"],
        ["vitrine-ui-designer", "Palette, typo, composants, design tokens", "Opus", "3"],
        ["vitrine-frontend-dev", "HTML/CSS/JS, responsive, animations", "Sonnet", "4"],
        ["vitrine-seo-writer", "Contenu, copywriting, SEO on-page", "Sonnet", "5"],
        ["vitrine-qa-engineer", "Tests, Lighthouse, a11y, securite", "Sonnet", "6"],
    ]
    agents_table = Table(agents_data, colWidths=[32*mm, 55*mm, 18*mm, usable_width-105*mm])
    agents_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5*mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 3*mm),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, BG_LIGHT]),
    ]))
    story.append(agents_table)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        "<b>Agents existants aussi utilises :</b><br/>"
        "\u2022 <b>planner</b> — Planification strategique (Phase 1)<br/>"
        "\u2022 <b>architect</b> — Decisions d'architecture (Phase 1)<br/>"
        "\u2022 <b>code-reviewer</b> — Revue de code (Phase 4)<br/>"
        "\u2022 <b>security-reviewer</b> — Audit securite (Phase 6)<br/>"
        "\u2022 <b>build-error-resolver</b> — Resolution d'erreurs build (Phase 7)<br/>"
        "\u2022 <b>refactor-cleaner</b> — Nettoyage de code (optimisation)<br/>"
        "\u2022 <b>doc-updater</b> — Documentation (Phase 8)",
        s_body))
    story.append(PageBreak())

    # =====================================================================
    # 6. LES COMMANDES (SKILLS)
    # =====================================================================
    story.append(ColorBlock("6. LES COMMANDES (SKILLS)", usable_width))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "Les commandes sont des raccourcis que vous tapez directement dans Claude Code. "
        "Elles declenchent des workflows specifiques.", s_body))
    story.append(Spacer(1, 3*mm))

    cmds = [
        ["/creation-site", "Lance le brief client complet puis le pipeline 8 phases.\n"
         "C'est LA commande principale pour creer un site."],
        ["/phase N", "Execute une phase specifique (1 a 8).\n"
         "Exemple : /phase 3 lance uniquement le UI Design."],
        ["/audit", "Audit complet multi-dimensions :\n"
         "Performance, Accessibilite, SEO, Securite, Code Quality."],
        ["/preview", "Lance un serveur local (port 3000) et ouvre le site\n"
         "dans le navigateur pour verification visuelle."],
        ["/deploy", "Deploie en production.\n"
         "Supporte GitHub Pages, Vercel, et Netlify."],
        ["/export", "Prepare le package de livraison client.\n"
         "Genere documentation + archive ZIP."],
    ]

    for cmd, desc in cmds:
        cmd_data = [[Paragraph(f"<b><font color='#2563eb'>{cmd}</font></b>", s_body),
                      Paragraph(desc.replace("\n", "<br/>"), s_body)]]
        cmd_table = Table(cmd_data, colWidths=[30*mm, usable_width - 30*mm])
        cmd_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), BG_LIGHT),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3*mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3*mm),
            ("LEFTPADDING", (0, 0), (-1, -1), 3*mm),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
        ]))
        story.append(cmd_table)
        story.append(Spacer(1, 2*mm))

    story.append(PageBreak())

    # =====================================================================
    # 7. CATALOGUE DE STYLES
    # =====================================================================
    story.append(ColorBlock("7. CATALOGUE DE STYLES", usable_width))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "8 directions artistiques predefinies, chacune avec sa palette, "
        "ses typographies et ses caracteristiques visuelles.", s_body))
    story.append(Spacer(1, 3*mm))

    style_items = [
        ("MINIMALISTE", "#1a1a1a", "Inter", "Epure, espace blanc, essentiel",
         "Architecte, Consultant, Photographe"),
        ("LUXE / PREMIUM", "#1c1c1c", "Playfair Display + Lato", "Fond sombre, accents dores, elegance",
         "Immobilier, Bijouterie, Hotel, Spa"),
        ("MODERNE / TECH", "#6366f1", "Plus Jakarta Sans + Inter", "Gradients, coins arrondis, ombres douces",
         "Startup, SaaS, Agence digitale"),
        ("CHALEUREUX / ARTISANAL", "#8b5e3c", "DM Serif Display + Source Sans", "Tons chauds, textures, authenticite",
         "Boulangerie, Restaurant, Artisan"),
        ("CORPORATE / SERIEUX", "#1e3a5f", "Merriweather + Source Sans", "Bleu marine, structure, autorite",
         "Avocat, Cabinet comptable, Assurance"),
        ("CREATIF / ARTISTIQUE", "#7c3aed", "Space Grotesk + DM Sans", "Couleurs vives, layouts asymetriques",
         "Graphiste, Agence creative, Galerie"),
        ("ECO / NATURE", "#166534", "Libre Baskerville + Nunito", "Verts, formes organiques, apaisant",
         "Bio, Yoga, Naturopathe, Jardinier"),
        ("BOLD / IMPACT", "#dc2626", "Montserrat + Open Sans", "Couleurs saturees, typo bold, energie",
         "Coach sportif, Auto-ecole, Evenementiel"),
    ]

    for name, color, fonts, desc, ideal in style_items:
        row = [[
            Paragraph(f"<b>{name}</b>", ParagraphStyle("StyleName", parent=s_body, fontSize=10)),
            Paragraph(f"<font size=8><i>Fonts :</i> {fonts}<br/>"
                      f"<i>Caracteristiques :</i> {desc}<br/>"
                      f"<i>Ideal pour :</i> {ideal}</font>", s_body),
        ]]
        st = Table(row, colWidths=[38*mm, usable_width - 38*mm])
        st.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), HexColor(color)),
            ("TEXTCOLOR", (0, 0), (0, 0), WHITE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2*mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2*mm),
            ("LEFTPADDING", (0, 0), (-1, -1), 3*mm),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
        ]))
        story.append(st)
        story.append(Spacer(1, 1.5*mm))

    story.append(PageBreak())

    # =====================================================================
    # 8. CATALOGUE DE LAYOUTS
    # =====================================================================
    story.append(ColorBlock("8. CATALOGUE DE LAYOUTS", usable_width))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>3 layouts de page d'accueil :</b>", s_h3))
    layouts = [
        ("Layout A — CLASSIQUE",
         "Hero + Confiance + Services (3 col) + A propos + Temoignages + CTA + Footer",
         "La plupart des domaines (avocat, medecin, coiffure, auto-ecole)"),
        ("Layout B — HERO FULL SCREEN",
         "Hero plein ecran + Intro + Services + Split image/texte + Slider + CTA + Footer",
         "Restaurant, Immobilier, Photographe, Architecte"),
        ("Layout C — STORYTELLING",
         "Hero anime + Probleme + Solution + Process + Preuves + CTA + Footer",
         "Coach, Artisan, Consultant (narration progressive)"),
    ]
    for name, structure, ideal in layouts:
        story.append(Paragraph(f"<b>{name}</b>", s_h3))
        story.append(Paragraph(f"<i>Structure :</i> {structure}", s_bullet))
        story.append(Paragraph(f"<i>Ideal pour :</i> {ideal}", s_bullet))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("<b>3 layouts de Hero section :</b>", s_h3))
    story.append(Paragraph("\u2022 <b>Hero Split (50/50)</b> — Texte a gauche, image a droite", s_bullet))
    story.append(Paragraph("\u2022 <b>Hero Centre</b> — Image de fond, texte centre, 2 CTA", s_bullet))
    story.append(Paragraph("\u2022 <b>Hero Asymetrique</b> — Grand titre a gauche, image decalee a droite", s_bullet))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("<b>2 layouts de Footer :</b>", s_h3))
    story.append(Paragraph("\u2022 <b>Footer Complet (4 colonnes)</b> — Logo + Liens + Services + Contact", s_bullet))
    story.append(Paragraph("\u2022 <b>Footer Simple (2 colonnes)</b> — Logo + Contact, mentions legales", s_bullet))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Le fichier complet avec les wireframes ASCII se trouve dans "
        "<b>.workflow/templates/layouts-catalogue.md</b>",
        s_note))
    story.append(PageBreak())

    # =====================================================================
    # 9. STANDARDS DE QUALITE
    # =====================================================================
    story.append(ColorBlock("9. STANDARDS DE QUALITE", usable_width))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>Performance (Lighthouse)</b>", s_h3))
    perf_data = [
        ["Metrique", "Objectif", "Importance"],
        ["Performance Score", "> 90", "CRITIQUE"],
        ["First Contentful Paint", "< 1.8s", "HAUTE"],
        ["Largest Contentful Paint", "< 2.5s", "CRITIQUE"],
        ["Cumulative Layout Shift", "< 0.1", "HAUTE"],
        ["Total Blocking Time", "< 200ms", "HAUTE"],
    ]
    perf_table = Table(perf_data, colWidths=[50*mm, 30*mm, usable_width-80*mm])
    perf_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2*mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 3*mm),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, BG_LIGHT]),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("<b>Accessibilite (WCAG 2.1 AA)</b>", s_h3))
    a11y_items = [
        "Contraste texte/fond minimum 4.5:1 (3:1 pour grands textes)",
        "Navigation complete au clavier (Tab, Enter, Escape)",
        "Focus visible sur tous les elements interactifs",
        "Images avec attributs alt descriptifs",
        "Formulaires avec labels associes aux inputs",
        "Hierarchie de headings logique (h1 > h2 > h3)",
        "Support de prefers-reduced-motion",
    ]
    for item in a11y_items:
        story.append(Paragraph(f"\u2713 {item}", s_bullet))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("<b>SEO Minimum</b>", s_h3))
    seo_items = [
        "Title + meta description uniques par page",
        "H1 unique par page avec mot-cle principal",
        "Schema.org JSON-LD (LocalBusiness si applicable)",
        "Open Graph + Twitter Cards",
        "Sitemap.xml + robots.txt",
        "URLs propres et descriptives",
        "Images avec attributs alt",
    ]
    for item in seo_items:
        story.append(Paragraph(f"\u2713 {item}", s_bullet))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("<b>Securite</b>", s_h3))
    sec_items = [
        "HTTPS obligatoire en production",
        "Headers securite (CSP, X-Frame-Options, X-Content-Type-Options)",
        "Formulaires avec protection CSRF + honeypot",
        "rel='noopener noreferrer' sur liens externes",
        "Pas de secrets dans le code source",
    ]
    for item in sec_items:
        story.append(Paragraph(f"\u2713 {item}", s_bullet))
    story.append(PageBreak())

    # =====================================================================
    # 10. STRUCTURE DES FICHIERS
    # =====================================================================
    story.append(ColorBlock("10. STRUCTURE DES FICHIERS", usable_width))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>Structure du projet :</b>", s_h3))
    tree = (
        "projet/<br/>"
        "\u251c\u2500\u2500 index.html&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Page d'accueil<br/>"
        "\u251c\u2500\u2500 about.html&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A propos<br/>"
        "\u251c\u2500\u2500 services.html&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp; Services<br/>"
        "\u251c\u2500\u2500 contact.html&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp; Contact<br/>"
        "\u251c\u2500\u2500 404.html&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Page d'erreur<br/>"
        "\u251c\u2500\u2500 sitemap.xml&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Plan du site<br/>"
        "\u251c\u2500\u2500 robots.txt&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Directives moteurs<br/>"
        "\u251c\u2500\u2500 assets/<br/>"
        "\u2502&nbsp;&nbsp; \u251c\u2500\u2500 css/<br/>"
        "\u2502&nbsp;&nbsp; \u2502&nbsp;&nbsp; \u251c\u2500\u2500 variables.css&nbsp;&nbsp;&nbsp; Design tokens<br/>"
        "\u2502&nbsp;&nbsp; \u2502&nbsp;&nbsp; \u251c\u2500\u2500 reset.css&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; CSS Reset<br/>"
        "\u2502&nbsp;&nbsp; \u2502&nbsp;&nbsp; \u251c\u2500\u2500 base.css&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Styles globaux<br/>"
        "\u2502&nbsp;&nbsp; \u2502&nbsp;&nbsp; \u251c\u2500\u2500 components.css&nbsp;&nbsp; Composants<br/>"
        "\u2502&nbsp;&nbsp; \u2502&nbsp;&nbsp; \u2514\u2500\u2500 layout.css&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Grille<br/>"
        "\u2502&nbsp;&nbsp; \u251c\u2500\u2500 js/<br/>"
        "\u2502&nbsp;&nbsp; \u2502&nbsp;&nbsp; \u251c\u2500\u2500 main.js&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Initialisation<br/>"
        "\u2502&nbsp;&nbsp; \u2502&nbsp;&nbsp; \u251c\u2500\u2500 navigation.js&nbsp;&nbsp;&nbsp; Menu mobile<br/>"
        "\u2502&nbsp;&nbsp; \u2502&nbsp;&nbsp; \u2514\u2500\u2500 animations.js&nbsp;&nbsp;&nbsp; Scroll reveal<br/>"
        "\u2502&nbsp;&nbsp; \u251c\u2500\u2500 images/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp; Visuels du site<br/>"
        "\u2502&nbsp;&nbsp; \u2514\u2500\u2500 fonts/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Polices locales<br/>"
        "\u251c\u2500\u2500 .workflow/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Fichiers du workflow<br/>"
        "\u2502&nbsp;&nbsp; \u251c\u2500\u2500 briefs/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp; Briefs clients<br/>"
        "\u2502&nbsp;&nbsp; \u251c\u2500\u2500 phases/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp; Livrables par phase<br/>"
        "\u2502&nbsp;&nbsp; \u251c\u2500\u2500 agents/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp; Documentation agents<br/>"
        "\u2502&nbsp;&nbsp; \u2514\u2500\u2500 templates/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp; Catalogues styles/layouts<br/>"
        "\u2514\u2500\u2500 docs/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Documentation finale"
    )
    story.append(Paragraph(tree, ParagraphStyle("Tree", parent=s_code, fontSize=8, leading=11)))
    story.append(PageBreak())

    # =====================================================================
    # 11. FAQ & DEPANNAGE
    # =====================================================================
    story.append(ColorBlock("11. FAQ & DEPANNAGE", usable_width))
    story.append(Spacer(1, 5*mm))

    faqs = [
        ("Comment lancer une creation de site ?",
         "Tapez <b>/creation-site</b> dans Claude Code. Le systeme vous posera 9 questions "
         "puis generera le site automatiquement."),
        ("Puis-je executer une seule phase ?",
         "Oui, utilisez <b>/phase N</b> (ex: /phase 4 pour le developpement). "
         "Assurez-vous que les phases precedentes sont completees."),
        ("Comment changer le style apres la creation ?",
         "Modifiez le fichier <b>assets/css/variables.css</b> avec les nouvelles couleurs "
         "et typographies. Consultez le catalogue de styles dans "
         "<b>.workflow/templates/styles-catalogue.md</b>."),
        ("Comment ajouter une nouvelle page ?",
         "Creez un nouveau fichier HTML en copiant la structure d'une page existante. "
         "Mettez a jour la navigation dans toutes les pages et le sitemap.xml."),
        ("Comment previsualiser le site ?",
         "Tapez <b>/preview</b> pour lancer un serveur local sur le port 3000."),
        ("Comment deployer ?",
         "Tapez <b>/deploy</b>. Le systeme supporte GitHub Pages (gratuit), "
         "Vercel (recommande) et Netlify."),
        ("Ou sont stockes les fichiers du workflow ?",
         "Dans le dossier <b>.workflow/</b> : briefs clients, checklists de phases, "
         "catalogues de styles et layouts."),
        ("Puis-je modifier les agents ?",
         "Oui, les agents sont dans <b>~/.claude/agents/vitrine-*.md</b>. "
         "Vous pouvez modifier leurs instructions, leur modele et leurs outils."),
        ("Puis-je modifier les skills ?",
         "Oui, les skills sont dans <b>~/.claude/skills/vitrine-*/SKILL.md</b>. "
         "Vous pouvez personnaliser les questions du brief ou les etapes du pipeline."),
        ("Le site utilise-t-il un framework ?",
         "Non, par defaut c'est du <b>HTML5 + CSS3 + Vanilla JS</b> pur — zero dependances, "
         "performances maximales. Pour des besoins avances, le pipeline peut utiliser "
         "Astro, Next.js ou Nuxt.js."),
    ]

    for question, answer in faqs:
        story.append(Paragraph(f"<b>{question}</b>", s_h3))
        story.append(Paragraph(answer, s_body))

    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "<b>VitrinePro Studio</b> — Systeme de creation de sites vitrines professionnels<br/>"
        "Version 1.0 — Avril 2026<br/>"
        "Propulse par Claude Code + Agents specialises",
        ParagraphStyle("Footer", parent=s_center, fontSize=9, textColor=TEXT_LIGHT)))

    # --- Build ---
    doc.build(story)
    print(f"PDF genere avec succes : {output_path}")


if __name__ == "__main__":
    build_pdf()
