import itertools
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

DATA_DIR = Path(__file__).parent.parent / "data"

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
    .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.02em; }}
    .pass-badge {{ background: {PASS_COLOR}; color: white; }}
    .fail-badge {{ background: {FAIL_COLOR}; color: white; }}
    .partial-badge {{ background: #6b5003; color: white; }}
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
    .pip-row {{ margin-top: 0.5rem; font-size: 1.1rem; letter-spacing: 0.15rem; }}
    .headline-metric {{ font-size: 2.4rem; font-weight: 700; line-height: 1.1; }}
    .headline-metric-label {{ font-size: 0.78rem; color: #5a5a5a; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 0.1rem; }}
    .spec-strip {{ display: flex; flex-wrap: wrap; gap: 0.6rem; margin: 0.4rem 0 0.2rem; }}
    .spec-item {{ background: #fbeef1; border-radius: 8px; padding: 0.5rem 0.9rem; font-size: 0.82rem; color: {DARK}; flex: 1 1 auto; min-width: 140px; }}
    .spec-item strong {{ display: block; font-size: 0.72rem; color: {RULE_LABEL}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.15rem; }}
    .spec-callout {{ background: {FAIL_BG}; border-left: 4px solid {FAIL_COLOR}; border-radius: 8px; padding: 0.6rem 1rem; font-size: 0.85rem; color: {DARK}; margin-top: 0.6rem; }}
    .spec-callout strong {{ color: {FAIL_COLOR}; }}
    .flow-row {{ display: flex; flex-wrap: wrap; align-items: stretch; gap: 0.4rem; margin: 0.6rem 0; }}
    .flow-step {{ background: white; border: 1px solid #f0d9df; border-left: 4px solid {PRIMARY}; border-radius: 8px; padding: 0.6rem 0.9rem; font-size: 0.82rem; flex: 1 1 0; min-width: 120px; text-align: center; display: flex; align-items: center; justify-content: center; }}
    .flow-arrow {{ display: flex; align-items: center; color: {PRIMARY}; font-size: 1.2rem; font-weight: 700; }}
    .legend-card {{ background: white; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.6rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-left: 4px solid {LIGHT}; }}
    .survey-hero {{ font-size: 2.2rem; font-weight: 700; color: {DARK}; line-height: 1.1; }}
    .rec-num {{ display:inline-flex; align-items:center; justify-content:center; width:1.6rem; height:1.6rem; border-radius:50%; background:{PRIMARY}; color:white !important; font-size:0.85rem; font-weight:700; flex-shrink:0; }}
    .rec-chip {{ display:inline-block; background:#fbeef1; color:{RULE_LABEL} !important; font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.03em; padding:0.15rem 0.6rem; border-radius:12px; }}
    .tooltip {{ position: relative; display: inline-block; }}
    .tooltip-toggle {{ position: absolute; opacity: 0; width: 1px; height: 1px; pointer-events: none; }}
    .tooltip-trigger {{ cursor: help; border-bottom: 1px dotted #888; outline: none; }}
    .tooltip-trigger:focus-visible {{ outline: 2px solid {PRIMARY}; outline-offset: 2px; border-radius: 2px; }}
    .tooltip .tooltiptext {{ visibility: hidden; width: 320px; background-color: #333; color: #fff;
        text-align: left; border-radius: 6px; padding: 8px 12px; position: absolute; z-index: 1;
        bottom: 125%; left: 50%; margin-left: -160px; font-size: 0.78rem; line-height: 1.4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2); }}
    .tooltip-trigger:hover ~ .tooltiptext,
    .tooltip-trigger:focus ~ .tooltiptext,
    .tooltip-toggle:checked ~ .tooltiptext {{ visibility: visible; }}

    /* ── THEME OVERRIDES: prevent dark mode from breaking colors ── */
    .stApp {{ background-color: {BG} !important; }}
    /* Hide Streamlit header, footer, and menu on mobile */
    #MainMenu, header[data-testid="stHeader"], footer {{
        display: none !important;
    }}
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
    /* Make tabs sticky so they don't disappear on mobile */
    .stTabs [data-baseweb="tab-list"] {{
        position: sticky !important;
        top: 0 !important;
        z-index: 999 !important;
        background-color: {BG} !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0.3rem !important;
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
    df = pd.read_excel(DATA_DIR / "disssurvey (Responses).xlsx")
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

# ── Centralised threshold provenance (single source of truth) ──
_tooltip_ids = itertools.count(1)

def tt(label, explanation):
    tid = f"tt-{next(_tooltip_ids)}"
    return (
        f"<span class='tooltip'>"
        f"<input type='checkbox' class='tooltip-toggle' id='{tid}'>"
        f"<label for='{tid}' class='tooltip-trigger' tabindex='0'>{label}</label>"
        f"<span class='tooltiptext'>{explanation}</span>"
        f"</span>"
    )

THRESH_AUC = "AUC-ROC of at least 0.80, commonly interpreted as showing good ability to distinguish between two outcomes (Mandrekar, 2010)."
THRESH_DISPARITY = "A disparity of no more than \u00b10.10 on both fairness measures, defined by the researcher as an operational benchmark since no single threshold is universally agreed in algorithmic fairness research."
THRESH_REPR = "A representation ratio of at least 0.80, adapted from the four-fifths principle used in fairness evaluation, comparing dataset composition against real-world CHD prevalence (British Heart Foundation, 2021)."
THRESH_CONSISTENCY = "An instability rate of no more than 5%, defined by the researcher as a conservative operational benchmark since no established clinical standard exists for this type of test."
THRESH_CHECKLIST_CORR = "At least 80% of correctability checklist criteria met, an operational benchmark defined by the researcher for sufficient governance and accountability coverage."
THRESH_CHECKLIST_ETH = "At least 80% of ethicality checklist criteria met, an operational benchmark defined by the researcher for sufficient ethical and legal coverage."
RECALL_EXPLANATION = "The percentage of patients who actually had heart disease that the model correctly identified (True Positives \u00f7 (True Positives + False Negatives)). High recall matters in healthcare because a missed case (false negative) means a sick patient goes undetected."
CONFIDENCE_BAND_EXPLANATION = "A very low score means the model is confident the patient does not have heart disease, and a very high score means it is confident they do. Scores in the middle are where the model is least certain, closest to a coin flip, so those are the ones a clinician should look at more closely."
FAIRNESS_TRAINING_EXPLANATION = "An ExponentiatedGradient algorithm was applied, constrained by Fairlearn's EqualizedOdds criterion, with a tolerance of 0.01 to balance fairness against predictive performance rather than forcing an exact match between groups. The same imputation, scaling, and logistic regression steps used in the baseline model were kept unchanged, so any difference in the result reflects the mitigation itself rather than a different underlying model."
SEED_ROBUSTNESS_EXPLANATION = "Repeating the test across 20 random seeds gave a mean instability of 0.03% (range 0.00% to 0.54%), confirming the result is not an artefact of a single perturbation draw. Only 2 of 184 test cases sat close to the decision boundary, which explains the high stability."

criteria = {
    "Accuracy": {
        "purpose": "Predictions should be reliable and minimise diagnostic errors.",
        "baseline": "PASS", "mitigated": "PASS",
        "headline": "0.957", "headline_label": "AUC-ROC",
        "mitigated_headline": "0.895", "mitigated_headline_label": "AUC-ROC",
        "baseline_finding": "AUC-ROC of 0.957 exceeded the 0.80 " + tt("threshold", THRESH_AUC) + ", indicating strong ability to distinguish between patients with and without heart disease. Overall accuracy was 89.1%. However, aggregate performance can hide differences between patient groups, and as shown in the Bias Suppression assessment, recall was lower for female patients.",
        "mitigated_finding": "After fairness-aware retraining, AUC-ROC decreased to 0.895 while overall accuracy remained stable at 89.7%. AUC-ROC remained above the 0.80 " + tt("threshold", THRESH_AUC) + ". The reduction in discrimination was a deliberate tradeoff to improve fairness across patient groups.",
        "metrics": "Overall accuracy, AUC-ROC, precision, recall, F1-score"
    },
    "Bias Suppression": {
        "purpose": "The tool should not be less accurate for some patient groups than others.",
        "baseline": "FAIL", "mitigated": "PARTIAL",
        "headline": "0.235 / 0.457", "headline_label": "Equalised odds / parity difference",
        "mitigated_headline": "0.120 / 0.380", "mitigated_headline_label": "Equalised odds / parity difference",
        "baseline_finding": "Female patients were identified with heart disease at a much lower rate (70.0%) than male patients (93.5%). Both fairness measures exceeded the " + tt("threshold", THRESH_DISPARITY) + ", with a demographic parity difference of 0.457 and an equalised odds difference of 0.235.",
        "mitigated_finding": "Partial improvement. Female recall rose from 70.0% to 90.0%, while male recall was unchanged at 93.5%. Both fairness measures improved, equalised odds difference from 0.235 to 0.120 and demographic parity difference from 0.457 to 0.380, but neither reached the ±0.10 acceptance " + tt("threshold", THRESH_DISPARITY) + ". The criterion is therefore classified as partial rather than passed. The small female test sample (n=39) limits the precision of these estimates.",
        "metrics": "Equalised odds difference, demographic parity difference, group-level recall"
    },
    "Representativeness": {
        "purpose": "Training data must reflect the full range of patients the tool will be used on.",
        "baseline": "FAIL", "mitigated": "FAIL",
        "headline": "0.64", "headline_label": "Representation ratio",
        "mitigated_headline": "0.64", "mitigated_headline_label": "Representation ratio",
        "baseline_finding": "Female patients made up 21.0% of the dataset compared to 33.0% in real-world CHD admissions (BHF, 2021), giving a representation ratio of 0.64, below the " + tt("threshold", THRESH_REPR) + ". The age distribution also skews younger than real-world CHD prevalence.",
        "mitigated_finding": "Unchanged, because algorithmic mitigation cannot fix data composition. Improving representativeness requires collecting more diverse clinical data.",
        "metrics": "Representation ratio (dataset proportion divided by real-world proportion)"
    },
    "Consistency": {
        "purpose": "The tool must make stable, predictable decisions for similar patients.",
        "baseline": "PASS", "mitigated": "PASS",
        "headline": "0.0%", "headline_label": "Predictions changed",
        "mitigated_headline": "1.1%", "mitigated_headline_label": "Predictions changed",
        "baseline_finding": "Small realistic changes were introduced to patient data to test whether predictions were stable. No predictions changed (0.0%), remaining well below the 5% " + tt("threshold", THRESH_CONSISTENCY) + ". Repeating the test across " + tt("multiple random variations", SEED_ROBUSTNESS_EXPLANATION) + " produced similarly stable results, suggesting the model's decisions were not sensitive to minor input changes.",
        "mitigated_finding": "After mitigation, 1.1% of predictions changed under the same perturbation test, still within the 5% " + tt("threshold", THRESH_CONSISTENCY) + ". The small increase reflects the randomised ensemble produced by the mitigation algorithm rather than a single decision boundary.",
        "metrics": "Percentage of predictions that change under minor input perturbation"
    },
    "Correctability": {
        "purpose": "There must be a way to review, challenge, and correct the tool's decisions.",
        "baseline": "FAIL", "mitigated": "PARTIAL",
        "headline": "3 of 7", "headline_label": "Governance criteria met",
        "mitigated_headline": "4 of 8", "mitigated_headline_label": "Governance criteria met",
        "baseline_finding": "Met 3 of 7 checklist criteria, below the 80% pass " + tt("threshold", THRESH_CHECKLIST_CORR) + ". The pipeline lacked a clinician override, a patient challenge mechanism, an audit trail, and model version history. The dashboard partially addresses this through transparent communication of predictions and uncertainty.",
        "mitigated_finding": "Confidence-based flagging was added, so predictions with model confidence between " + tt("30% and 70%", CONFIDENCE_BAND_EXPLANATION) + " are flagged for clinician review (10.3% of test cases), adding a new checklist item. Because the checklist total grew alongside it, the 80% pass " + tt("threshold", THRESH_CHECKLIST_CORR) + " became harder to reach rather than easier, so the criterion remains unmet.",
        "metrics": "Proportion of correctability checklist criteria met (qualitative assessment)"
    },
    "Ethicality": {
        "purpose": "The tool must meet ethical and legal standards and respect patient rights.",
        "baseline": "PASS", "mitigated": "PASS",
        "headline": "7 of 8", "headline_label": "Ethics criteria met",
        "mitigated_headline": "7 of 8", "mitigated_headline_label": "Ethics criteria met",
        "baseline_finding": "Met 7 of 8 checklist criteria (87.5%), above the 80% " + tt("threshold", THRESH_CHECKLIST_ETH) + ". The one gap was that consent practices for secondary ML use were not available within the dataset documentation.",
        "mitigated_finding": "Unchanged, as the informed consent limitation is inherent to retrospective clinical datasets.",
        "metrics": "Proportion of ethicality checklist criteria met (qualitative assessment)"
    }
}

def badge(result):
    cls = {"PASS": "pass", "FAIL": "fail", "PARTIAL": "partial"}[result]
    icon = {"PASS": "\u2713", "FAIL": "\u2715", "PARTIAL": "\u26a0"}[result]
    return f"<span class='badge {cls}-badge'>{icon} {result}</span>"

baseline_counts = {"PASS": 0, "FAIL": 0, "PARTIAL": 0}
mitigated_counts = {"PASS": 0, "FAIL": 0, "PARTIAL": 0}
for _c in criteria.values():
    baseline_counts[_c["baseline"]] += 1
    mitigated_counts[_c["mitigated"]] += 1

def dot_row(pass_n=0, partial_n=0, fail_n=0):
    pass_dots = "\u25cf" * pass_n
    partial_dots = "\u25cf" * partial_n
    fail_dots = "\u25cb" * fail_n
    html = ""
    if pass_n:
        html += f"<span style='color:{PASS_COLOR};'>{pass_dots}</span>"
    if partial_n:
        html += f"<span style='color:{PARTIAL_COLOR};'>{partial_dots}</span>"
    if fail_n:
        html += f"<span style='color:#d9b3bd;'>{fail_dots}</span>"
    return html

def spec_strip(extra_label=None, extra_value=None):
    extra_html = f"<div class='spec-item'><strong>{extra_label}</strong>{extra_value}</div>" if extra_label else ""
    return f"""
    <div class='spec-strip'>
        <div class='spec-item'><strong>Algorithm</strong>Logistic regression classifier</div>
        <div class='spec-item'><strong>Data</strong>UCI Heart Disease, 918 records</div>
        <div class='spec-item'><strong>Predicts</strong>Presence of heart disease</div>
        {extra_html}
    </div>
    """

tabs = st.tabs(["Overview", "Methodology", "Fairness Assessment", "Survey", "Discussion"])

# ══════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("<h1>Evaluating Procedural Fairness in Healthcare AI</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-size:1rem; color:{DARK}; line-height:1.7; margin:1rem 0 1.4rem;'>
        Artificial intelligence is increasingly being used to support medical decision-making,
        including predicting a patient's risk of heart disease. However, accuracy alone is not
        enough to make an AI system trustworthy. For healthcare AI to be responsible, it must
        also be fair across different groups of patients, transparent, and accountable when
        mistakes occur.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='method-box'>
        <strong>What am I looking at?</strong> Six rules for fair decision-making were defined
        specifically for healthcare. A model was built to predict heart disease. That model was
        tested against the six rules, and a public survey asked people what they expect from
        fairness in medical AI. The results are shown across five tabs.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div class='card' style='text-align:center; padding:2rem;'>
            <div class='kpi-label'>Fairness Criteria Met</div>
            <div class='kpi-number'>{baseline_counts['PASS']} of {len(criteria)}</div>
            <div class='pip-row'>{dot_row(pass_n=baseline_counts['PASS'], fail_n=baseline_counts['FAIL'])}</div>
            <div style='font-size:0.82rem; color:#5f5f5f; margin-top:0.3rem;'>{baseline_counts['PASS']} pass, {baseline_counts['FAIL']} fail (baseline)</div>
            <div style='font-size:0.78rem; color:#888; margin:0.7rem 0 0.2rem; text-transform:uppercase; letter-spacing:0.04em;'>After mitigation</div>
            <div class='pip-row'>{dot_row(pass_n=mitigated_counts['PASS'], partial_n=mitigated_counts['PARTIAL'], fail_n=mitigated_counts['FAIL'])}</div>
            <div style='font-size:0.82rem; color:#5f5f5f; margin-top:0.3rem;'>{mitigated_counts['PASS']} pass, {mitigated_counts['PARTIAL']} partial, {mitigated_counts['FAIL']} fail (after mitigation)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card' style='padding:1.5rem 2rem;'>
            <div class='kpi-label' style='margin-bottom:0.8rem;'>{tt("Recall", RECALL_EXPLANATION)} by Sex (Heart Disease Present Class)</div>
            <div style='display:flex; gap:2rem; align-items:center;'>
                <div>
                    <span style='font-size:2.5rem; font-weight:700; color:{FAIL_COLOR};'>70.0%</span>
                    <div style='font-size:0.85rem; color:#666; margin-top:0.2rem;'>Female patients (n=39)</div>
                </div>
                <div style='font-size:1.5rem; color:#ccc;'>vs</div>
                <div>
                    <span style='font-size:2.5rem; font-weight:700; color:{PASS_COLOR};'>93.5%</span>
                    <div style='font-size:0.85rem; color:#666; margin-top:0.2rem;'>Male patients (n=145)</div>
                </div>
            </div>
            <div style='margin-top:1rem; font-size:0.88rem; color:#555; padding-top:0.8rem; border-top:1px solid #eee;'>
                The model identified heart disease less reliably in female patients, likely linked to
                their 21.0% share of the training data.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='rule-label'>The Model</div>", unsafe_allow_html=True)
    st.markdown(spec_strip() + """
    <div class='spec-callout'><strong>Known limitation:</strong> only 21% of records are female.</div>
    """, unsafe_allow_html=True)
    st.markdown(f"""<div style='font-size:0.85rem; color:#666; margin-top:0.8rem;'>
        For the model's design rationale, how the six criteria are tested, and how each mitigation
        strategy works, see the <strong>Methodology</strong> tab.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## The Six Principles of Fair Decision-Making")
    st.markdown(f"""<div style='font-size:0.9rem; color:#5f5f5f; margin-bottom:1rem; line-height:1.6;'>
        This model is evaluated against six criteria. Here is what each one means. The results for
        each follow in the Fairness Assessment tab. Definitions are adapted from Leventhal's (1980)
        procedural justice rules for healthcare automated decision-making, following the approach of
        Jabagi et al. (2025).
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, (name, data) in enumerate(criteria.items()):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div class='legend-card'>
                <div style='display:flex; justify-content:space-between; align-items:center; gap:0.6rem;'>
                    <span class='rule-name'>{name}</span>
                    {badge(data['baseline'])}
                </div>
                <div class='rule-desc'>{data['purpose']}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2: METHODOLOGY
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("<h1>How This Was Tested</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>The data, model, and two-stage evaluation behind the fairness assessment</div>", unsafe_allow_html=True)

    st.markdown("<div class='rule-label' style='margin-top:1.2rem;'>The Model</div>", unsafe_allow_html=True)
    st.markdown(spec_strip("Train / test split", "734 / 184, stratified 80/20"), unsafe_allow_html=True)
    st.markdown(f"""
    <div class='method-box' style='margin-top:0.8rem;'>
        <strong>Why logistic regression?</strong> It shows how it reached its answer. That matters for
        the criteria that require reviewable decisions.<br><br>
        <strong>Why keep sex and age as inputs?</strong> Removing them would not stop the model
        picking up those patterns indirectly, through other related clinical measurements. Keeping
        them in means any such pattern can be measured directly, as it is in the Bias Suppression
        criterion.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='rule-label'>The Pipeline</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='flow-row'>
        <div class='flow-step'><div><strong>918 patient records</strong><br><span style='font-size:0.72rem; color:#666;'>UCI Heart Disease dataset</span></div></div>
        <div class='flow-arrow'>→</div>
        <div class='flow-step'><div><strong>734 train / 184 test</strong><br><span style='font-size:0.72rem; color:#666;'>stratified 80/20 split</span></div></div>
        <div class='flow-arrow'>→</div>
        <div class='flow-step'><div><strong>6 criteria tested</strong><br><span style='font-size:0.72rem; color:#666;'>against pre-set thresholds</span></div></div>
        <div class='flow-arrow'>→</div>
        <div class='flow-step'><div><strong>2 mitigations applied</strong><br><span style='font-size:0.72rem; color:#666;'>training + flagging</span></div></div>
        <div class='flow-arrow'>→</div>
        <div class='flow-step'><div><strong>Re-tested on all 6</strong><br><span style='font-size:0.72rem; color:#666;'>results in the next tab</span></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='rule-label'>The Six Criteria: What They Test and How</div>", unsafe_allow_html=True)
    method_rows = "".join(f"""
        <tr style='border-bottom:1px solid #f0e0e5;'>
            <td style='padding:0.6rem 0.7rem; font-weight:600; color:{DARK}; white-space:nowrap; vertical-align:top;'>{name}</td>
            <td style='padding:0.6rem 0.7rem; color:#444; vertical-align:top;'>{data['metrics']}</td>
        </tr>""" for name, data in criteria.items())
    st.markdown(f"""
    <div class='card'>
        <div style='overflow-x:auto;'>
        <table style='width:100%; border-collapse:collapse; font-size:0.85rem;'>
            <thead>
                <tr style='border-bottom:2px solid #e0c3cc;'>
                    <th style='text-align:left; padding:0.5rem 0.7rem; color:{DARK}; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.03em;'>Criterion</th>
                    <th style='text-align:left; padding:0.5rem 0.7rem; color:{DARK}; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.03em;'>How It's Measured</th>
                </tr>
            </thead>
            <tbody>{method_rows}</tbody>
        </table>
        </div>
        <div style='font-size:0.8rem; color:#666; margin-top:0.8rem; padding-top:0.6rem; border-top:1px solid #eee;'>
            For Bias Suppression, equalised odds was prioritised over demographic parity when judging
            pass/fail, because differences in false positive and false negative rates relate more
            directly to potential clinical harm, particularly the risk of missed diagnoses.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='rule-label'>The Two Mitigation Strategies</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='method-box'>
        <strong>1. Fairness-aware training (addresses Bias Suppression)</strong><br><br>
        A {tt("fairness-aware training method", FAIRNESS_TRAINING_EXPLANATION)} re-weighted patient
        records during training, so the model's error rates moved closer together across male and
        female patients, rather than optimising for overall accuracy alone.
    </div>
    <div class='method-box'>
        <strong>2. Confidence-based flagging (addresses Correctability)</strong><br><br>
        The model already gives a confidence score for each prediction, not just a yes or no answer.
        Predictions between {tt("30% and 70%", CONFIDENCE_BAND_EXPLANATION)} are automatically flagged
        for clinician review, rather than returned as a routine result. This does not change what the
        model predicts. It adds a signal for where a human should look more closely.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""<div style='font-size:0.85rem; color:#666; margin-top:0.5rem;'>
        Results of this evaluation, before and after both interventions, are presented in the
        <strong>Fairness Assessment</strong> tab.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 3: PROCEDURAL FAIRNESS ASSESSMENT
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("<h1>Procedural Fairness Assessment</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Detailed evaluation of each criterion with technical results</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card' style='background:#fff0f3; border-left:4px solid {PRIMARY}; margin-bottom:1.5rem;'>
        <strong>Framework</strong><br><br>
        Six procedural fairness criteria, based on Leventhal's (1980) procedural justice framework
        adapted for healthcare by Jabagi et al. (2025), each assessed at baseline and after
        mitigation.
    </div>
    """, unsafe_allow_html=True)

    scorecard_rows = "".join(f"""
        <tr style='border-bottom:1px solid #f0e0e5;'>
            <td style='padding:0.6rem 0.7rem; font-weight:600; color:{DARK}; white-space:nowrap;'>{name}</td>
            <td style='padding:0.6rem 0.7rem;'>
                <div style='display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;'>
                    <span style='font-variant-numeric:tabular-nums; font-size:0.82rem; color:{DARK}; display:inline-block; min-width:105px;'>{data['headline']}</span>
                    {badge(data['baseline'])}
                </div>
            </td>
            <td style='padding:0.6rem 0.7rem;'>
                <div style='display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;'>
                    <span style='font-variant-numeric:tabular-nums; font-size:0.82rem; color:{DARK}; display:inline-block; min-width:105px;'>{data['mitigated_headline']}</span>
                    {badge(data['mitigated'])}
                </div>
            </td>
        </tr>""" for name, data in criteria.items())

    st.markdown(f"""
    <div class='card' style='margin-bottom:1.5rem;'>
        <div class='rule-label' style='margin-bottom:0.4rem;'>At a Glance: All Six Criteria</div>
        <div style='margin-bottom:0.5rem;'><span style='letter-spacing:0.15rem; font-size:1.1rem;'><span style='color:{PASS_COLOR};'>●●●</span><span style='color:#d9b3bd;'>○○○</span></span> <span style='font-size:0.78rem; color:#666;'>3 of 6 pass at baseline</span></div>
        <div style='font-size:0.82rem; color:#666; margin-bottom:0.8rem;'>Every criterion, baseline and after mitigation, in one view. Use the toggle below for the full detail behind each result.</div>
        <div style='overflow-x:auto;'>
        <table style='width:100%; border-collapse:collapse; font-size:0.85rem;'>
            <thead>
                <tr style='border-bottom:2px solid #e0c3cc;'>
                    <th style='text-align:left; padding:0.5rem 0.7rem; color:{DARK}; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.03em;'>Criterion</th>
                    <th style='text-align:left; padding:0.5rem 0.7rem; color:{DARK}; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.03em;'>Baseline</th>
                    <th style='text-align:left; padding:0.5rem 0.7rem; color:{DARK}; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.03em;'>Mitigated</th>
                </tr>
            </thead>
            <tbody>{scorecard_rows}</tbody>
        </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_mit = st.toggle("View post-mitigation results", value=False, key="assessment_toggle",
        help="Compare the baseline model against the model after bias mitigation and confidence-based flagging were applied.")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    for name, data in criteria.items():
        result = data["mitigated"] if show_mit else data["baseline"]
        finding = data["mitigated_finding"] if show_mit else data["baseline_finding"]
        headline = data["mitigated_headline"] if show_mit else data["headline"]
        headline_label = data["mitigated_headline_label"] if show_mit else data["headline_label"]
        if name == "Correctability" and show_mit:
            headline = f"{data['headline']} → {data['mitigated_headline']}"
        cls = {"PASS": "pass", "FAIL": "fail", "PARTIAL": "partial"}[result]
        num_color = {"PASS": PASS_COLOR, "FAIL": FAIL_COLOR, "PARTIAL": PARTIAL_COLOR}[result]

        st.markdown(f"""
        <div class='card {cls}-card' style='margin-bottom:0.3rem;'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;'>
                <div style='flex:1;'>
                    <span class='rule-name'>{name}</span>
                    <div class='headline-metric' style='color:{num_color}; margin-top:0.3rem;'>{headline}</div>
                    <div class='headline-metric-label'>{headline_label}</div>
                </div>
                <div style='flex-shrink:0;'>{badge(result)}</div>
            </div>
            <div style='margin-top:0.7rem; font-size:0.88rem; color:#444; line-height:1.55;'>{finding}</div>
        </div>
        """, unsafe_allow_html=True)
        expander_label = f"Purpose, metrics and checklist: {name}" if name in ("Correctability", "Ethicality") else f"Purpose and metrics: {name}"
        with st.expander(expander_label):
            st.markdown(f"**Purpose:** {data['purpose']}")
            st.markdown(f"**Metrics:** {data['metrics']}")
            if name == "Correctability":
                if show_mit:
                    checklist = [
                        ("Prediction outputs are visible and interpretable", True, False),
                        ("Confidence scores are provided with predictions", True, False),
                        ("Low confidence predictions flagged for human review", True, True),
                        ("Clinician override mechanism exists", False, False),
                        ("Patient challenge mechanism exists", False, False),
                        ("Audit trail of predictions is maintained", False, False),
                        ("Model version history is recorded", False, False),
                        ("Dashboard communicates uncertainty to stakeholders", True, False),
                    ]
                    st.markdown(f"**Checklist: {data['headline']} at baseline → {data['mitigated_headline']} after mitigation**")
                else:
                    checklist = [
                        ("Prediction outputs are visible and interpretable", True, False),
                        ("Confidence scores are provided with predictions", True, False),
                        ("Clinician override mechanism exists", False, False),
                        ("Patient challenge mechanism exists", False, False),
                        ("Audit trail of predictions is maintained", False, False),
                        ("Model version history is recorded", False, False),
                        ("Dashboard communicates uncertainty to stakeholders", True, False),
                    ]
                    st.markdown(f"**Checklist (baseline): {data['headline']} met**")
                for item, passed, is_new in checklist:
                    icon = "✅" if passed else "❌"
                    tag = " — **added after mitigation**" if is_new else ""
                    st.markdown(f"{icon} {item}{tag}")
            elif name == "Ethicality":
                checklist = [
                    ("Ethics approval granted by Newcastle University", True),
                    ("Dataset is fully anonymised, no patient identifiers", True),
                    ("No personal data collected or processed", True),
                    ("GDPR compliance, survey is anonymous", True),
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
        <div style='font-size:0.82rem; color:#555; padding-top:0.5rem; border-top:1px solid #eee; line-height:1.5;'>
            <strong>Why:</strong> The baseline model identified heart disease in female patients at a
            much lower rate (70.0%) than male patients (93.5%). This intervention aimed to reduce
            that disparity. See the <strong>Methodology</strong> tab for how the training method works.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Recall by Sex: Baseline vs Post-Mitigation")
    st.caption("Recall measures the percentage of actual heart disease cases the tool correctly identified.")

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Male', x=['Baseline model','Post-mitigation model'], y=[93.5,93.5], marker_color="#7b2d4e", text=['93.5%','93.5%'], textposition='outside', width=0.3))
    fig.add_trace(go.Bar(name='Female', x=['Baseline model','Post-mitigation model'], y=[70.0,90.0], marker=dict(color="#e8a3b8", pattern=dict(shape="/")), text=['70.0%','90.0%'], textposition='outside', width=0.3))
    fig.add_hline(y=80, line_dash="dot", line_color="#5f5f5f", annotation_text="80% clinical threshold", annotation_position="bottom right")
    fig.add_annotation(text="Female n=39 · Male n=145", xref="paper", yref="paper", x=0.5, y=-0.16, xanchor="center", showarrow=False, font=dict(size=10, color="#888"))
    fig.update_layout(barmode='group', yaxis=dict(range=[0,105], showgrid=False, showticklabels=False), xaxis=dict(showgrid=False), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', y=1.1), margin=dict(t=20,b=45,l=0,r=120), font=dict(color=DARK, size=13), height=370)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("#### Distance to the ±0.10 Fairness Threshold")
    st.caption("Both measures moved toward the acceptable range after mitigation, but neither crossed it.")

    gauge = go.Figure()
    gauge.add_shape(type="rect", x0=0, x1=0.10, y0=-0.5, y1=1.5, fillcolor=PASS_BG, line=dict(width=0), layer="below")
    gauge.add_vline(x=0.10, line_dash="dot", line_color=PARTIAL_COLOR)
    gauge.add_annotation(x=0.10, y=1.42, text="±0.10 threshold", showarrow=False, font=dict(size=10, color=PARTIAL_COLOR), yanchor="bottom")

    gauge_rows = [
        ("Equalised Odds Difference", 0.235, 0.120),
        ("Demographic Parity Difference", 0.457, 0.380),
    ]
    for i, (label, before, after) in enumerate(gauge_rows):
        gauge.add_trace(go.Scatter(x=[before, after], y=[label, label], mode="lines", line=dict(color="#ccc", width=2), showlegend=False, hoverinfo="skip"))
        gauge.add_trace(go.Scatter(x=[before], y=[label], mode="markers", marker=dict(size=11, color=LIGHT, line=dict(color=PRIMARY, width=1.5)), name="Baseline", legendgroup="baseline", showlegend=(i == 0), hovertemplate=f"Baseline: {before:.3f}<extra></extra>"))
        gauge.add_trace(go.Scatter(x=[after], y=[label], mode="markers+text", marker=dict(size=13, color=PRIMARY), text=[f"{after:.3f}"], textposition="top center", textfont=dict(size=11, color=DARK), name="Mitigated", legendgroup="mitigated", showlegend=(i == 0), hovertemplate=f"Mitigated: {after:.3f}<extra></extra>"))

    gauge.add_annotation(text="Female test sample: n=39 · Male: n=145", xref="paper", yref="paper", x=0, y=-0.28, xanchor="left", showarrow=False, font=dict(size=10, color="#888"))
    gauge.update_layout(xaxis=dict(range=[0, 0.5], showgrid=False, zeroline=False, title=None), yaxis=dict(showgrid=False, zeroline=False), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', y=1.25), margin=dict(t=50, b=45, l=10, r=10), height=240, font=dict(color=DARK, size=12))
    st.plotly_chart(gauge, use_container_width=True, config={'displayModeBar': False})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='card partial-card'>
            <div style='font-size:0.85rem; font-weight:600; color:#555; text-transform:uppercase; margin-bottom:0.2rem;'>Equalised Odds Difference ⚠ Improved, Above Threshold</div>
            <div style='color:{PARTIAL_COLOR}; font-size:2rem; font-weight:700; line-height:1.2; margin:0.4rem 0;'>0.235 → 0.120</div>
            <div style='font-size:0.86rem; color:#444;'>The difference in error rates between male and female patients approximately halved after mitigation, but remained above the ±0.10 {tt("threshold", THRESH_DISPARITY)}.</div>
            <div style='font-size:0.82rem; color:#666; margin-top:0.4rem;'>This may be influenced by the small number of female patients in the test set (n=39), which limits the reliability of this measure.</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card partial-card'>
            <div style='font-size:0.85rem; font-weight:600; color:#555; text-transform:uppercase; margin-bottom:0.2rem;'>Demographic Parity Difference ⚠ Above Threshold</div>
            <div style='color:{PARTIAL_COLOR}; font-size:2rem; font-weight:700; line-height:1.2; margin:0.4rem 0;'>0.457 → 0.380</div>
            <div style='font-size:0.86rem; color:#444;'>The difference in positive prediction rates between male and female patients decreased but remained above the predefined ±0.10 {tt("threshold", THRESH_DISPARITY)}.</div>
            <div style='font-size:0.82rem; color:#666; margin-top:0.4rem;'>Measures whether the model flags patients across groups at similar rates.</div>
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
        <div style='font-size:0.82rem; color:#555; padding-top:0.5rem; border-top:1px solid #eee; line-height:1.5;'>
            <strong>Why:</strong> The baseline pipeline met only 3 of 7 correctability criteria and lacked
            mechanisms for human review of uncertain predictions. This intervention partially addresses
            that gap (now 4 of 8 criteria met). See the <strong>Methodology</strong> tab for how flagging works.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.metric("Overall flagged for review", "10.3%")

    flag_fig = go.Figure()
    flag_fig.add_trace(go.Bar(name='Male', x=['Flagged for clinician review'], y=[9.0], marker_color="#7b2d4e", text=['9.0%'], textposition='outside', width=0.3))
    flag_fig.add_trace(go.Bar(name='Female', x=['Flagged for clinician review'], y=[15.4], marker=dict(color="#e8a3b8", pattern=dict(shape="/")), text=['15.4%'], textposition='outside', width=0.3))
    flag_fig.add_annotation(text="Female n=39 · Male n=145", xref="paper", yref="paper", x=0.5, y=-0.18, xanchor="center", showarrow=False, font=dict(size=10, color="#888"))
    flag_fig.update_layout(barmode='group', yaxis=dict(range=[0,25], showgrid=False, showticklabels=False), xaxis=dict(showgrid=False), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', y=1.15), margin=dict(t=20,b=45,l=0,r=20), font=dict(color=DARK, size=13), height=280)
    st.plotly_chart(flag_fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("""<div style='font-size:0.86rem; color:#555; margin-top:0.3rem;'>
        <strong>Finding:</strong> Female patients were flagged for review nearly twice as often as male
        patients. This is the same disparity seen in the recall gap, surfacing here through a separate
        mechanism (model confidence rather than classification outcome). This may be related to
        differences in training data representation.
    </div>""", unsafe_allow_html=True)

    # ── OVERALL OUTCOME ──
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### Overall Outcome")
    st.markdown(f"""
    <div class='card' style='border-left:4px solid {PRIMARY}; background:#fff0f3;'>
        <div style='font-size:0.92rem; color:#444; line-height:1.6;'>
            The mitigation strategy improved procedural fairness by reducing disparities between
            demographic groups and introducing a mechanism for clinician oversight. Notably, female recall
            improved without any reduction in male recall. However, fairness was not fully achieved, as both
            formal fairness measures remained above threshold and limitations in dataset representativeness
            and governance mechanisms remained.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 4: PUBLIC SURVEY
# ══════════════════════════════════════════════════════════════
with tabs[3]:
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

    st.markdown("""<div style='color:#5f5f5f; font-size:0.78rem; text-align:center; padding:0.5rem 0;'>Age: 41–60 (29.2%) · Under 25 (28.3%) · Over 60 (22.8%) · 25–40 (19.7%)</div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Strongest Public Priorities: Human Oversight and Transparency")

    st.markdown(f"""
    <div class='tier-section'>
        <div class='rule-label'>Correctability</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;'>
            <div><div class='survey-hero'>{challenge_pct}%</div><div class='hero-desc'>chose the option supporting patients' right to request a human review of an AI decision, even at cost or delay</div></div>
            <div><div class='survey-hero'>{human_pct}%</div><div class='hero-desc'>chose the option supporting human doctor involvement in medical decisions, regardless of AI accuracy</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='tier-section'>
        <div class='rule-label'>Ethicality</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;'>
            <div><div class='survey-hero'>{consent_pct}%</div><div class='hero-desc'>chose the option supporting patients being informed when an AI tool is used in their care</div></div>
            <div><div class='survey-hero'>{data_consent_pct}%</div><div class='hero-desc'>chose the option supporting patients being informed when their records are used to train AI, even if anonymised</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Moderate Agreement: Equal Performance Across Groups")
    st.markdown(f"""
    <div class='tier-section'>
        <div class='rule-label'>Bias Suppression / Representativeness</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; align-items:center;'>
            <div><div class='survey-hero'>{tool_a_pct}%</div><div class='hero-desc'>chose equal performance across all patient groups over higher overall accuracy</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Mixed Views: Consistency")
    st.markdown(f"""
    <div class='tier-section'>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;'>
            <div><div class='survey-hero'>{same_rules_pct}%</div><div class='hero-desc'>favoured applying the same rules to every patient regardless of outcome</div></div>
            <div><div class='survey-hero'>{equal_outcomes_pct}%</div><div class='hero-desc'>prioritised equal accuracy across all patient groups over uniform rules</div></div>
        </div>
        <div style='font-size:0.82rem; color:#666; margin-top:1rem; padding-top:0.8rem; border-top:1px solid #eee;'>The majority leaned toward outcome-based fairness rather than procedural consistency.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='rule-label' style='margin-top:0.5rem;'>Additional Context: Trust in AI</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='card' style='padding:0.9rem 1.2rem;'>
        <span style='font-size:1.4rem; font-weight:700; color:{DARK};'>{trust_pct}%</span>
        <span style='font-size:0.85rem; color:#555;'> reported some level of trust in healthcare AI but believed human oversight should always remain.</span>
        <div style='font-size:0.76rem; color:#888; margin-top:0.3rem; font-style:italic;'>Context only: this does not directly measure accuracy as a fairness criterion and is not one of the six evaluated criteria.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style='font-size:0.82rem; color:#5f5f5f; font-style:italic; margin-top:1rem;'>
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
        import textwrap
        for col_name, title, main_options in questions:
            counts = survey[col_name].value_counts()
            filtered = counts[counts.index.isin(main_options)]
            other = counts[~counts.index.isin(main_options)].sum()
            if other > 0: filtered['Other responses'] = other
            pcts = (filtered / total_responses * 100).round(0).astype(int)
            wrapped_labels = ['<br>'.join(textwrap.wrap(str(lbl), 40)) for lbl in pcts.index]
            fig = go.Figure(go.Bar(x=pcts.values, y=wrapped_labels, orientation='h', marker_color=PRIMARY, text=[f"{v}%" for v in pcts.values], textposition='outside'))
            fig.update_layout(title=dict(text=title, font=dict(size=13)), xaxis=dict(showgrid=False, showticklabels=False, range=[0,118]), yaxis=dict(showgrid=False, autorange='reversed'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=38,b=10,l=0,r=55), height=max(170, len(filtered)*52), font=dict(color=DARK, size=11))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ══════════════════════════════════════════════════════════════
# TAB 5: DISCUSSION AND RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("<h1>Discussion and Recommendations</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Integrating technical findings and public expectations to identify priorities for responsible deployment</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card' style='background:#fff0f3; border-left:4px solid {PRIMARY}; margin-bottom:1.5rem;'>
        This tab draws on two independent sources: the pipeline, which evaluates the model's technical
        and procedural fairness, and the public survey, which explores what people expect from fairness
        in healthcare AI. They are kept separate, since one does not validate the other, and are only
        brought together in the final recommendations.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Key Pipeline Findings")
    pipeline_rows = [
        ("Accuracy", "AUC-ROC (0.957) exceeded the 0.80 threshold, indicating strong ability to distinguish between patients with and without heart disease. However, aggregate performance masked lower recall for female patients."),
        ("Bias Suppression", "Bias mitigation substantially reduced disparities between male and female patients, raising female recall from 70.0% to 90.0% with no reduction in male recall, although both fairness measures remained above the predefined threshold."),
        ("Representativeness", "Female patients and younger age groups were underrepresented compared with real-world disease prevalence."),
        ("Consistency", "Predictions remained stable under small, clinically realistic input perturbations, with instability of 0.0% at baseline and 1.1% after mitigation, both within the 5% threshold."),
        ("Correctability", "The pipeline lacked key correctability mechanisms. Confidence-based flagging was introduced to partially address this, improving criteria met from 3 of 7 to 4 of 8."),
        ("Ethicality", "Most ethical criteria were satisfied, but consent practices for secondary ML use were not documented."),
    ]
    pipeline_html = f"""
    <div style='background:#7b2d4e; color:white; padding:0.5rem 0.8rem; border-radius:8px 8px 0 0; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;'>Evidence source 1: Technical pipeline</div>
    <table style='width:100%; border-collapse:collapse; font-size:0.88rem; border:1px solid #f0d9df;'>
        <thead><tr style='border-bottom:2px solid #e0c3cc; background:#fbeef1;'>
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
    <div style='background:{RULE_LABEL}; color:white; padding:0.5rem 0.8rem; border-radius:8px 8px 0 0; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;'>Evidence source 2: Public survey</div>
    <table style='width:100%; border-collapse:collapse; font-size:0.88rem; border:1px solid #f0d9df;'>
        <thead><tr style='border-bottom:2px solid #e0c3cc; background:#fbeef1;'>
            <th style='text-align:left; padding:0.6rem 0.8rem; color:{DARK}; width:200px;'>Theme</th>
            <th style='text-align:left; padding:0.6rem 0.8rem; color:{DARK};'>Finding</th>
        </tr></thead>
        <tbody>{"".join(f"<tr style='border-bottom:1px solid #eee;'><td style='padding:0.6rem 0.8rem; font-weight:600; vertical-align:top; color:{DARK};'>{t}</td><td style='padding:0.6rem 0.8rem; color:#444; line-height:1.5;'>{f}</td></tr>" for t, f in survey_rows)}</tbody>
    </table>"""
    st.markdown(survey_html, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("## Bringing the Evidence Together")
    st.markdown(f"""
    <div class='card' style='border-left:4px solid {PRIMARY};'>
        <div style='font-size:0.9rem; color:#444; line-height:1.6;'>
            Mitigation substantially narrowed the recall gap between male and female patients
            (70.0% to 90.0% for female patients, with male recall unchanged at 93.5%), and moved two
            failing criteria, Bias Suppression and Correctability, to Partial, without fully
            resolving either. The public survey points in the same direction from a different angle:
            a majority of respondents expect equal performance across patient groups and continued
            human oversight regardless of how accurate the tool is. Together, the two sources suggest
            the technical improvements made here are a step toward what the public expects, not a
            substitute for it.
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
        {"title": "Collect more representative clinical data", "addresses": "Representativeness, Bias Suppression",
         "finding": "Female patients make up 21.0% of the dataset against 33.0% of real-world CHD prevalence (BHF, 2021), and the small female test sample (n=39) limits the precision of subgroup fairness estimates.",
         "recommendation": "Prioritise more representative clinical datasets before deployment."},
        {"title": "Implement clinician override and patient challenge mechanisms", "addresses": "Correctability",
         "finding": "Only 4 of 8 correctability criteria were satisfied, with no route for clinicians or patients to challenge a decision.",
         "recommendation": "Add clear mechanisms for clinician override, patient review requests, and accountability tracking."},
        {"title": "Establish prediction audit trails and model version control", "addresses": "Correctability",
         "finding": "Audit trail and model version history mechanisms were not available within the assessed pipeline.",
         "recommendation": "Add audit trails and version control to support accountability and retrospective review."},
        {"title": "Address informed consent for retrospective data use", "addresses": "Ethicality",
         "finding": "Consent practices for secondary ML use were not documented in the dataset.",
         "recommendation": "Establish clear consent frameworks for the secondary use of clinical data in ML research."},
        {"title": "Improve fairness communication and stakeholder involvement", "addresses": "All criteria",
         "finding": "This dashboard is one approach to communicating fairness findings to a mixed audience.",
         "recommendation": "Evaluate whether fairness dashboards are understandable and useful for clinicians, patients, and policymakers."},
    ]

    for n, rec in enumerate(recs, 1):
        st.markdown(f"""
        <div class='rec-box'>
            <div style='display:flex; align-items:center; gap:0.7rem; margin-bottom:0.5rem;'>
                <span class='rec-num'>{n}</span>
                <span style='font-weight:700; font-size:0.98rem;'>{rec['title']}</span>
            </div>
            <div style='margin-bottom:0.5rem;'><span class='rec-chip'>Addresses: {rec['addresses']}</span></div>
            <div style='font-size:0.85rem; color:#444; line-height:1.55;'>{rec['finding']}</div>
            <div style='font-size:0.86rem; color:{DARK}; margin-top:0.5rem; padding-top:0.5rem; border-top:1px solid #f0e0e5;'><strong>Recommendation:</strong> {rec['recommendation']}</div>
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

    st.markdown(f"""<div style='text-align:center; padding:2rem 0 1rem; color:#6a6a6a; font-size:0.82rem;'>
        Procedural Fairness in Healthcare ADM · Kaylee Scarce · Newcastle University 2026 · Supervised by Dr Vlad González-Zelaya
    </div>""", unsafe_allow_html=True)
