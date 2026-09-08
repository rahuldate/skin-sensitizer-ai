with open("app.py", "r") as f:
    lines = f.readlines()

# --- 1. Fix Indentation in HITL PDF section around line 1686 ---
for i in range(len(lines)):
    if "story.append(Paragraph(\"<b>4. Expert Human-in-the-Loop" in lines[i]:
        # Dedent subsequent lines until the next unindented block
        for j in range(i + 1, min(len(lines), i + 40)):
            if lines[j].startswith("        hitl_rows") or lines[j].startswith("            ") or lines[j].startswith("        ]"):
                lines[j] = lines[j][4:]
            elif lines[j].startswith("def ") or lines[j].startswith("class "):
                break
        print(f"✅ Adjusted HITL PDF indentation around line {i+1}")
        break

content = "".join(lines)

# --- 2. Update evaluate_pro_pre_hapten_activation with enhanced SMARTS ---
target_fn = "def evaluate_pro_pre_hapten_activation(mol) -> dict:"
new_fn_body = '''def evaluate_pro_pre_hapten_activation(mol) -> dict:
    if mol is None:
        return {"category": "Direct-acting Electrophile", "classification": "Direct-acting Electrophile", "alerts": ["No valid structure parsed"], "pathway": "Direct Nucleophilic Adduct Formation"}
    
    alerts = []
    category = "Direct-acting Electrophile"
    pathway = "Direct Nucleophilic Adduct Formation"
    
    p1 = Chem.MolFromSmarts("Oc1ccc(C=CC)cc1")
    p2 = Chem.MolFromSmarts("Oc1ccc(CC=C)cc1")
    p3 = Chem.MolFromSmarts("c1cc(OC)c(O)cc1C=CC")
    p4 = Chem.MolFromSmarts("Oc1c(OC)ccc(C=CC)c1")
    is_propenyl_phenol = any(mol.HasSubstructMatch(p) for p in [p1, p2, p3, p4] if p)
    
    pa = Chem.MolFromSmarts("[CH2;D2]([OH])[CH]=[CH]")
    is_allyl_alcohol = mol.HasSubstructMatch(pa) if pa else False
    
    pc1 = Chem.MolFromSmarts("Oc1ccccc1O")
    pc2 = Chem.MolFromSmarts("Oc1ccc(O)cc1")
    is_catechol = any(mol.HasSubstructMatch(p) for p in [pc1, pc2] if p)
    
    pn1 = Chem.MolFromSmarts("Nc1ccc(N)cc1")
    pn2 = Chem.MolFromSmarts("Nc1ccccc1")
    is_amine = any(mol.HasSubstructMatch(p) for p in [pn1, pn2] if p)
    
    pt1 = Chem.MolFromSmarts("C=C(C)CC")
    pt2 = Chem.MolFromSmarts("CC(=C)C")
    is_terpene = any(mol.HasSubstructMatch(p) for p in [pt1, pt2] if p)
    
    if is_propenyl_phenol:
        alerts.append("Propenyl Phenol Core: Cutaneous CYP-mediated oxidation yielding reactive Quinone-Methide intermediate")
        alerts.append("Air Auto-Oxidation Pre-Hapten: Spontaneous formation of Isoeugenol hydroperoxide")
        category = "Pro-Hapten & Pre-Hapten (Dual Activation)"
        pathway = "Cutaneous CYP450 Quinone-Methide & Auto-Oxidation Radical Cascade"
    elif is_allyl_alcohol:
        alerts.append("Allylic Primary Alcohol: Cutaneous Alcohol Dehydrogenase (ADH) oxidation to reactive Alpha,Beta-Unsaturated Aldehyde")
        category = "Pro-Hapten (Enzymatic Bioactivation)"
        pathway = "Cutaneous ADH Alcohol Oxidation to Michael Acceptor"
    elif is_catechol:
        alerts.append("Polyphenolic Ring: Cutaneous Tyrosinase / Peroxidase oxidation to reactive ortho/para-Benzoquinone")
        category = "Pro-Hapten & Pre-Hapten"
        pathway = "Enzymatic & Spontaneous Quinone Formation"
    elif is_amine:
        alerts.append("Aromatic Amine Core: Cutaneous Phase I N-hydroxylation & diimine oxidation")
        category = "Pro-Hapten (Cutaneous CYP/NAT Bioactivation)"
        pathway = "N-Hydroxylation to Reactive Benzoquinone Diimine"
    elif is_terpene:
        alerts.append("Conjugated / Terpenic Double Bond: High susceptibility to atmospheric allylic auto-oxidation (Hydroperoxide Pre-Hapten)")
        category = "Pre-Hapten (Auto-Oxidation)"
        pathway = "Atmospheric Air Oxidation to Reactive Hydroperoxides"
    else:
        alerts.append("No structural pro/pre-hapten bioactivation alerts identified")
        category = "Direct-acting Electrophile"
        pathway = "Direct Nucleophilic Adduct Formation"
        
    return {
        "category": category,
        "classification": category,
        "alerts": alerts,
        "pathway": pathway
    }'''

# Replace evaluate_pro_pre_hapten_activation safely
import re
content = re.sub(
    r"def evaluate_pro_pre_hapten_activation\(mol\) -> dict:.*?(?=\ndef [a-zA-Z_])",
    new_fn_body + "\n",
    content,
    flags=re.DOTALL
)

