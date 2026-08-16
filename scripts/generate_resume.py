"""Generate the downloadable, educator-focused PDF resume."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public" / "cv" / "Resume_Pardeep_Kumar_SD.pdf"

INK = colors.HexColor("#17211F")
MUTED = colors.HexColor("#53615E")
TEAL = colors.HexColor("#006D68")
PALE_TEAL = colors.HexColor("#EAF4F1")
RULE = colors.HexColor("#B9CAC5")
PAPER = colors.HexColor("#FFFEFB")


def register_fonts():
    """Use readable system fonts when present, with PDF-safe fallbacks."""
    font_dir = Path("C:/Windows/Fonts")
    candidates = {
        "ResumeSans": font_dir / "arial.ttf",
        "ResumeSans-Bold": font_dir / "arialbd.ttf",
        "ResumeSerif": font_dir / "cambria.ttc",
        "ResumeSerif-Bold": font_dir / "cambriab.ttf",
    }
    fallbacks = {
        "ResumeSans": "Helvetica",
        "ResumeSans-Bold": "Helvetica-Bold",
        "ResumeSerif": "Times-Roman",
        "ResumeSerif-Bold": "Times-Bold",
    }

    names = {}
    for name, path in candidates.items():
        if path.exists() and path.suffix.lower() == ".ttf":
            pdfmetrics.registerFont(TTFont(name, str(path)))
            names[name] = name
        else:
            names[name] = fallbacks[name]
    return names


FONTS = register_fonts()
styles = getSampleStyleSheet()

NAME = ParagraphStyle(
    "Name",
    parent=styles["Normal"],
    fontName=FONTS["ResumeSerif-Bold"],
    fontSize=25,
    leading=27,
    textColor=INK,
    spaceAfter=1.5 * mm,
)
ROLE = ParagraphStyle(
    "Role",
    parent=styles["Normal"],
    fontName=FONTS["ResumeSans-Bold"],
    fontSize=9.1,
    leading=11,
    tracking=0.35,
    textColor=TEAL,
    spaceAfter=2.5 * mm,
)
CONTACT = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName=FONTS["ResumeSans"],
    fontSize=7.7,
    leading=10.2,
    textColor=MUTED,
    spaceAfter=4 * mm,
)
SECTION = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontName=FONTS["ResumeSans-Bold"],
    fontSize=9.3,
    leading=11,
    tracking=0.75,
    textTransform="uppercase",
    textColor=TEAL,
    spaceBefore=3.5 * mm,
    spaceAfter=1.7 * mm,
    keepWithNext=True,
)
BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName=FONTS["ResumeSans"],
    fontSize=8.1,
    leading=11.1,
    textColor=INK,
    spaceAfter=1.9 * mm,
)
SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=7.5,
    leading=10,
    spaceAfter=1.2 * mm,
)
BULLET = ParagraphStyle(
    "Bullet",
    parent=BODY,
    leftIndent=3.4 * mm,
    firstLineIndent=-2.5 * mm,
    bulletIndent=0,
    spaceAfter=0.9 * mm,
)
ENTRY_TITLE = ParagraphStyle(
    "EntryTitle",
    parent=BODY,
    fontName=FONTS["ResumeSans-Bold"],
    fontSize=8.3,
    leading=10.5,
    spaceAfter=0,
)
ENTRY_META = ParagraphStyle(
    "EntryMeta",
    parent=SMALL,
    textColor=MUTED,
    spaceAfter=1.1 * mm,
)
DATE = ParagraphStyle(
    "Date",
    parent=SMALL,
    fontName=FONTS["ResumeSans-Bold"],
    alignment=TA_RIGHT,
    textColor=TEAL,
)
BOX_HEADING = ParagraphStyle(
    "BoxHeading",
    parent=SECTION,
    spaceBefore=0,
    spaceAfter=1.5 * mm,
)
BOX_BODY = ParagraphStyle(
    "BoxBody",
    parent=BODY,
    fontSize=7.9,
    leading=10.7,
    spaceAfter=1.4 * mm,
)
FOOTER = ParagraphStyle(
    "Footer",
    parent=SMALL,
    fontSize=6.8,
    alignment=TA_RIGHT,
    textColor=MUTED,
)


def p(text, style=BODY):
    return Paragraph(text, style)


def bullet(text, style=BULLET):
    return Paragraph(f"- {text}", style)


def section(title):
    return Paragraph(title, SECTION)


def entry(title, organisation, dates, bullets):
    heading = Table(
        [[p(title, ENTRY_TITLE), p(dates, DATE)]],
        colWidths=[139 * mm, 33 * mm],
        hAlign="LEFT",
    )
    heading.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    parts = [heading, p(organisation, ENTRY_META)]
    parts.extend(bullet(item) for item in bullets)
    parts.append(Spacer(1, 1.1 * mm))
    return KeepTogether(parts)


def education_entry(degree, institution, dates, detail):
    heading = Table(
        [[p(degree, ENTRY_TITLE), p(dates, DATE)]],
        colWidths=[139 * mm, 33 * mm],
    )
    heading.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return KeepTogether(
        [heading, p(institution, ENTRY_META), p(detail, SMALL), Spacer(1, 1.5 * mm)]
    )


def teaching_box():
    content = [
        p("Teaching direction", BOX_HEADING),
        p(
            "I am preparing for a deliberate move toward high-school education. I want to help students approach mathematics and physics through careful questions, physical intuition, visual explanation, and small computational investigations.",
            BOX_BODY,
        ),
        bullet("Interested in high-school mathematics, physics, computational thinking, and science outreach.", BOX_BODY),
        bullet("Able to connect classroom ideas to real examples from fluids, thermodynamics, electromagnetics, aerospace, and engineering.", BOX_BODY),
        bullet("Committed to treating questions and mistakes as useful parts of learning, while helping students learn how to test an argument.", BOX_BODY),
    ]
    box = Table([[content]], colWidths=[172 * mm])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
                ("BOX", (0, 0), (-1, -1), 0.55, RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm),
            ]
        )
    )
    return box


def page_decor(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.rect(0, A4[1] - 4 * mm, A4[0], 4 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.45)
    canvas.line(19 * mm, 11 * mm, A4[0] - 19 * mm, 11 * mm)
    footer = Paragraph(
        f"Pardeep Kumar  |  Curriculum Vitae  |  {doc.page}",
        FOOTER,
    )
    footer.wrapOn(canvas, 172 * mm, 5 * mm)
    footer.drawOn(canvas, 19 * mm, 6 * mm)
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=19 * mm,
        rightMargin=19 * mm,
        topMargin=13 * mm,
        bottomMargin=15 * mm,
        title="Pardeep Kumar - Scientific Computing Researcher and Aspiring Educator",
        author="Pardeep Kumar",
        subject="Curriculum vitae",
        keywords="scientific computing, numerical methods, education, teaching, mathematics, physics",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates(PageTemplate(id="resume", frames=[frame], onPage=page_decor))

    story = [
        p("Pardeep Kumar", NAME),
        p("SCIENTIFIC COMPUTING RESEARCHER  |  NUMERICAL METHODS  |  ASPIRING EDUCATOR", ROLE),
        p(
            'Amsterdam, the Netherlands  |  +31 6 1311 9813  |  '
            '<link href="mailto:pardeep.iitb@gmail.com" color="#006D68">pardeep.iitb@gmail.com</link>  |  '
            '<link href="https://pkpardeepkumar30.github.io/" color="#006D68">pkpardeepkumar30.github.io</link><br/>'
            '<link href="https://www.linkedin.com/in/pkpardeepkumar30/" color="#006D68">LinkedIn</link>  |  '
            '<link href="https://scholar.google.com/citations?hl=en&amp;user=th4w0rYAAAAJ" color="#006D68">Google Scholar</link>',
            CONTACT,
        ),
        section("Profile"),
        p(
            "Scientific computing researcher with a submitted doctoral thesis from Delft University of Technology and more than ten years of experience in numerical modelling, simulation software, and computational problem-solving. My research at CWI Amsterdam concerns robust numerical methods for multiphase thermodynamics and CO2-rich transport.",
        ),
        p(
            "I am now exploring a serious transition toward high-school education. Teaching brings together the parts of research I value most: asking careful questions, making difficult ideas understandable, and helping someone gain the confidence to reason independently. I would bring broad examples, patient explanation, and an honest learning mindset to mathematics, physics, and computing education.",
        ),
        teaching_box(),
        section("Education"),
        education_entry(
            "PhD in Mechanical Engineering",
            "Delft University of Technology | Research conducted at CWI Amsterdam",
            "2022-2026",
            "Thesis submitted; defence planned for January 2027. Research focus: numerical methods for transient multiphase flow of multicomponent mixtures, with industrial collaboration from Shell Projects &amp; Technology.",
        ),
        education_entry(
            "MSc in Aerospace Engineering",
            "Indian Institute of Technology Bombay, India",
            "2012-2014",
            "Research focus: finite-volume time-domain methods for electromagnetic propagation and scattering.",
        ),
        section("Doctoral research and scientific contribution"),
        bullet("Reformulated constrained phase-equilibrium calculations in a more efficient thermodynamic variable space."),
        bullet("Coupled phase-stability and equilibrium calculations to finite-volume solvers for CO2-rich tank and pipeline transport."),
        bullet("Developed thermodynamically consistent temperature-evolution models for multiphase flow."),
        bullet("Investigated exact and approximate Riemann problems for real-fluid mixtures."),
        bullet("Created Julia and Python research software supported by systematic validation and reproducibility workflows."),
        section("Transferable strengths for education"),
        Table(
            [
                [
                    p("<b>Clear explanation</b><br/>Used to moving between mathematics, physical meaning, algorithms, plots, and plain-language interpretation.", SMALL),
                    p("<b>Interdisciplinary perspective</b><br/>Examples drawn from aerospace, energy, fluids, electromagnetics, semiconductors, finance, and computing.", SMALL),
                ],
                [
                    p("<b>Evidence and verification</b><br/>A research habit of checking units, assumptions, limiting cases, numerical results, and alternative explanations.", SMALL),
                    p("<b>Computational demonstrations</b><br/>Able to create small programs and visual models that let students investigate a mathematical or physical question.", SMALL),
                ],
            ],
            colWidths=[84 * mm, 84 * mm],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOX", (0, 0), (-1, -1), 0.45, RULE),
                    ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2.4 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5 * mm),
                ]
            ),
        ),
        PageBreak(),
        p("Pardeep Kumar", NAME),
        p("SCIENTIFIC COMPUTING, ENGINEERING EXPERIENCE, AND SELECTED OUTPUT", ROLE),
        section("Scientific computing strengths"),
    ]

    strengths = Table(
        [
            [
                p("<b>Numerical methods</b><br/>Finite-volume and finite-difference methods, Riemann solvers, nonlinear equations, constrained optimisation, automatic differentiation, and numerical linear algebra.", SMALL),
                p("<b>Computational physics</b><br/>Multiphase flow, real-fluid thermodynamics, CFD, electromagnetics, wave propagation, and numerical relativity.", SMALL),
            ],
            [
                p("<b>Scientific programming</b><br/>C++, Julia, Python, C#, F#, Java, MATLAB, CUDA, MPI, multithreading, and performance-oriented computation.", SMALL),
                p("<b>Research software practice</b><br/>Modular architecture, interoperability, testing, validation, version control, visualisation, and reproducible computation.", SMALL),
            ],
        ],
        colWidths=[84 * mm, 84 * mm],
        hAlign="LEFT",
    )
    strengths.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOX", (0, 0), (-1, -1), 0.45, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5 * mm),
            ]
        )
    )
    story.extend(
        [
            strengths,
            section("Professional experience"),
            entry(
                "PhD Researcher in Scientific Computing",
                "Centrum Wiskunde &amp; Informatica (CWI), Amsterdam",
                "Aug 2022-present",
                [
                    "Developed numerical formulations and software for multicomponent, multiphase thermodynamics and transient flow.",
                    "Connected mathematical analysis, physical modelling, algorithm design, implementation, and validation in interdisciplinary research.",
                ],
            ),
            entry(
                "Software Engineer",
                "ASM International, Almere",
                "Feb-Aug 2022",
                [
                    "Enhanced and refactored a Java-based simulator for semiconductor thin-film deposition equipment.",
                ],
            ),
            entry(
                "Software Engineer",
                "Shell, Amsterdam",
                "Jun 2019-Dec 2021",
                [
                    "Migrated numerical workflows from Python to C++ and CUDA, reducing a representative runtime from about 30 minutes to 15 seconds.",
                    "Developed concurrent infrastructure, interoperability layers, and visualisation for process and pipeline simulation software.",
                ],
            ),
            entry(
                "Earlier engineering roles",
                "Aakraya Research, KLA-Tencor, Altair, and Fluidyn",
                "Jul 2014-Apr 2019",
                [
                    "Worked on trading infrastructure, semiconductor simulation, geometry and mesh tools, engineering software architecture, and computational physics.",
                    "Developed a parallel finite-volume electromagnetic solver, higher-order schemes, shared-memory infrastructure, and scientific testing tools.",
                ],
            ),
            section("Selected peer-reviewed publications"),
            p(
                "1. <b>P. Kumar</b> and P. I. Rosen Esquivel. A Reformulation of UVN-Flash for Multicomponent Two-Phase Systems with Application to CO2-Rich Mixture Transport in Pipelines. <i>Computers &amp; Fluids</i>, 314, 107108, 2026.",
                SMALL,
            ),
            p(
                "2. <b>P. Kumar</b> and P. I. Rosen Esquivel. Solving the UVN-Flash Problem in TVN-Space. <i>Fluid Phase Equilibria</i>, 599, 114528, 2026.",
                SMALL,
            ),
            p(
                "3. <b>P. Kumar</b>, B. Sanderse, P. I. Rosen Esquivel, and R. A. W. M. Henkes. A New Temperature Evolution Equation That Enforces Thermodynamic Vapour-Liquid Equilibrium in Multiphase Flows. <i>Computers &amp; Fluids</i>, 289, 106524, 2025.",
                SMALL,
            ),
            section("Web applications - secondary interest"),
        ]
    )

    web_box = Table(
        [[p(
            'I independently developed The Republic, Nazar India, Chess Duel, and WorkAtlas. The work demonstrates product thinking and self-directed learning, while remaining secondary to my scientific-computing and teaching direction. '
            '<link href="https://pkpardeepkumar30.github.io/web/" color="#006D68"><b>View web application experience</b></link>',
            BOX_BODY,
        )]],
        colWidths=[172 * mm],
    )
    web_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
                ("BOX", (0, 0), (-1, -1), 0.45, RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 3.5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3.5 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5 * mm),
            ]
        )
    )
    story.extend(
        [
            web_box,
            section("Languages"),
            p("English: proficient  |  Hindi: proficient  |  Dutch: A2", SMALL),
        ]
    )

    doc.build(story)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    build()
