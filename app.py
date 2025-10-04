import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from crew_setup import crew

# ===========================================
# 🧠 Load Trained Autoencoder Model
# ===========================================
autoencoder = load_model("ai_sentinel_autoencoder.h5", compile=False)

# ===========================================
# 🏷️ App Title
# ===========================================
st.title("🛡️ AI Sentinel - Log Anomaly Detector")
st.caption("A multi-agent anomaly detection system with lightweight guardrails.")

# ===========================================
# 📂 File Upload Section
# ===========================================
uploaded_files = st.file_uploader(
    "Upload preprocessed log files (.csv)",
    type="csv",
    accept_multiple_files=True
)

# ===========================================
# 🧩 Lightweight Guardrail & Validation Utils
# ===========================================
def clean_text(text: str) -> str:
    """Minimal guardrail to trim irrelevant or unsafe outputs."""
    if not isinstance(text, str):
        return "Invalid model response."
    # Keep natural reasoning flow but trim extreme or irrelevant outputs
    blocked_terms = ["<html>", "</script>", "import ", "Traceback (most recent call)"]
    if any(term.lower() in text.lower() for term in blocked_terms):
        return "Response skipped due to invalid output."
    # Trim overly long responses for clarity
    return text.strip()[:800]

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures uploaded dataset is clean and numeric."""
    if df.isnull().sum().sum() > 0:
        st.warning("⚠️ Missing values detected — replaced with 0.")
        df = df.fillna(0)
    non_numeric = [col for col in df.columns if not np.issubdtype(df[col].dtype, np.number)]
    if non_numeric:
        st.warning(f"⚠️ Non-numeric columns detected and ignored: {non_numeric}")
        df = df.select_dtypes(include=[np.number])
    return df

# ===========================================
# 🚨 Severity Mapping Function
# ===========================================
def map_severity(error, threshold=20):
    if error > threshold * 2:
        return "Critical"
    elif error > threshold * 1.5:
        return "Major"
    else:
        return "Minor"

# ===========================================
# 🚀 Main Execution
# ===========================================
if uploaded_files:
    dfs = [pd.read_csv(file) for file in uploaded_files]
    df = pd.concat(dfs, ignore_index=True)
    df = validate_data(df)
    st.write("✅ Uploaded Data Sample:")
    st.dataframe(df.head())

    # Ensure BlockId exists
    if "BlockId" not in df.columns:
        df.insert(0, "BlockId", range(1, len(df) + 1))

    # Convert to NumPy
    X = df.drop(columns=["BlockId"]).values

    # Predict reconstruction
    reconstructed = autoencoder.predict(X)
    errors = np.mean((X - reconstructed) ** 2, axis=1)

    # Threshold
    threshold = 20
    predictions = (errors > threshold).astype(int)

    # Add results
    df["Reconstruction Error"] = errors
    df["Prediction"] = ["Anomaly" if p == 1 else "Normal" for p in predictions]
    df["Severity"] = df["Reconstruction Error"].apply(lambda e: map_severity(e, threshold))

    # Summary
    st.subheader("📊 Summary")
    st.write(f"**Total Logs:** {len(df)}")
    st.write(f"**Anomalies:** {(df['Prediction'] == 'Anomaly').sum()}")
    st.write(f"**Normal Entries:** {(df['Prediction'] == 'Normal').sum()}")

    # Preview results
    st.subheader("🔎 Results Preview")
    st.dataframe(df.head(20))

    # ===========================================
    # 🤖 CrewAI Multi-Agent Section
    # ===========================================
    st.subheader("🧠 CrewAI Agent Reasoning")
    anomaly_rows = df[df["Prediction"] == "Anomaly"]

    if not anomaly_rows.empty:
        explanations = []

        # Pick one anomaly from each severity level
        for severity_level in ["Critical", "Major", "Minor"]:
            sample = anomaly_rows[anomaly_rows["Severity"] == severity_level].head(1)

            if not sample.empty:
                sample = sample.iloc[0]
                block_id = sample["BlockId"]
                error = sample["Reconstruction Error"]
                sequence = sample.drop(["Reconstruction Error", "Prediction", "Severity"]).tolist()

                try:
                    result = crew.kickoff(inputs={
                        "block_id": str(block_id),
                        "error": float(error),
                        "sequence": [str(s) for s in sequence]
                    })

                    reason, action = "N/A", "N/A"

                    if hasattr(result, "tasks_output") and result.tasks_output:
                        outputs = result.tasks_output
                        if len(outputs) > 0:
                            reason = clean_text(outputs[0].raw)
                        if len(outputs) > 2:
                            action = clean_text(outputs[2].raw)

                except Exception as e:
                    reason = f"⚠️ CrewAI Error: {str(e)[:200]}"
                    action = "N/A"

                explanations.append({
                    "BlockId": block_id,
                    "Reason": reason,
                    "Severity": severity_level,
                    "Suggested Action": action
                })

        # Display CrewAI results
        final_df = pd.DataFrame(explanations)
        st.write("### 📝 Example Results (1 per Severity)")
        st.dataframe(final_df)

        with st.expander("🔍 Full Anomaly List with Severity Buckets"):
            st.dataframe(anomaly_rows)

    else:
        st.success("✅ No anomalies detected to analyze.")

    # ===========================================
    # 📥 Download Results
    # ===========================================
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results", csv, "results.csv", "text/csv")

else:
    st.info("👆 Please upload one or more log CSV files to start the analysis.")
