import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Procedural Fairness in Healthcare AI", page_icon="🏥", layout="wide")

PRIMARY = "#c9748f"
LIGHT = "#f2c4ce"
DARK = "#1a1a1a"
BG = "#fdf8f9"
PASS_COLOR = "#2d6a4f"
FAIL_COLOR = "#9d0208"
PARTIAL_COLOR = "#856404"
PASS_BG = "#d8f3dc"
FAIL_BG = "#ffe0e0"
PARTIAL_BG = "#fff3cd"
RULE_LABEL = "#993556"

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; }}
    .block-container {{ padding: 2rem 3rem; max-width: 1200px; }}
    h1 {{ color: {PRIMARY}; font-family: Georgia, serif; font-size: 2rem; margin-bottom: 0; }}
    h2 {{ color: {DARK}; font-size: 1.3rem; font-weight: 600; margin-top: 2rem; }}
    h3 {{ color: {DARK}; font-size: 1.1rem; font-weight: 600; }}
    .subtitle {{ color: #666; font-size: 1rem; margin-top: 0.2rem; margin-bottom: 1.5rem; }}
    .card {{ background: white; border-radius: 10px; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
    .pass-card {{ border-left: 4px solid {PASS_COLOR}; background: {PASS_BG}; }}
    .fail-card {{ border-left: 4px solid {FAIL_COLOR}; background: {FAIL_BG}; }}
    .partial-card {{ border-left: 4px solid {PARTIAL_COLOR}; background: {PARTIAL_BG}; }}
    .rule-name {{ font-weight: 700; font-size: 1.05rem; }}
    .rule-desc {{ font-size: 0.88rem; color: #444; margin-top: 0.3rem; }}
    .badge {{ display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }}
    .pass-badge {{ background: {PASS_COLOR}; color: white; }}
    .fail-badge {{ background: {FAIL_COLOR}; color: white; }}
    .partial-badge {{ background: {PARTIAL_COLOR}; color: white; }}
    .divider {{ border: none; border-top: 1px solid #eee; margin: 1.5rem 0; }}
    .survey-stat {{ background: white; border-radius: 10px; padding: 1rem 1.2rem; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
    .survey-pct {{ font-size: 2.2rem; font-weight: 700; color: {PRIMARY}; }}
    .survey-label {{ font-size: 0.82rem; color: #555; margin-top: 0.2rem; }}
    .rec-box {{ background: white; border-radius: 10px; padding: 1rem 1.4rem; margin-bottom: 0.6rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-left: 4px solid {PRIMARY}; }}
    .hero-number {{ font-size: 2.8rem; font-weight: 700; color: {DARK}; line-height: 1; }}
    .hero-desc {{ font-size: 0.85rem; color: #5a5a5a; margin-top: 0.3rem; }}
    .rule-label {{ font-size: 0.9rem; font-weight: 700; color: {RULE_LABEL}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.8rem; }}
    .tier-section {{ background: white; border-radius: 10px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
    .kpi-label {{ font-size: 1.1rem; font-weight: 700; color: {DARK}; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.3rem; }}
    .kpi-number {{ font-size: 4.5rem; font-weight: 700; color: {PRIMARY}; line-height: 1; }}
    .method-box {{ background: white; border-radius: 10px; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-left: 4px solid {PRIMARY}; }}
    .tooltip {{ position: relative; display: inline-block; cursor: help; border-bottom: 1px dotted #888; }}
    .tooltip .tooltiptext {{ visibility: hidden; width: 320px; background-color: #333; color: #fff;
        text-align: left; border-radius: 6px; padding: 8px 12px; position: absolute; z-index: 1;
        bottom: 125%; left: 50%; margin-left: -160px; font-size: 0.78rem; line-height: 1.4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2); }}
    .tooltip:hover .tooltiptext {{ visibility: visible; }}

    /* ── THEME OVERRIDES: prevent dark mode from breaking colors ── */
    .stApp {{ background-color: {BG} !important; }}
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {{
        color: {DARK} !important;
    }}
    /* Preserve intentionally colored elements */
    .pass-badge, .fail-badge, .partial-badge {{ color: white !important; }}
    .tooltip .tooltiptext {{ color: #fff !important; background-color: #333 !important; }}
    .card, .method-box, .rec-box, .tier-section, .survey-stat {{
        background: white !important;
        color: {DARK} !important;
    }}
    .pass-card {{ background: {PASS_BG} !important; }}
    .fail-card {{ background: {FAIL_BG} !important; }}
    .partial-card {{ background: {PARTIAL_BG} !important; }}
    /* Force Streamlit tab text visible */
    .stTabs [data-baseweb="tab-list"] button {{
        color: {DARK} !important;
        font-size: 0.9rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }}
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: {PRIMARY} !important;
        border-bottom-color: {PRIMARY} !important;
    }}
    /* Ensure tab bar scrolls horizontally on small screens */
    .stTabs [data-baseweb="tab-list"] {{
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        -webkit-overflow-scrolling: touch;
        gap: 0 !important;
    }}
    .stTabs [data-baseweb="tab-list"] button {{
        white-space: nowrap !important;
        flex-shrink: 0 !important;
    }}
    /* Streamlit metric text color fix */
    [data-testid="stMetricValue"] {{ color: {PRIMARY} !important; }}
    [data-testid="stMetricLabel"] {{ color: {DARK} !important; }}

    /* ── RESPONSIVE: tablets and smaller ── */
    @media (max-width: 768px) {{
        .block-container {{ padding: 1rem 1rem !important; }}
        h1 {{ font-size: 1.4rem !important; }}
        h2 {{ font-size: 1.1rem !important; }}
        h3 {{ font-size: 1rem !important; }}
        .kpi-number {{ font-size: 3rem !important; }}
        .hero-number {{ font-size: 2rem !important; }}
        .survey-pct {{ font-size: 1.6rem !important; }}
        .card {{ padding: 1rem !important; }}
        .tooltip .tooltiptext {{
            width: 240px !important;
            margin-left: -120px !important;
            font-size: 0.72rem !important;
        }}
        /* Stack grids on mobile */
        div[style*="grid-template-columns:1fr 1fr"] {{
            grid-template-columns: 1fr !important;
        }}
        div[style*="grid-template-columns:auto 1fr"] {{
            grid-template-columns: 1fr !important;
        }}
        /* HTML tables scroll horizontally */
        table {{ display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }}
    }}

    /* ── RESPONSIVE: phones ── */
    @media (max-width: 480px) {{
        .block-container {{ padding: 0.8rem 0.6rem !important; }}
        h1 {{ font-size: 1.2rem !important; }}
        .kpi-number {{ font-size: 2.2rem !important; }}
        .hero-number {{ font-size: 1.6rem !important; }}
        .survey-pct {{ font-size: 1.3rem !important; }}
        .kpi-label {{ font-size: 0.85rem !important; }}
        div[style*="display:flex"][style*="gap:2rem"] {{
            flex-direction: column !important;
            gap: 0.8rem !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_survey():
    df = pd.read_excel("disssurvey (Responses).xlsx")
    df.columns = ['timestamp','age','gender','technical','tool_choice','correctability','fairness_type','responsibility','consent_use','human_involvement','data_consent','trust']
    return df

survey = load_survey()
total_responses = len(survey)
tool_a_pct = round((survey['tool_choice'] == 'Tool A \u2014 equal performance across groups').sum() / total_responses * 100)
challenge_pct = round((survey['correctability'] == 'Yes \u2014 patients should always have the right to challenge a decision about their health').sum() / total_responses * 100)
consent_pct = round((survey['consent_use'] == 'Yes \u2014 patients have a right to know').sum() / total_responses * 100)
human_pct = round((survey['human_involvement'] == 'Yes \u2014 human involvement is essential regardless of accuracy').sum() / total_responses * 100)
data_consent_pct = round((survey['data_consent'] == 'Yes \u2014 patients should always be informed how their data is used').sum() / total_responses * 100)
trust_pct = round((survey['trust'] == 'I trust them somewhat \u2014 but there should always be human oversight').sum() / total_responses * 100)
same_rules_pct = round((survey['fairness_type'] == 'Using the same rules for every patient, no matter who they are').sum() / total_responses * 100)
equal_outcomes_pct = round((survey['fairness_type'] == 'Making sure the AI is equally accurate for all groups of patients').sum() / total_responses * 100)
non_technical_pct = round((survey['technical'] == "No, I work or study in another field / I'm a student in a non-technical subject").sum() / total_responses * 100)
female_pct = round((survey['gender'] == 'Female').sum() / total_responses * 100)

criteria = {
    "Accuracy": {
        "purpose": "Predictions should be reliable and minimise diagnostic errors.",
        "baseline": "PASS", "mitigated": "PASS",
        "baseline_finding": "Overall accuracy (84.2%) met the 80% clinical <span class='tooltip'>threshold<span class='tooltiptext'>Minimum accuracy of 80%. Selected based on clinical machine learning literature reporting acceptable performance levels for healthcare prediction models (Liu et al., 2025; Simon and Aliferis, 2024).</span></span>. However, aggregate accuracy alone can hide differences between patient groups. As shown in the Bias Suppression assessment, performance was lower for female patients.",
        "mitigated_finding": "Overall accuracy decreased slightly from 84.2% to 80.4%, remaining above the 80% clinical <span class='tooltip'>threshold<span class='tooltiptext'>Minimum accuracy of 80%. Selected based on clinical machine learning literature reporting acceptable performance levels for healthcare prediction models (Liu et al., 2025; Simon and Aliferis, 2024).</span></span>. This reduction was a deliberate tradeoff to improve fairness across patient groups.",
        "metrics": "Overall accuracy, AUC-ROC, precision, recall, F1-score"
    },
    "Bias Suppression": {
        "purpose": "The tool should not be less accurate for some patient groups than others.",
        "baseline": "FAIL", "mitigated": "PARTIAL",
        "baseline_finding": "Female patients were identified with heart disease at a much lower rate (62.5%) than male patients (82.8%). Both fairness measures exceeded the <span class='tooltip'>threshold<span class='tooltiptext'>Fairness disparity measures should remain within \u00b10.10. This follows commonly used fairness evaluation conventions, where differences above 0.10 may indicate meaningful group disparities (Fairlearn, 2024).</span></span>: demographic parity difference was 0.264 and equalised odds difference was 0.203.",
        "mitigated_finding": "After mitigation, female recall improved to 87.5% and male recall decreased to 76.8%. Demographic parity difference reduced to 0.041, now within the <span class='tooltip'>threshold<span class='tooltiptext'>Fairness disparity measures should remain within \u00b10.10. This follows commonly used fairness evaluation conventions, where differences above 0.10 may indicate meaningful group disparities (Fairlearn, 2024).</span></span>. Equalised odds difference remained at 0.212, partly due to limited female test set size (n=27).",
        "metrics": "Demographic parity difference, equalised odds difference, group-level recall"
    },
    "Representativeness": {
        "purpose": "Training data must reflect the full range of patients the tool will be used on.",
        "baseline": "FAIL", "mitigated": "FAIL",
        "baseline_finding": "Female patients made up 21.0% of the dataset compared to 33.0% in real-world CHD admissions (BHF, 2021), below the <span class='tooltip'>threshold<span class='tooltiptext'>Representation ratio \u22650.80. This threshold was adapted from the four-fifths rule commonly used in algorithmic fairness assessment (Fairlearn, 2024), applied here to compare dataset demographics against real-world disease prevalence (BHF, 2021).</span></span> (ratio 0.64). Age distribution also skews younger than real-world CHD prevalence.",
        "mitigated_finding": "Unchanged. Algorithmic mitigation cannot fix data composition. Improving representativeness requires collecting more diverse clinical data.",
        "metrics": "Representation ratio (dataset proportion / real-world proportion)"
    },
    "Consistency": {
        "purpose": "The tool must make stable, predictable decisions for similar patients.",
        "baseline": "FAIL", "mitigated": "FAIL",
        "baseline_finding": "When small variations were applied to patient data, 8.7% of predictions changed, exceeding the 5% <span class='tooltip'>threshold<span class='tooltiptext'>5% instability threshold, set as a conservative benchmark for clinical decision support. No established standard exists for this type of prediction stability testing; this threshold was defined by the researcher.</span></span>. Instability was highest for under-45 patients (15.9%).",
        "mitigated_finding": "Unchanged. Consistency improvements require more representative training data so the model has stronger confidence across all patient groups.",
        "metrics": "Percentage of predictions that change under minor input perturbation"
    },
    "Correctability": {
        "purpose": "There must be a way to review, challenge, and correct the tool's decisions.",
        "baseline": "FAIL", "mitigated": "PARTIAL",
        "baseline_finding": "Met 3 of 7 checklist criteria, below the 80% pass <span class='tooltip'>threshold<span class='tooltiptext'>An 80% checklist completion threshold was defined by the researcher as an operational benchmark for sufficient coverage of correctability criteria. This threshold was selected to indicate that the majority of required governance and accountability mechanisms were present while allowing for minor gaps.</span></span>. The pipeline lacked clinician override, patient challenge mechanism, audit trail, and model version history. The dashboard partially addresses this through transparent communication of predictions and uncertainty.",
        "mitigated_finding": "Confidence-based flagging was added: predictions with less than 70% model confidence are flagged for clinician review (20.1% of test cases). Met 4 of 8 criteria, still below the 80% pass <span class='tooltip'>threshold<span class='tooltiptext'>An 80% checklist completion threshold was defined by the researcher as an operational benchmark for sufficient coverage of correctability criteria. This threshold was selected to indicate that the majority of required governance and accountability mechanisms were present while allowing for minor gaps.</span></span>.",
        "metrics": "Proportion of correctability checklist criteria met (qualitative assessment)"
    },
    "Ethicality": {
        "purpose": "The tool must meet ethical and legal standards and respect patient rights.",
        "baseline": "PASS", "mitigated": "PASS",
        "baseline_finding": "Met 7 of 8 checklist criteria (87.5%), above the 80% <span class='tooltip'>threshold<span class='tooltiptext'>An 80% checklist completion threshold was defined by the researcher as an operational benchmark for sufficient coverage of ethicality criteria. This threshold was selected to indicate that the majority of required ethical and legal standards were met while allowing for minor gaps.</span></span>. The one gap: consent practices for secondary ML use were not available within the dataset documentation.",
        "mitigated_finding": "Unchanged. The informed consent limitation is inherent to retrospective clinical datasets.",
        "metrics": "Proportion of ethicality checklist criteria met (qualitative assessment)"
    }
}

def badge(result):
    cls = {"PASS": "pass", "FAIL": "fail", "PARTIAL": "partial"}[result]
    return f"<span class='badge {cls}-badge'>{result}</span>"

def tt(label, explanation):
    return f"<span class='tooltip'>{label}<span class='tooltiptext'>{explanation}</span></span>"

tabs = st.tabs(["Overview", "Fairness Assessment", "Survey", "Discussion"])

# ══════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("<h1>Evaluating Procedural Fairness in Healthcare AI</h1>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='method-box'>
        <strong>About This Dashboard</strong><br><br>
        <strong>What is this?</strong> A fairness assessment of a heart disease prediction tool,
        evaluating whether it meets six procedural fairness criteria.<br><br>
        <strong>What was evaluated?</strong> A logistic regression classifier trained on 918 patient
        records from the UCI Heart Disease dataset, assessed against six criteria based on
        Leventhal's (1980) procedural justice framework.<br><br>
        <strong>What am I looking at?</strong> Results from the pipeline evaluation and a
        public survey (n=325), presented across four tabs.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div class='card' style='text-align:center; padding:2rem;'>
            <div class='kpi-label'>Fairness Criteria Met</div>
            <div class='kpi-number'>2 of 6</div>
            <div style='font-size:0.82rem; color:#666; margin-top:0.3rem;'>2 PASS · 4 FAIL</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card' style='padding:1.5rem 2rem;'>
            <div class='kpi-label' style='margin-bottom:0.8rem;'><span class='tooltip'>Recall<span class='tooltiptext'>Recall measures the percentage of patients who actually had heart disease that the model correctly identified. It is calculated as True Positives ÷ (True Positives + False Negatives). In healthcare, high recall is critical because a missed case (false negative) means a sick patient goes undetected.</span></span> by Sex (Heart Disease Present Class)</div>
            <div style='display:flex; gap:2rem; align-items:center;'>
                <div>
                    <span style='font-size:2.5rem; font-weight:700; color:{FAIL_COLOR};'>62.5%</span>
                    <div style='font-size:0.85rem; color:#666; margin-top:0.2rem;'>Female patients</div>
                </div>
                <div style='font-size:1.5rem; color:#ccc;'>vs</div>
                <div>
                    <span style='font-size:2.5rem; font-weight:700; color:{PASS_COLOR};'>82.8%</span>
                    <div style='font-size:0.85rem; color:#666; margin-top:0.2rem;'>Male patients</div>
                </div>
            </div>
            <div style='margin-top:1rem; font-size:0.88rem; color:#555; padding-top:0.8rem; border-top:1px solid #eee;'>
                The model identified heart disease less reliably in female patients.
                Their underrepresentation in the training data (21.0% of records) may have contributed to this disparity.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Procedural Fairness Criteria at a Glance")
    st.markdown(f"""<div style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>
        Definitions adapted from Leventhal's (1980) procedural justice rules for healthcare
        automated decision-making, following the approach of Jabagi et al. (2025).
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, (name, data) in enumerate(criteria.items()):
        result = data["baseline"]
        cls = {"PASS": "pass", "FAIL": "fail", "PARTIAL": "partial"}[result]
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div class='card {cls}-card' style='margin-bottom:0.6rem;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span class='rule-name'>{name}</span>
                    {badge(result)}
                </div>
                <div class='rule-desc'>{data['purpose']}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2: PROCEDURAL FAIRNESS ASSESSMENT
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("<h1>Procedural Fairness Assessment</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Detailed evaluation of each criterion with technical results</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card' style='background:#fff0f3; border-left:4px solid {PRIMARY}; margin-bottom:1.5rem;'>
        <strong>Framework</strong><br><br>
        This assessment evaluates the model against six procedural fairness criteria based on
        Leventhal's (1980) procedural justice framework, adapted for healthcare automated
        decision-making following Jabagi et al. (2025). Technical criteria were assessed using
        quantitative metrics; sociotechnical criteria were evaluated using structured qualitative checklists.
    </div>
    """, unsafe_allow_html=True)

    show_mit = st.toggle("View post-mitigation results", value=False, key="assessment_toggle",
        help="Compare the baseline model against the model after bias mitigation and confidence-based flagging were applied.")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    for name, data in criteria.items():
        result = data["mitigated"] if show_mit else data["baseline"]
        finding = data["mitigated_finding"] if show_mit else data["baseline_finding"]
        cls = {"PASS": "pass", "FAIL": "fail", "PARTIAL": "partial"}[result]

        st.markdown(f"""
        <div class='card {cls}-card' style='margin-bottom:0.3rem;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span class='rule-name'>{name}</span>
                {badge(result)}
            </div>
            <div style='margin-top:0.6rem; font-size:0.88rem; color:#444;'>{finding}</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander(f"Purpose and metrics: {name}"):
            st.markdown(f"**Purpose:** {data['purpose']}")
            st.markdown(f"**Metrics:** {data['metrics']}")
            if name == "Correctability":
                if show_mit:
                    checklist = [
                        ("Prediction outputs are visible and interpretable", True),
                        ("Confidence scores are provided with predictions", True),
                        ("Low confidence predictions flagged for human review", True),
                        ("Clinician override mechanism exists", False),
                        ("Patient challenge mechanism exists", False),
                        ("Audit trail of predictions is maintained", False),
                        ("Model version history is recorded", False),
                        ("Dashboard communicates uncertainty to stakeholders", True),
                    ]
                    st.markdown("**Checklist (post-mitigation): 4 of 8 met**")
                else:
                    checklist = [
                        ("Prediction outputs are visible and interpretable", True),
                        ("Confidence scores are provided with predictions", True),
                        ("Clinician override mechanism exists", False),
                        ("Patient challenge mechanism exists", False),
                        ("Audit trail of predictions is maintained", False),
                        ("Model version history is recorded", False),
                        ("Dashboard communicates uncertainty to stakeholders", True),
                    ]
                    st.markdown("**Checklist (baseline): 3 of 7 met**")
                for item, passed in checklist:
                    icon = "✅" if passed else "❌"
                    st.markdown(f"{icon} {item}")
            elif name == "Ethicality":
                checklist = [
                    ("Ethics approval granted by Newcastle University", True),
                    ("Dataset is fully anonymised — no patient identifiers", True),
                    ("No personal data collected or processed", True),
                    ("GDPR compliance — survey is anonymous", True),
                    ("Dataset used within its intended research purpose", True),
                    ("Patients gave informed consent for ML research use", False),
                    ("System designed to avoid unjust harm to patients", True),
                    ("Findings communicated transparently via dashboard", True),
                ]
                st.markdown("**Checklist: 7 of 8 met**")
                for item, passed in checklist:
                    icon = "✅" if passed else "❌"
                    st.markdown(f"{icon} {item}")


    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Fairness Mitigation Strategies Applied")
    st.markdown(f"""
    <div class='card' style='border-left:4px solid {PRIMARY}; background:#fff0f3; margin-bottom:1.2rem;'>
        <div style='font-size:0.9rem; color:#444; line-height:1.6;'>
            Two interventions were applied to address limitations identified in the baseline assessment:
            (1) a fairness-aware training approach to reduce demographic disparities, and
            (2) a confidence-based flagging mechanism to introduce additional human oversight for uncertain predictions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 1. BIAS SUPPRESSION MITIGATION ──
    st.markdown("### 1. Bias Suppression Mitigation")
    st.markdown(f"""
    <div class='card' style='border-left:4px solid {PASS_COLOR};'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;'>
            <span class='rule-name'>Bias Suppression</span>
            <span class='badge partial-badge'>PARTIAL</span>
        </div>
        <div style='font-size:0.82rem; font-weight:600; color:{PRIMARY}; text-transform:uppercase; margin-bottom:0.5rem;'>Intervention: Fairness-Aware Training</div>
        <div style='font-size:0.86rem; color:#444; line-height:1.5; margin-bottom:0.6rem;'>
            An ExponentiatedGradient algorithm with an EqualizedOdds constraint was applied during
            model training to reduce differences in performance between demographic groups.
        </div>
        <div style='font-size:0.82rem; color:#555; padding-top:0.5rem; border-top:1px solid #eee; line-height:1.5;'>
            <strong>Why:</strong> The baseline model identified heart disease in female patients at a
            much lower rate (62.5%) than male patients (82.8%). This intervention aimed to reduce
            that disparity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Recall by Sex: Baseline vs Post-Mitigation")
    st.caption("Recall measures the percentage of actual heart disease cases the tool correctly identified.")

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Male', x=['Baseline model','Post-mitigation model'], y=[82.8,76.8], marker_color=PRIMARY, text=['82.8%','76.8%'], textposition='outside', width=0.3))
    fig.add_trace(go.Bar(name='Female', x=['Baseline model','Post-mitigation model'], y=[62.5,87.5], marker_color=LIGHT, text=['62.5%','87.5%'], textposition='outside', width=0.3))
    fig.add_hline(y=80, line_dash="dot", line_color="#999", annotation_text="80% clinical threshold", annotation_position="bottom right")
    fig.update_layout(barmode='group', yaxis=dict(range=[0,105], showgrid=False, showticklabels=False), xaxis=dict(showgrid=False), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', y=1.1), margin=dict(t=20,b=20,l=0,r=120), font=dict(color=DARK, size=13), height=350)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='card pass-card'>
            <div style='font-size:0.85rem; font-weight:600; color:#555; text-transform:uppercase; margin-bottom:0.2rem;'>Demographic Parity Difference  ✅ Improved</div>
            <div style='color:{PASS_COLOR}; font-size:2rem; font-weight:700; line-height:1.2; margin:0.4rem 0;'>0.264 → 0.041</div>
            <div style='font-size:0.86rem; color:#444;'>The difference in positive prediction rates between male and female patients decreased and is now within the predefined ±0.10 <span class='tooltip'>threshold<span class='tooltiptext'>Fairness disparity measures should remain within ±0.10. This follows commonly used fairness evaluation conventions, where differences above 0.10 may indicate meaningful group disparities (Fairlearn, 2024).</span></span>.</div>
            <div style='font-size:0.82rem; color:#666; margin-top:0.4rem;'>Measures whether the model flags patients across groups at similar rates.</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card partial-card'>
            <div style='font-size:0.85rem; font-weight:600; color:#555; text-transform:uppercase; margin-bottom:0.2rem;'>Equalised Odds Difference  ⚠️ Above Threshold</div>
            <div style='color:{PARTIAL_COLOR}; font-size:2rem; font-weight:700; line-height:1.2; margin:0.4rem 0;'>0.203 → 0.212</div>
            <div style='font-size:0.86rem; color:#444;'>The difference in error rates between male and female patients remained above the ±0.10 <span class='tooltip'>threshold<span class='tooltiptext'>Fairness disparity measures should remain within ±0.10. This follows commonly used fairness evaluation conventions, where differences above 0.10 may indicate meaningful group disparities (Fairlearn, 2024).</span></span> after mitigation.</div>
            <div style='font-size:0.82rem; color:#666; margin-top:0.4rem;'>This may be influenced by the small number of female patients in the test set (n=27), which limits the reliability of this measure.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 2. CORRECTABILITY MITIGATION ──
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### 2. Correctability Mitigation")
    st.markdown(f"""
    <div class='card' style='border-left:4px solid {PARTIAL_COLOR};'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;'>
            <span class='rule-name'>Correctability</span>
            <span class='badge partial-badge'>PARTIAL</span>
        </div>
        <div style='font-size:0.82rem; font-weight:600; color:{PRIMARY}; text-transform:uppercase; margin-bottom:0.5rem;'>Intervention: Confidence-Based Flagging</div>
        <div style='font-size:0.86rem; color:#444; line-height:1.5; margin-bottom:0.6rem;'>
            Predictions with model confidence below 70% are automatically flagged for clinician review,
            creating an opportunity for human oversight before decisions are finalised.
        </div>
        <div style='font-size:0.82rem; color:#555; padding-top:0.5rem; border-top:1px solid #eee; line-height:1.5;'>
            <strong>Why:</strong> The baseline pipeline met only 3 of 7 correctability criteria and lacked
            mechanisms for human review of uncertain predictions. This intervention partially addresses
            that gap (now 4 of 8 criteria met).
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Overall flagged", "20.1%")
    with col2: st.metric("Male patients flagged", "19.1%")
    with col3: st.metric("Female patients flagged", "25.9%")

    st.markdown("""<div style='font-size:0.86rem; color:#555; margin-top:0.3rem;'>
        <strong>Finding:</strong> Female patients were flagged for review more frequently than male patients,
        suggesting greater uncertainty in predictions for this group. This may be related to differences in training data representation.
    </div>""", unsafe_allow_html=True)

    # ── OVERALL OUTCOME ──
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### Overall Outcome")
    st.markdown(f"""
    <div class='card' style='border-left:4px solid {PRIMARY}; background:#fff0f3;'>
        <div style='font-size:0.92rem; color:#444; line-height:1.6;'>
            The mitigation strategy improved procedural fairness by reducing disparities between
            demographic groups and introducing a mechanism for clinician oversight. However, fairness
            was not fully achieved, as limitations in dataset representativeness and model consistency remained.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 3: PUBLIC SURVEY
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("<h1>Public Survey Results</h1>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.95rem; color:#555; margin-top:0.3rem; margin-bottom:1rem;'>
        This survey explored public perceptions of fairness in healthcare AI. Responses were
        mapped to Leventhal's (1980) six procedural fairness criteria.
    </div>""", unsafe_allow_html=True)

    with st.expander("Survey Methodology"):
        st.markdown(f"""
**Distribution:** The survey used a snowball sampling approach. It was posted on social media
platforms with a request for respondents to share it further, and physical QR codes were printed
and placed in publicly accessible locations including the School of Computing building and
student accommodation at Newcastle University.

**Collection:** Responses were collected via Google Forms. Participation was voluntary and anonymous.
No personally identifiable information was collected. The survey was approved by Newcastle University's
ethics board prior to distribution.

**Sample:** {total_responses} responses. Predominantly female ({female_pct}%) and non-technical ({non_technical_pct}%). Conducted exclusively in English.

**Limitations:** Convenience sampling with potential self-selection bias. The gender skew toward
female respondents ({female_pct}%) and English-only distribution may limit the generalisability of findings.
        """)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f"<div class='survey-stat'><div class='survey-pct'>325</div><div class='survey-label'>Total responses</div></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='survey-stat'><div class='survey-pct'>{female_pct}%</div><div class='survey-label'>Female</div></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='survey-stat'><div class='survey-pct'>{non_technical_pct}%</div><div class='survey-label'>Non-technical</div></div>", unsafe_allow_html=True)
    with col4: st.markdown(f"<div class='survey-stat'><div class='survey-pct'>4</div><div class='survey-label'>Age groups</div></div>", unsafe_allow_html=True)

    st.markdown("""<div style='color:#999; font-size:0.78rem; text-align:center; padding:0.5rem 0;'>Age: 41–60 (29.2%) · Under 25 (28.3%) · Over 60 (22.8%) · 25–40 (19.7%)</div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Strongest Public Priorities: Human Oversight and Transparency")

    st.markdown(f"""
    <div class='tier-section'>
        <div class='rule-label'>Correctability</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;'>
            <div><div class='hero-number'>{challenge_pct}%</div><div class='hero-desc'>chose the option supporting patients' right to request a human review of an AI decision, even at cost or delay</div></div>
            <div><div class='hero-number'>{human_pct}%</div><div class='hero-desc'>chose the option supporting human doctor involvement in medical decisions, regardless of AI accuracy</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='tier-section'>
        <div class='rule-label'>Ethicality</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;'>
            <div><div class='hero-number'>{consent_pct}%</div><div class='hero-desc'>chose the option supporting patients being informed when an AI tool is used in their care</div></div>
            <div><div class='hero-number'>{data_consent_pct}%</div><div class='hero-desc'>chose the option supporting patients being informed when their records are used to train AI, even if anonymised</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Moderate Agreement: Equal Performance Across Groups")
    st.markdown(f"""
    <div class='tier-section'>
        <div class='rule-label'>Bias Suppression / Representativeness</div>
        <div style='display:grid; grid-template-columns:auto 1fr; gap:1.5rem; align-items:center;'>
            <div><div style='font-size:2.2rem; font-weight:700; color:{DARK};'>{tool_a_pct}%</div><div class='hero-desc'>chose equal performance across all patient groups over higher overall accuracy</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Mixed Views: Consistency")
    st.markdown(f"""
    <div class='tier-section'>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;'>
            <div><div style='font-size:2.2rem; font-weight:700; color:{DARK};'>{same_rules_pct}%</div><div class='hero-desc'>favoured applying the same rules to every patient regardless of outcome</div></div>
            <div><div style='font-size:2.2rem; font-weight:700; color:{DARK};'>{equal_outcomes_pct}%</div><div class='hero-desc'>prioritised equal accuracy across all patient groups over uniform rules</div></div>
        </div>
        <div style='font-size:0.82rem; color:#666; margin-top:1rem; padding-top:0.8rem; border-top:1px solid #eee;'>The majority leaned toward outcome-based fairness rather than procedural consistency.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Additional Context: Trust in AI")
    st.markdown(f"""
    <div class='tier-section'>
        <div style='display:grid; grid-template-columns:auto 1fr; gap:1.5rem; align-items:center;'>
            <div><div style='font-size:2.2rem; font-weight:700; color:{DARK};'>{trust_pct}%</div></div>
            <div>
                <div class='hero-desc'>reported some level of trust in healthcare AI but believed human oversight should always remain.</div>
                <div style='font-size:0.78rem; color:#888; margin-top:0.4rem; font-style:italic;'>This finding provides context on public expectations of AI reliability and oversight but does not directly measure accuracy as a fairness criterion.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style='font-size:0.82rem; color:#888; font-style:italic; margin-top:1rem;'>
        Note: Accuracy was assessed computationally through the ML pipeline. The survey did not
        include a question designed to isolate public perceptions of accuracy as a procedural fairness criterion.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    with st.expander("See all survey questions and full response distributions"):
        questions = [
            ('tool_choice', 'Which AI tool should the hospital use?', ['Tool A — equal performance across groups', 'Tool B — higher overall accuracy', "I'm not sure"]),
            ('correctability', 'Should patients have the right to request human review?', ['Yes — patients should always have the right to challenge a decision about their health', 'Only if the patient has a specific reason to doubt the result', 'No — if the tool is correct most of the time, human reviews are an unnecessary cost']),
            ('fairness_type', 'When it comes to fairness in medical AI, which is more important?', ['Making sure the AI is equally accurate for all groups of patients', 'Using the same rules for every patient, no matter who they are', 'I am not sure']),
            ('responsibility', 'Who should be held responsible when AI makes a wrong diagnosis?', ['All of the above', 'No one — AI errors are unavoidable', 'The doctor who relied on it', "I'm not sure", 'The hospital that used the tool', 'The company that built the tool']),
            ('consent_use', 'Should patients be told when AI is used in their care?', ['Yes — patients have a right to know', "No — it doesn't matter how the decision is made as long as it's accurate", 'Only if the patient asks']),
            ('human_involvement', 'Should a human doctor always be involved?', ['Yes — human involvement is essential regardless of accuracy', 'No — accuracy should be the priority', "I'm not sure"]),
            ('data_consent', 'Should patients be informed when their data trains AI?', ['Yes — patients should always be informed how their data is used', 'Only if there is a chance they could be identified from the data', 'No — anonymised data can be used freely for medical research']),
            ('trust', 'How much do you trust AI in healthcare?', ['I trust them somewhat — but there should always be human oversight', "I don't trust them — medical decisions should be made by humans only", "I'm not sure", 'I trust them fully — AI is more objective than humans']),
        ]
        for col_name, title, main_options in questions:
            counts = survey[col_name].value_counts()
            filtered = counts[counts.index.isin(main_options)]
            other = counts[~counts.index.isin(main_options)].sum()
            if other > 0: filtered['Other responses'] = other
            pcts = (filtered / total_responses * 100).round(0).astype(int)
            fig = go.Figure(go.Bar(x=pcts.values, y=pcts.index, orientation='h', marker_color=PRIMARY, text=[f"{v}%" for v in pcts.values], textposition='outside'))
            fig.update_layout(title=dict(text=title, font=dict(size=12)), xaxis=dict(showgrid=False, showticklabels=False, range=[0,115]), yaxis=dict(showgrid=False, autorange='reversed'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=35,b=10,l=0,r=60), height=max(160, len(filtered)*45), font=dict(color=DARK, size=11))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ══════════════════════════════════════════════════════════════
# TAB 4: DISCUSSION AND RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("<h1>Discussion and Recommendations</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Integrating technical findings and public expectations to identify priorities for responsible deployment</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card' style='background:#fff0f3; border-left:4px solid {PRIMARY}; margin-bottom:1.5rem;'>
        This tab brings together findings from two independent evidence sources. The pipeline evaluates
        the technical and procedural fairness of the model, while the public survey explores expectations
        of fairness in healthcare AI. Where findings are discussed together, this represents a comparison
        of perspectives rather than a direct validation between sources.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Key Pipeline Findings")
    pipeline_rows = [
        ("Accuracy", "Overall accuracy met the clinical threshold, but aggregate performance masked lower recall for female patients."),
        ("Bias Suppression", "Bias mitigation substantially reduced disparities between male and female patients, although equalised odds remained above the predefined threshold."),
        ("Representativeness", "Female patients and younger age groups were underrepresented compared with real-world disease prevalence."),
        ("Consistency", "Predictions changed under small input perturbations, with instability highest among younger patients."),
        ("Correctability", "The pipeline lacked key correctability mechanisms. Confidence-based flagging was introduced to partially address this, improving criteria met from 3 of 7 to 4 of 8."),
        ("Ethicality", "Most ethical criteria were satisfied, but consent practices for secondary ML use were not documented."),
    ]
    pipeline_html = f"""
    <table style='width:100%; border-collapse:collapse; font-size:0.88rem;'>
        <thead><tr style='border-bottom:2px solid #ddd;'>
            <th style='text-align:left; padding:0.6rem 0.8rem; color:{DARK}; width:160px;'>Criterion</th>
            <th style='text-align:left; padding:0.6rem 0.8rem; color:{DARK};'>Finding</th>
        </tr></thead>
        <tbody>{"".join(f"<tr style='border-bottom:1px solid #eee;'><td style='padding:0.6rem 0.8rem; font-weight:600; vertical-align:top; color:{DARK};'>{c}</td><td style='padding:0.6rem 0.8rem; color:#444; line-height:1.5;'>{f}</td></tr>" for c, f in pipeline_rows)}</tbody>
    </table>"""
    st.markdown(pipeline_html, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Key Public Survey Findings")
    survey_rows = [
        ("Human Oversight (Correctability)", f"{challenge_pct}% supported patients' right to challenge AI decisions; {human_pct}% supported human doctor involvement regardless of AI accuracy."),
        ("Transparency (Ethicality)", f"{consent_pct}% supported informing patients when AI is used; {data_consent_pct}% supported informed consent when patient data is used for AI training."),
        ("Equal Performance (Bias Suppression / Representativeness)", f"{tool_a_pct}% preferred equal performance across patient groups over higher overall accuracy."),
        ("Fairness Expectations (Consistency)", f"{equal_outcomes_pct}% prioritised equal outcomes across groups, while {same_rules_pct}% favoured applying the same rules to all patients."),
        ("Trust in AI (Contextual)", f"{trust_pct}% reported some level of trust in AI but believed human oversight should remain. Accuracy was not directly assessed."),
    ]
    survey_html = f"""
    <table style='width:100%; border-collapse:collapse; font-size:0.88rem;'>
        <thead><tr style='border-bottom:2px solid #ddd;'>
            <th style='text-align:left; padding:0.6rem 0.8rem; color:{DARK}; width:200px;'>Theme</th>
            <th style='text-align:left; padding:0.6rem 0.8rem; color:{DARK};'>Finding</th>
        </tr></thead>
        <tbody>{"".join(f"<tr style='border-bottom:1px solid #eee;'><td style='padding:0.6rem 0.8rem; font-weight:600; vertical-align:top; color:{DARK};'>{t}</td><td style='padding:0.6rem 0.8rem; color:#444; line-height:1.5;'>{f}</td></tr>" for t, f in survey_rows)}</tbody>
    </table>"""
    st.markdown(survey_html, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Impact of Mitigation Strategies")
    st.markdown("""<div style='font-size:0.88rem; color:#555; margin-bottom:1rem;'>
        The following section summarises the outcomes of the mitigation strategies evaluated in the pipeline.
        Survey findings are included separately to provide context on related public expectations.
    </div>""", unsafe_allow_html=True)

    RECALL_TT = tt("Recall", "The percentage of patients who actually had heart disease that the model correctly identified. Higher is better — a lower recall means more patients with the disease were missed.")
    DPD_TT = tt("Demographic parity difference", "Measures whether the model flags patients for heart disease at similar rates across groups. A value closer to 0 means the model treats groups more equally.")
    ACC_TT = tt("Overall accuracy", "The percentage of all predictions (both positive and negative) that the model got correct across all patients combined.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='card' style='border-left:4px solid {PASS_COLOR};'>
            <div style='font-weight:600; margin-bottom:0.6rem;'>Bias Mitigation</div>
            <div style='display:flex; gap:1.5rem; margin-bottom:0.6rem;'>
                <div style='text-align:center;'>
                    <div style='font-size:0.75rem; color:#888;'>Female {RECALL_TT}</div>
                    <div style='font-size:1.8rem; font-weight:700; color:{PASS_COLOR};'>62.5% → 87.5%</div>
                </div>
            </div>
            <div style='font-size:0.86rem; color:#444;'>
                {DPD_TT} reduced from 0.264 to 0.041. {ACC_TT} decreased from 84.2% to 80.4% — a deliberate tradeoff.
            </div>
            <div style='font-size:0.82rem; color:#888; margin-top:0.6rem; padding-top:0.4rem; border-top:1px solid #eee;'>
                <strong>Public perspective:</strong> Separately, survey responses indicated that respondents valued equal performance across groups over higher overall accuracy.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card' style='border-left:4px solid {PARTIAL_COLOR};'>
            <div style='font-weight:600; margin-bottom:0.6rem;'>Confidence-Based Flagging</div>
            <div style='display:flex; gap:1.5rem; margin-bottom:0.6rem;'>
                <div style='text-align:center;'>
                    <div style='font-size:0.75rem; color:#888;'>Predictions flagged</div>
                    <div style='font-size:1.8rem; font-weight:700; color:{PARTIAL_COLOR};'>20.1%</div>
                </div>
            </div>
            <div style='font-size:0.86rem; color:#444;'>
                Female patients flagged more frequently (25.9% vs 19.1%), suggesting greater model uncertainty for this group.
            </div>
            <div style='font-size:0.82rem; color:#888; margin-top:0.6rem; padding-top:0.4rem; border-top:1px solid #eee;'>
                <strong>Public perspective:</strong> Separately, the survey found strong support for human oversight and the right to challenge AI decisions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Priorities for Responsible Deployment")
    st.markdown(f"""<div style='font-size:0.88rem; color:#555; margin-bottom:1rem;'>
        These priorities address the limitations identified during the fairness assessment and focus
        on improving data quality, accountability, transparency, governance, and human oversight.
    </div>""", unsafe_allow_html=True)

    recs = [
        {"title": "Collect more representative clinical data", "addresses": "Representativeness, Consistency",
         "finding": "Dataset composition likely contributed to limitations in representativeness and consistency. Female patients represent 21.0% of the dataset vs 33.0% of real-world CHD prevalence (BHF, 2021). Under-45 patients showed 15.9% prediction instability.",
         "recommendation": "Future healthcare AI systems should prioritise more representative clinical datasets before deployment."},
        {"title": "Implement clinician override and patient challenge mechanisms", "addresses": "Correctability",
         "finding": "Only 4 of 8 correctability criteria were satisfied. Separately, most survey respondents supported human review and clinician involvement.",
         "recommendation": "Clinical AI systems should include clear mechanisms for clinician override, patient review requests, and accountability tracking."},
        {"title": "Establish prediction audit trails and model version control", "addresses": "Correctability",
         "finding": "Audit trail and model version history mechanisms were not available within the assessed pipeline.",
         "recommendation": "These mechanisms support accountability, monitoring, and retrospective review in clinical deployment."},
        {"title": "Address informed consent for retrospective data use", "addresses": "Ethicality",
         "finding": "Consent practices for secondary ML use were not available within the dataset documentation. Separately, most survey respondents indicated patients should be informed when their data is used to train AI.",
         "recommendation": "Future deployments should establish clear consent frameworks for the secondary use of clinical data in machine learning research."},
        {"title": "Improve fairness communication and stakeholder involvement", "addresses": "All criteria",
         "finding": "This dashboard is one approach to communicating fairness assessments to diverse stakeholders.",
         "recommendation": "Future work should evaluate whether fairness dashboards and explanations are understandable and useful for clinicians, patients, and policymakers."},
    ]

    for rec in recs:
        st.markdown(f"""
        <div class='rec-box'>
            <div style='font-weight:600; font-size:0.95rem; margin-bottom:0.3rem;'>{rec['title']}</div>
            <div style='font-size:0.78rem; color:{PRIMARY}; font-weight:600; margin-bottom:0.5rem;'>Addresses: {rec['addresses']}</div>
            <div style='font-size:0.84rem; color:#555; margin-bottom:0.4rem;'><strong>Finding:</strong> {rec['finding']}</div>
            <div style='font-size:0.86rem; color:#444; padding-top:0.4rem; border-top:1px solid #eee;'><strong>Recommendation:</strong> {rec['recommendation']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='card' style='border-left:4px solid {PRIMARY}; background:#fff0f3;'>
        <div style='font-size:0.95rem; color:#444; line-height:1.6;'>
            <strong>Overall conclusion:</strong> Responsible healthcare AI requires both technical evaluation
            of model behaviour and consideration of stakeholder expectations and values. Improving fairness requires
            not only model-level interventions, but also better data practices, human oversight, and
            transparent governance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""<div style='text-align:center; padding:2rem 0 1rem; color:#aaa; font-size:0.82rem;'>
        Procedural Fairness in Healthcare ADM · Kaylee Scarce · Newcastle University 2026 · Supervised by Dr Vlad González-Zelaya
    </div>""", unsafe_allow_html=True)
