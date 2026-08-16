"""Generate the Software, Web, and Teaching PDF resume variants."""

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
CV_DIR = ROOT / "public" / "cv"
SOFTWARE_OUTPUT = CV_DIR / "Resume_Pardeep_Kumar_Software.pdf"
WEB_OUTPUT = CV_DIR / "Resume_Pardeep_Kumar_Web.pdf"
TEACHING_OUTPUT = CV_DIR / "Resume_Pardeep_Kumar_Teaching.pdf"

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
EXPERIENCE_BULLET = ParagraphStyle(
    "ExperienceBullet",
    parent=BULLET,
    fontSize=7.35,
    leading=9.45,
    spaceAfter=0.3 * mm,
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
    parts.extend(bullet(item, EXPERIENCE_BULLET) for item in bullets)
    parts.append(Spacer(1, 0.55 * mm))
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


def build_teaching():
    TEACHING_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(TEACHING_OUTPUT),
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
            '<link href="https://pkpardeepkumar30.github.io/" color="#006D68">Portfolio</link><br/>'
            '<link href="https://www.linkedin.com/in/pkpardeepkumar30/" color="#006D68">LinkedIn</link>  |  '
            '<link href="https://scholar.google.com/citations?hl=en&amp;user=th4w0rYAAAAJ" color="#006D68">Google Scholar</link>  |  '
            'Languages: English, Hindi, Dutch (A2)',
            CONTACT,
        ),
        section("Profile"),
        p(
            'Scientific computing researcher with a submitted doctoral thesis developed at '
            '<link href="https://www.cwi.nl/en/" color="#006D68"><b>CWI Amsterdam</b></link> and '
            '<link href="https://www.tudelft.nl/en/me/about/departments/process-energy" color="#006D68"><b>TU Delft</b></link>, '
            'and more than ten years of experience in numerical modelling, simulation software, and computational problem-solving. '
            'My research concerns robust numerical methods for multiphase thermodynamics and CO2-rich transport.',
        ),
        p(
            "I am now exploring a serious transition toward high-school education. Teaching brings together the parts of research I value most: asking careful questions, making difficult ideas understandable, and helping someone gain the confidence to reason independently. I would bring broad examples, patient explanation, and an honest learning mindset to mathematics, physics, and computing education.",
        ),
        teaching_box(),
        section("Education"),
        education_entry(
            "PhD in Mechanical Engineering",
            '<link href="https://www.tudelft.nl/en/me/about/departments/process-energy" color="#53615E">Delft University of Technology</link> | '
            '<link href="https://www.cwi.nl/en/" color="#53615E">Research conducted at CWI Amsterdam</link>',
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
                    p("<b>Evidence and verification</b><br/>A research habit of examining assumptions, limiting cases, numerical results, and alternative explanations.", SMALL),
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
        section("Selected professional development at TU Delft"),
        p(
            "Graduate School courses: Scientific Storytelling; Advanced Problem Solving and Decision Making; Teamwork, Leadership and Group Dynamics; Conversation Skills; Embedding Societal Values in Research; and Scientific Integrity.",
            SMALL,
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
                "Aug 2022-Aug 14, 2026",
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
                "Shell, Amsterdam | Individual contributor",
                "Jun 2019-Dec 2021",
                [
                    "Migrated numerical workflows from Python to C++ and CUDA, reducing a representative runtime from about 30 minutes to 15 seconds.",
                    "Developed concurrent infrastructure, interoperability layers, and visualisation for process and pipeline simulation software.",
                ],
            ),
            entry(
                "Software Engineer",
                "Aakraya Research, Bangalore | Team of 2",
                "Feb-Apr 2019",
                [
                    "Developed regression-model generation and live profit-and-loss evaluation tools for high-frequency trading.",
                    "Improved C++ order-book infrastructure for efficient order matching.",
                ],
            ),
            entry(
                "Software Engineer II",
                "KLA-Tencor, Chennai | Team of 2",
                "May-Nov 2018",
                [
                    "Developed cross-application infrastructure and a silica-wafer thickness simulation engine using C#, F#, and MATLAB.",
                    "Implemented reusable testing libraries and an Erlang fault-tolerance mechanism with failover and recovery.",
                ],
            ),
            entry(
                "Software Engineer",
                "Altair, Bangalore | Team of 6",
                "Mar 2016-Apr 2018",
                [
                    "Developed shared-memory infrastructure and geometry and mesh-manipulation tools in C++.",
                    "Modernised C++/Python bindings, built Python testing frameworks, and contributed to an MVC refactoring.",
                ],
            ),
            entry(
                "Research and Development Engineer",
                "Fluidyn, Bangalore | Team of 4",
                "Jul 2014-Mar 2016",
                [
                    "Developed an MPI-parallel finite-volume electromagnetic solver with higher-order spatial schemes.",
                    "Implemented near-to-far-field transformations and extended a Navier-Stokes solver for aeroacoustic prediction.",
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
        ]
    )

    doc.build(story)
    print(f"Generated {TEACHING_OUTPUT}")


def make_document(output, title, keywords):
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=19 * mm,
        rightMargin=19 * mm,
        topMargin=13 * mm,
        bottomMargin=15 * mm,
        title=title,
        author="Pardeep Kumar",
        subject="Curriculum vitae",
        keywords=keywords,
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
    return doc


def career_header(role, include_scholar=False):
    second_line = (
        '<link href="https://www.linkedin.com/in/pkpardeepkumar30/" color="#006D68">LinkedIn</link>  |  '
        '<link href="https://github.com/pkpardeepkumar30" color="#006D68">GitHub</link>'
    )
    if include_scholar:
        second_line += (
            '  |  <link href="https://scholar.google.com/citations?hl=en&amp;user=th4w0rYAAAAJ" '
            'color="#006D68">Google Scholar</link>'
        )
    second_line += "  |  Languages: English, Hindi, Dutch (A2)"
    return [
        p("Pardeep Kumar", NAME),
        p(role, ROLE),
        p(
            'Amsterdam, the Netherlands  |  +31 6 1311 9813  |  '
            '<link href="mailto:pardeep.iitb@gmail.com" color="#006D68">pardeep.iitb@gmail.com</link>  |  '
            '<link href="https://pkpardeepkumar30.github.io/" color="#006D68">Portfolio</link><br/>'
            + second_line,
            CONTACT,
        ),
    ]


def grid(items, columns=2):
    rows = []
    for index in range(0, len(items), columns):
        row = [p(item, SMALL) for item in items[index:index + columns]]
        while len(row) < columns:
            row.append("")
        rows.append(row)
    width = 168 * mm / columns
    table = Table(rows, colWidths=[width] * columns, hAlign="LEFT")
    table.setStyle(
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
    return table


def impact_box(items):
    cells = []
    for number, label in items:
        cells.append(
            [
                p(f"<font size='15'><b>{number}</b></font>", BOX_HEADING),
                p(label, SMALL),
            ]
        )
    table = Table([cells], colWidths=[56 * mm] * 3, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
                ("BOX", (0, 0), (-1, -1), 0.45, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5 * mm),
            ]
        )
    )
    return table