# --- 3. Inject Cutaneous Bioactivation card into Section 2 of render_dashboard_cards ---
sec3_header = 'st.markdown("### ⚡ 3. OpenMM MD Dynamics, Quantitative Potency & 3D Protein Structure")'
bioact_card = """    # Cutaneous Metabolism & Pro/Pre-Hapten Bioactivation Card
    st.markdown("#### 🧪 Cutaneous Bioactivation & Pre/Pro-Hapten Profiling")
    bioact = res.get("Bioactivation") or (classify_cutaneous_bioactivation(res.get("SMILES", "")) if "classify_cutaneous_bioactivation" in globals() else {})
    pro_pre = res.get("Pro_Pre_Hapten") or evaluate_pro_pre_hapten_activation(Chem.MolFromSmiles(res.get("SMILES", "")) if res.get("SMILES") else None)
    
    col_mb1, col_mb2 = st.columns([1, 1])
    with col_mb1:
        bioact_class = pro_pre.get("category") or bioact.get("classification", "Direct-acting Electrophile")
        badge_color = "#dc2626" if "Pro-Hapten" in bioact_class or "Pre-Hapten" in bioact_class or "Pro-hapten" in bioact_class else "#16a34a"
        badge_bg = "#fef2f2" if "Pro-Hapten" in bioact_class or "Pre-Hapten" in bioact_class or "Pro-hapten" in bioact_class else "#f0fdf4"
        st.markdown(f\"\"\"
        <div style="background:{badge_bg}; border:1.5px solid {badge_color}; border-radius:8px; padding:12px;">
            <div style="color:#64748b; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Hapten Activation Mode</div>
            <div style="color:{badge_color}; font-size:1.05rem; font-weight:800; margin-top:3px;">{bioact_class}</div>
            <div style="color:#334155; font-size:0.82rem; margin-top:4px;"><b>Mechanistic Pathway:</b> {pro_pre.get('pathway', bioact.get('pathway', 'Direct Nucleophilic Adduct Formation'))}</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with col_mb2:
        alerts = pro_pre.get("alerts", []) or bioact.get("alerts", ["No structural metabolic alerts identified"])
        alerts_str = "<br>• ".join(alerts) if isinstance(alerts, list) else str(alerts)
        st.markdown(f\"\"\"
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:12px;">
            <div style="color:#64748b; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Skin Enzymatic / Auto-Oxidation Alerts</div>
            <div style="color:#0f172a; font-size:0.85rem; font-weight:600; margin-top:3px;">• {alerts_str}</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### ⚡ 3. OpenMM MD Dynamics, Quantitative Potency & 3D Protein Structure")"""

if sec3_header in content and "Cutaneous Bioactivation & Pre/Pro-Hapten Profiling" not in content:
    content = content.replace(sec3_header, bioact_card, 1)
    print("✅ Injected Cutaneous Bioactivation dashboard card.")

# --- 4. Append Main UI Input Controller at the very bottom ---
main_ui_tail = """

# =====================================================================
# MAIN APPLICATION CONTROLLER & DASHBOARD EXECUTION
# =====================================================================
st.markdown("---")
st.header("🔬 Target Chemical Assessment")

col_in1, col_in2 = st.columns([4, 1])
with col_in1:
    user_query = st.text_input(
        "Enter Chemical Name, CAS RN, or SMILES String:",
        value="1-Chloro-2,4-dinitrobenzene (DNCB)",
        help="Provide a chemical identifier (e.g., DNCB, Isoeugenol, Cinnamyl alcohol, PPD, or SMILES)."
    )
with col_in2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run Assessment", type="primary", use_container_width=True)

if user_query:
    active_key = api_key_input if "api_key_input" in locals() and api_key_input else ""
    with st.spinner("⏳ Running OpenMM Molecular Dynamics, Defined Approaches & Multi-Agent Council..."):
        try:
            res = process_single_chemical(user_query, api_key=active_key)
            if res:
                render_dashboard_cards(res)
            else:
                st.error("❌ Unable to resolve chemical structure. Please verify the CAS/SMILES.")
        except Exception as e:
            st.error(f"❌ Execution Error: {e}")
            import traceback
            st.text(traceback.format_exc())

# Render footer
st.markdown(\"\"\"
<div style="text-align: center; padding: 24px 0; color: #64748b; font-size: 13px; border-top: 1px solid #e2e8f0; margin-top: 40px;">
    <p style="margin: 0; font-weight: 600;">🧪 SensAOP Enterprise Platform | Powered by OpenMM MD, Gemini LLM & OECD GL 497</p>
    <p style="margin: 4px 0 0 0; color: #475569;">Created by <strong>Dr. Rahul Anant Date</strong> with <strong>Gemini AI</strong></p>
</div>
\"\"\", unsafe_allow_html=True)
"""

if "# MAIN APPLICATION CONTROLLER & DASHBOARD EXECUTION" not in content:
    content = content.strip() + "\n\n" + main_ui_tail.strip() + "\n"
    print("✅ Appended main execution controller to the bottom of app.py.")

with open("app.py", "w") as f:
    f.write(content)

print("🎯 Master patch successfully applied!")
