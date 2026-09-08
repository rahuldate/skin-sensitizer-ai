import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Colors
DARK_NAVY = RGBColor(15, 23, 42)
SLATE_GRAY = RGBColor(71, 85, 105)
TEAL_ACCENT = RGBColor(13, 148, 136)
WHITE = RGBColor(255, 255, 255)
LIGHT_BG = RGBColor(248, 250, 252)

def add_header(slide, title_text, category_text="EXECUTIVE BRIEFING"):
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = TEAL_ACCENT
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = DARK_NAVY

# Slide 1: Title
slide_layout = prs.slide_layouts[6]
slide1 = prs.slides.add_slide(slide_layout)
bg1 = slide1.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = DARK_NAVY

tb = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.5))
tf = tb.text_frame
p1 = tf.paragraphs[0]
p1.text = "Next-Gen In Silico Skin Sensitization AI"
p1.font.size = Pt(36)
p1.font.bold = True
p1.font.color.rgb = WHITE

p2 = tf.add_paragraph()
p2.text = "Automated Defined Approach based on OECD Guideline 497 & UN GHS"
p2.font.size = Pt(20)
p2.font.color.rgb = TEAL_ACCENT

p3 = tf.add_paragraph()
p3.text = "\nCreated by Dr. Rahul Anant Date with Gemini AI"
p3.font.size = Pt(16)
p3.font.color.rgb = RGBColor(203, 213, 225)

# Slide 2: Strategic Executive Summary
slide2 = prs.slides.add_slide(slide_layout)
add_header(slide2, "Strategic R&D & Regulatory Context")
tb2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
tf2 = tb2.text_frame
tf2.word_wrap = True
items2 = [
    ("The Global Regulatory Imperative: ", "Animal testing for cosmetics and consumer formulations is banned across the EU, UK, India, and APAC. REACH requires non-animal New Approach Methodologies (NAMs)."),
    ("The Multi-Agent Solution: ", "We built an autonomous in silico testing battery that replicates the OECD GL 497 Defined Approach (DA) to predict skin sensitization with regulatory concordance."),
    ("Core Value Drivers: ", "Delivers instant hazard classification (UN GHS Cat 1A / 1B / NC), reduces laboratory screening costs by >95%, and accelerates pre-market formulation pipelines.")
]
for head, body in items2:
    p = tf2.add_paragraph()
    p.text = "• " + head + body
    p.font.size = Pt(16)
    p.space_after = Pt(18)
    p.font.color.rgb = DARK_NAVY

# Slide 3: Multi-Agent Architecture
slide3 = prs.slides.add_slide(slide_layout)
add_header(slide3, "Five-Agent OECD GL 497 Architecture")
tb3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
tf3 = tb3.text_frame
tf3.word_wrap = True
agents = [
    ("Bot 1: Chemist Agent", "Scans for 12+ OECD electrophilic SMARTS haptenation alerts, prohaptens, and transition metal chelation."),
    ("Bot 2: Toxicologist Agent", "Predicts Adverse Outcome Pathway Key Events: KE1 (DPRA - TG 442C), KE2 (KeratinoSens - TG 442D), KE3 (h-CLAT - TG 442E)."),
    ("Bot 3: Statistician Agent", "Integrates weighted Key Event evidence (0.50 KE1 + 0.25 KE2 + 0.25 KE3) and computes Applicability Domain compliance."),
    ("Bot 4: Regulatory Agent", "Assigns official UN GHS Classification (Category 1A Strong, 1B Moderate, or Not Classified) and specifies next testing actions."),
    ("Bot 5: QA & Audit Agent", "Generates immutable SHA-256 traceable audit IDs for regulatory audit trail compliance.")
]
for name, desc in agents:
    p = tf3.add_paragraph()
    p.text = f"• {name}: {desc}"
    p.font.size = Pt(15)
    p.space_after = Pt(14)
    p.font.color.rgb = DARK_NAVY

# Slide 4: Demo Benchmark Table
slide4 = prs.slides.add_slide(slide_layout)
add_header(slide4, "Demonstration Benchmarks: OECD 497 Validation")

table_shape = slide4.shapes.add_table(5, 5, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.5))
table = table_shape.table

headers = ["Substance", "CAS RN", "Mechanism / Alerts", "Consensus Score", "OECD 497 / GHS Call"]
for col_idx, h_text in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.text = h_text
    cell.fill.solid()
    cell.fill.fore_color.rgb = DARK_NAVY
    for p in cell.text_frame.paragraphs:
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE

rows_data = [
    ["Acrylic Acid", "79-10-7", "Michael Acceptor (Ester/Acid)", "0.840", "SENSITIZER (GHS Cat 1B)"],
    ["Benzoic Acid", "65-85-0", "Non-electrophilic (Unreactive)", "0.160", "NON-SENSITIZER (GHS NC)"],
    ["Nickel", "7440-02-0", "Metal Chelation / TLR4 Axis", "0.893", "SENSITIZER (GHS Cat 1A)"],
    ["Rebaudioside A", "58543-16-1", "Natural Glycoside (High MW)", "0.160", "NON-SENSITIZER (GHS NC)"]
]

for row_idx, row in enumerate(rows_data):
    for col_idx, val in enumerate(row):
        cell = table.cell(row_idx + 1, col_idx)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.color.rgb = DARK_NAVY

# Slide 5: Business ROI & Impact
slide5 = prs.slides.add_slide(slide_layout)
add_header(slide5, "Business ROI & Operational Impact")
tb5 = slide5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
tf5 = tb5.text_frame
tf5.word_wrap = True
roi_points = [
    ("Drastic Cost Reduction: ", "Traditional in vitro 2-of-3 battery testing costs $8,000–$15,000 per compound. In silico screening costs < $0.05 per molecule."),
    ("Accelerated Time-to-Market: ", "Replaces 4–8 week CRO turnaround cycles with sub-second automated evaluations."),
    ("Pre-Screening R&D Funnel: ", "High-throughput batch screening weeds out hazardous lead candidates before entering costly laboratory synthesis."),
    ("100% Animal-Free Compliance: ", "Ensures full compliance with EU Cosmetic Regulation 1223/2009 and global NAM directives.")
]
for head, body in roi_points:
    p = tf5.add_paragraph()
    p.text = "• " + head + body
    p.font.size = Pt(16)
    p.space_after = Pt(18)
    p.font.color.rgb = DARK_NAVY

# Slide 6: Conclusion & Credits
slide6 = prs.slides.add_slide(slide_layout)
bg6 = slide6.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg6.fill.solid()
bg6.fill.fore_color.rgb = DARK_NAVY

tb6 = slide6.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.5))
tf6 = tb6.text_frame
p1 = tf6.paragraphs[0]
p1.text = "Platform Ready for Enterprise Deployment"
p1.font.size = Pt(34)
p1.font.bold = True
p1.font.color.rgb = WHITE

p2 = tf6.add_paragraph()
p2.text = "Seamless integration with internal R&D databases, formulation pipelines, and regulatory dossiers."
p2.font.size = Pt(18)
p2.font.color.rgb = TEAL_ACCENT

p3 = tf6.add_paragraph()
p3.text = "\nDesigned & Developed by Dr. Rahul Anant Date with Gemini AI"
p3.font.size = Pt(16)
p3.font.color.rgb = RGBColor(203, 213, 225)

output_path = "Skin_Sensitizer_AI_Management_Presentation.pptx"
prs.save(output_path)
print(f"Presentation saved successfully as '{output_path}'")