def build_software():
    doc = make_document(
        SOFTWARE_OUTPUT,
        "Pardeep Kumar - Scientific Software Engineer",
        "scientific software, C++, Python, Julia, numerical methods, simulation, HPC, CUDA, MPI",
    )
    story = career_header(
        "SCIENTIFIC SOFTWARE ENGINEER  |  C++  |  PYTHON  |  JULIA  |  HIGH-PERFORMANCE COMPUTING",
        include_scholar=True,
    )
    story.extend(
        [
            section("Profile"),
            p(
                'Scientific software engineer with more than ten years of experience developing numerical solvers, high-performance simulation software, optimisation algorithms, and engineering applications. Experience spans energy, semiconductors, CAE, finance, computational electromagnetics, CFD, and scientific research. My submitted doctoral thesis was developed at '
                '<link href="https://www.cwi.nl/en/" color="#006D68"><b>CWI Amsterdam</b></link> and '
                '<link href="https://www.tudelft.nl/en/me/about/departments/process-energy" color="#006D68"><b>TU Delft</b></link>.',
            ),
            p(
                "Strong at translating mathematical and physical models into robust, tested, maintainable software, from formulation and implementation through profiling, interoperability, verification, and documentation.",
            ),
            section("Selected engineering impact"),
            impact_box(
                [
                    ("30x", "Faster constrained thermodynamic optimisation formulation"),
                    ("30 min to 15 sec", "GPU-enabled scientific workflow after C++ and CUDA migration"),
                    (">15x", "Higher throughput for multi-client simulation data workflows"),
                ]
            ),
            section("Technical strengths"),
            grid(
                [
                    "<b>Programming</b><br/>C++, Python, Julia, C#, Java, F#, MATLAB, TypeScript, and Erlang.",
                    "<b>Numerical methods</b><br/>Finite-volume and finite-difference methods, nonlinear optimisation, Riemann solvers, thermodynamics, CFD, and numerical linear algebra.",
                    "<b>High-performance computing</b><br/>CUDA, MPI, multithreading, concurrent programming, shared memory, profiling, and performance optimisation.",
                    "<b>Software engineering</b><br/>Modular architecture, OOP and functional programming, MVC, API interoperability, unit testing, TDD, Git, Perforce, and CI-oriented development.",
                    "<b>Computational physics</b><br/>Multiphase flow, electromagnetics, wave propagation, real-fluid thermodynamics, aeroacoustics, and numerical relativity.",
                    "<b>AI and data workflows</b><br/>Neural surrogate models, scientific-data pipelines, automated training and validation, and reproducible experiments.",
                ]
            ),
            section("Recent experience"),
            entry(
                "PhD Researcher in Scientific Computing",
                'Centrum Wiskunde &amp; Informatica (CWI), Amsterdam',
                "Aug 2022-Aug 14, 2026",
                [
                    "Developed Julia and Python solvers for transient multiphase, multicomponent flow with an emphasis on robustness, convergence, validation, and efficiency.",
                    "Reformulated constrained phase-equilibrium algorithms, achieving approximately 30x speedup over a traditional nested approach.",
                    "Built neural thermodynamics workflows and scientific software for hyperbolic flow models and numerical relativity.",
                ],
            ),
            entry(
                "Software Engineer",
                "ASM International, Almere",
                "Feb-Aug 2022",
                [
                    "Enhanced and refactored a Java simulator for semiconductor thin-film deposition equipment.",
                    "Improved modularity, maintainability, testability, and incremental feature delivery.",
                ],
            ),
            entry(
                "Software Engineer",
                "Shell, Amsterdam | Individual contributor",
                "Jun 2019-Dec 2021",
                [
                    "Migrated Python workflows to C++ and CUDA, reducing a representative runtime from about 30 minutes to 15 seconds.",
                    "Designed concurrent data infrastructure and C#/C++ interoperability for process and pipeline simulation tools.",
                    "Improved multi-client throughput by more than 15x and built modular visualisation components.",
                ],
            ),
            PageBreak(),
        ]
    )
    story.extend(career_header("SCIENTIFIC SOFTWARE ENGINEERING EXPERIENCE AND OUTPUT", include_scholar=False)[:2])
    story.extend(
        [
            section("Earlier engineering experience"),
            entry(
                "Software Engineer",
                "Aakraya Research, Bangalore | Team of 2",
                "Feb-Apr 2019",
                [
                    "Developed Python regression-model generators and post-trade performance-analysis tools.",
                    "Built profit-and-loss analysis tools for evaluating live-trading performance.",
                    "Improved C++ order-book infrastructure for efficient matching and market-data processing.",
                ],
            ),
            entry(
                "Software Engineer II",
                "KLA-Tencor, Chennai | Team of 2",
                "May-Nov 2018",
                [
                    "Built C# and F# cross-application infrastructure and a C#/F#/MATLAB wafer-thickness simulator.",
                    "Developed shared C++ and C# libraries for common functionality across server applications.",
                    "Implemented unit tests and Erlang fault tolerance with failover and recovery.",
                ],
            ),
            entry(
                "Software Engineer",
                "Altair, Bangalore | Team of 6",
                "Mar 2016-Apr 2018",
                [
                    "Developed C++ shared-memory infrastructure and geometry and mesh tools for HyperMesh.",
                    "Modernised C++/Python bindings from SWIG to Boost.Python and built Python testing frameworks.",
                    "Contributed to an MVC refactoring and extended COM-based application APIs.",
                ],
            ),
            entry(
                "Research and Development Engineer",
                "Fluidyn, Bangalore | Team of 4",
                "Jul 2014-Mar 2016",
                [
                    "Developed an MPI-parallel finite-volume electromagnetic solver in C++ and C#.",
                    "Implemented second- and third-order spatial schemes and near-to-far-field radar cross-section processing.",
                    "Extended a Navier-Stokes solver for far-field aeroacoustic prediction using retarded-time integration.",
                ],
            ),
            section("Education"),
            education_entry(
                "PhD in Mechanical Engineering",
                'TU Delft | Research conducted at CWI Amsterdam',
                "2022-2026",
                "Thesis submitted; defence planned for January 2027. Numerical methods for multicomponent, multiphase pipeline transport.",
            ),
            education_entry(
                "MSc in Aerospace Engineering",
                "Indian Institute of Technology Bombay, India",
                "2012-2014",
                "Finite-volume time-domain methods for electromagnetic propagation and scattering.",
            ),
            section("Selected peer-reviewed output"),
            p(
                "1. <b>P. Kumar</b> and P. I. Rosen Esquivel. A Reformulation of UVN-Flash for Multicomponent Two-Phase Systems with Application to CO2-Rich Mixture Transport in Pipelines. <i>Computers &amp; Fluids</i>, 314, 107108, 2026.",
                SMALL,
            ),
            p(
                "2. <b>P. Kumar</b> and P. I. Rosen Esquivel. Solving the UVN-Flash Problem in TVN-Space. <i>Fluid Phase Equilibria</i>, 599, 114528, 2026.",
                SMALL,
            ),
            p(
                "3. <b>P. Kumar</b>, B. Sanderse, P. I. Rosen Esquivel, and R. A. W. M. Henkes. A New Temperature Evolution Equation That Enforces Thermodynamic Vapour-Liquid Equilibrium in Multiphase Flows. <i>Computers &amp; Fluids</i>, 289, 106524, 2025. "
                '<link href="https://pkpardeepkumar30.github.io/publications/" color="#006D68"><b>View publications</b></link>.',
                SMALL,
            ),
            section("Independent product work"),
            p(
                "Built and deployed four public web products using TypeScript, React, Next.js, Python, Rust, PostgreSQL, and cloud platforms. "
                '<link href="https://pkpardeepkumar30.github.io/web/" color="#006D68"><b>View web applications</b></link>.',
                SMALL,
            ),
        ]
    )
    doc.build(story)
    print(f"Generated {SOFTWARE_OUTPUT}")


