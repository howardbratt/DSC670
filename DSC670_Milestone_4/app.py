"""Streamlit interface for the Healthcare Data Mapping Assistant."""

import json
import os
from pathlib import Path

import streamlit as st

from mapping import INPUTS, TARGETS, checkpoint_ready, generate_mapping, load_model, read_examples
from mapping import validate_response

st.set_page_config(page_title="Healthcare Data Mapping Assistant", page_icon="🗂️", layout="wide")
root = Path(__file__).resolve().parent
model_path = Path(os.environ.get("MAPPING_MODEL_DIR", root / "final_model")).expanduser().resolve()


@st.cache_resource(show_spinner=False)
def get_model(path):
    # Preserve a single model across Streamlit reruns.
    return load_model(path)


st.title("Healthcare Data Mapping Assistant")
st.caption("DSC670 Milestone 4 · Shelia Howard")
st.write("Suggest a target for a demographic field and record an analyst decision.")
st.info("Use synthetic field metadata only. Keep patient records and identifiers out of the form.")

with st.sidebar:
    st.header("Inference mode")
    live, demo = "Live Qwen checkpoint", "Illustrative demo"
    ready = checkpoint_ready(model_path)
    mode = st.radio("Mode", [demo, live], index=int(ready))
    if mode == live:
        st.caption("Uses the model files in the configured checkpoint folder.")
    else:
        st.caption("Uses authored responses for two synthetic examples.")
    with st.expander("Approved target fields"):
        st.code("\n".join(TARGETS), language=None)

if mode == live and not ready:
    st.warning("Checkpoint missing. Extract the Milestone 3 full-model ZIP and see the README for setup.")
    st.stop()

left, right = st.columns([1, 1], gap="large")
with left:
    st.subheader("Source field")
    example = None
    if mode == demo:
        examples = {case["label"]: case for case in read_examples()}
        example = examples[st.selectbox("Synthetic example", list(examples))]
        source = example["source"]
        st.table([{"Field": key.replace("_", " ").title(), "Value": source[key]} for key in INPUTS])
        submitted = st.button("Show illustrative result", type="primary")
    else:
        with st.form("mapping_form"):
            source = {
                "source_field": st.text_input("Source field name", max_chars=100),
                "datatype": st.text_input("Datatype", max_chars=50),
                "description": st.text_area("Description", max_chars=600),
                "example_value": st.text_input("Synthetic example value (optional)", max_chars=120),
            }
            submitted = st.form_submit_button("Generate recommendation", type="primary")
        source = {key: value.strip() for key, value in source.items()}

# Associate results with the submitted input and mode to prevent stale results.
signature = (mode, tuple(source.values()))
if submitted:
    st.session_state.pop("mapping_result", None)
    if not all(source[key] for key in INPUTS[:3]):
        left.error("Enter a field name, datatype, and description.")
    else:
        try:
            if example is not None:
                raw = json.dumps(example["response"])
            else:
                with st.spinner("Running checkpoint inference…"):
                    raw = generate_mapping(*get_model(str(model_path)), source)
        except (ImportError, OSError, ValueError, RuntimeError) as error:
            left.error(f"Inference failed ({type(error).__name__}). Check the model files and setup guide.")
        else:
            response, valid = validate_response(raw)
            run = st.session_state.get("mapping_run", 0) + 1
            st.session_state["mapping_run"] = run
            st.session_state["mapping_result"] = (signature, response, valid, run)

with right:
    st.subheader("Recommendation")
    saved = st.session_state.get("mapping_result")
    if not saved or saved[0] != signature:
        st.caption("Submit the source metadata to see its recommendation here.")
    else:
        _, response, valid, run = saved
        target = response["target_field"]
        if response["human_review"]:
            st.warning("Analyst review required")
        else:
            st.success("Candidate mapping")
        st.code(target, language=None)
        st.text(response["reason"])
        st.caption("Illustrative response" if mode == demo else "Live Qwen response")
        if not valid:
            st.caption("The app assigned REVIEW after response validation failed.")
        with st.expander("Structured result"):
            st.json(response)

        st.subheader("Analyst decision")
        options = ["Hold", "Reject", "Revise"]
        if target != "REVIEW":
            options.insert(1, "Accept")
        decision = st.selectbox("Decision", options, key=f"decision_{run}")
        selected = None
        if decision == "Accept":
            selected = target
        if decision == "Revise":
            selected = st.selectbox("Analyst-selected target", TARGETS, key=f"target_{run}")
        record = {
            "mode": mode, "source": source, "contract_valid": valid,
            "recommendation": response, "analyst_decision": decision,
            "analyst_target": selected,
        }
        st.download_button(
            "Download decision as JSON", json.dumps(record, indent=2),
            file_name="mapping_decision.json", mime="application/json",
        )