def build_web():
    doc = make_document(
        WEB_OUTPUT,
        "Pardeep Kumar - Full-Stack Software Engineer",
        "full-stack software, TypeScript, Next.js, React, PostgreSQL, Python, Rust, cloud deployment",
    )
    story = career_header(
        "FULL-STACK SOFTWARE ENGINEER  |  NEXT.JS  |  TYPESCRIPT  |  REACT  |  POSTGRESQL",
        include_scholar=False,
    )
    story.extend(
        [
            section("Profile"),
            p(
                "Software engineer with more than ten years of experience building applications, data-integration frameworks, simulation platforms, and performance-critical backend components. I independently design, implement, and deploy web products using TypeScript, Next.js, React, PostgreSQL, Python, Rust, real-time services, authentication, automation, and cloud platforms.",
            ),
            p(
                "My engineering background brings strong architecture, performance, testing, interoperability, and problem-solving habits to product development. I am comfortable carrying an idea from requirements and data modelling through responsive UI, server logic, deployment, observability, and iteration.",
            ),
            section("Full-stack strengths"),
            grid(
                [
                    "<b>Frontend</b><br/>Next.js, React, TypeScript, JavaScript, HTML, CSS, responsive UI, and accessible interaction.",
                    "<b>Backend and data</b><br/>Node.js, Python, Rust, PostgreSQL, Drizzle ORM, SQL, REST APIs, server actions, and validation.",
                    "<b>Identity and realtime</b><br/>Authentication, permissions, owner-scoped data, Appwrite, transactions, reconnect handling, and persistent sessions.",
                    "<b>Deployment</b><br/>Vercel, Cloudflare, Docker, GitHub Actions, environment configuration, migrations, and scheduled publishing.",
                    "<b>Architecture</b><br/>Configuration-driven systems, modular monoliths, component registries, data pipelines, and API interoperability.",
                    "<b>Broader programming</b><br/>C++, C#, Java, Julia, F#, CUDA, MPI, concurrency, profiling, and performance optimisation.",
                ]
            ),
            section("Selected web products"),
            entry(
                "WorkAtlas",
                'Next.js | React | TypeScript | PostgreSQL | Drizzle ORM | <link href="https://workatlas-kappa.vercel.app/" color="#006D68">Live application</link>',
                "2026",
                [
                    "Designed a multi-user workspace for research, projects, publications, experiments, tasks, and long-term ideas.",
                    "Implemented authentication, owner-scoped data, project and Kanban workflows, comments, reminders, documentation, and portable exports.",
                    "Created a configuration-driven content system and deployed it with Vercel and Neon PostgreSQL.",
                ],
            ),
            entry(
                "The Republic",
                'Rust | Axum | Tokio | Phaser 3 | PWA | <link href="https://the-republic.pages.dev/" color="#006D68">Live application</link>',
                "2026",
                [
                    "Built a civic strategy simulation with persistent sessions, idempotent actions, and validated scenario packs.",
                    "Developed a responsive browser client and installable PWA with mobile-ready interaction.",
                ],
            ),
            entry(
                "Nazar India",
                'Python | Static publishing | AI-assisted pipeline | Cloudflare | <link href="https://nazar-india.pages.dev/" color="#006D68">Live application</link>',
                "2026",
                [
                    "Built a source-transparent news platform with RSS collection, validation, search, filtering, archives, and structured metadata.",
                    "Automated four-hour collection and publishing workflows with GitHub Actions and Cloudflare.",
                ],
            ),
            entry(
                "Chess Duel",
                'Next.js | TypeScript | Appwrite | Realtime | <link href="https://chess-duel.appwrite.network/" color="#006D68">Live application</link>',
                "2026",
                [
                    "Implemented server-authoritative chess rules, transaction-safe realtime synchronisation, reconnect handling, and persistent records.",
                    "Supported instant guest play, verified accounts, responsive board orientation, and complete draw conditions.",
                ],
            ),
            PageBreak(),
        ]
    )
    story.extend(career_header("SOFTWARE EXPERIENCE SUPPORTING FULL-STACK DELIVERY", include_scholar=False)[:2])
    story.extend(
        [
            section("Professional experience"),
            entry(
                "PhD Researcher in Scientific Computing",
                "Centrum Wiskunde &amp; Informatica (CWI), Amsterdam",
                "Aug 2022-Aug 14, 2026",
                [
                    "Built maintainable Julia and Python applications, data-generation pipelines, validation workflows, and reproducible computational experiments.",
                    "Delivered an approximately 30x optimisation speedup and developed automated neural-model training and validation workflows.",
                ],
            ),
            entry(
                "Software Engineer",
                "ASM International, Almere",
                "Feb-Aug 2022",
                [
                    "Delivered Java simulator features and refactored legacy components for modularity, testability, and release velocity.",
                    "Worked across software and equipment-domain teams to translate operational workflows into application behaviour.",
                ],
            ),
            entry(
                "Software Engineer",
                "Shell, Amsterdam | Individual contributor",
                "Jun 2019-Dec 2021",
                [
                    "Designed concurrent integrations between real-time databases and process and pipeline applications.",
                    "Improved throughput by more than 15x and built C#/C++ interoperability, visualisation, and GPU-accelerated components.",
                ],
            ),
            entry(
                "Software Engineer",
                "Aakraya Research, Bangalore | Team of 2",
                "Feb-Apr 2019",
                [
                    "Built Python applications for model generation, profit-and-loss calculation, and post-trade analytics.",
                    "Improved C++ order-book and market-data components.",
                ],
            ),
            entry(
                "Software Engineer II",
                "KLA-Tencor, Chennai | Team of 2",
                "May-Nov 2018",
                [
                    "Built reusable C# and F# server infrastructure, shared libraries, simulation features, tests, and Erlang fault tolerance.",
                ],
            ),
            entry(
                "Software Engineer",
                "Altair, Bangalore | Team of 6",
                "Mar 2016-Apr 2018",
                [
                    "Developed shared-memory infrastructure, engineering UI features, C++/Python integrations, COM APIs, and testing frameworks.",
                ],
            ),
            entry(
                "Research and Development Engineer",
                "Fluidyn, Bangalore | Team of 4",
                "Jul 2014-Mar 2016",
                [
                    "Built C++/C# simulation applications, MPI components, reusable numerical libraries, and parallel processing workflows.",
                ],
            ),
            section("Engineering impact"),
            impact_box(
                [
                    ("10+ years", "Cross-industry software engineering experience"),
                    (">15x", "Higher throughput in a concurrent data-integration workflow"),
                    ("4 products", "Independently designed, built, and publicly deployed"),
                ]
            ),
            section("Education"),
            education_entry(
                "PhD in Mechanical Engineering",
                "TU Delft | Research conducted at CWI Amsterdam",
                "2022-2026",
                "Thesis submitted; defence planned for January 2027.",
            ),
            education_entry(
                "MSc in Aerospace Engineering",
                "Indian Institute of Technology Bombay, India",
                "2012-2014",
                "Numerical simulation of electromagnetic propagation and scattering.",
            ),
        ]
    )
    doc.build(story)
    print(f"Generated {WEB_OUTPUT}")


if __name__ == "__main__":
    build_software()
    build_web()
    build_teaching()
