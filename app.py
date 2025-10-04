import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from crew_setup import crew

# Load trained model
autoencoder = load_model("ai_sentinel_autoencoder.h5", compile=False)

# Title
st.title("🛡️ AI Sentinel - Log Anomaly Detector")

# File upload
uploaded_files = st.file_uploader(
    "Upload preprocessed log files (.csv)",
    type="csv",
    accept_multiple_files=True
)

# Function to map severity deterministically from reconstruction error
def map_severity(error, threshold=20):
    if error > threshold * 2:
        return "Critical"
    elif error > threshold * 1.5:
        return "Major"
    else:
        return "Minor"

if uploaded_files:
    dfs = [pd.read_csv(file) for file in uploaded_files]
    df = pd.concat(dfs, ignore_index=True)
    st.write("✅ Uploaded Data Sample:", df.head())

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
    total_logs = len(df)
    anomalies = (df["Prediction"] == "Anomaly").sum()
    normals = (df["Prediction"] == "Normal").sum()
    st.subheader("📊 Summary")
    st.write(f"**Total Logs:** {total_logs}")
    st.write(f"**Anomalies:** {anomalies}")
    st.write(f"**Normal Entries:** {normals}")

    # Preview results
    st.subheader("🔎 Results Preview")
    st.dataframe(df.head(20))

    # =====================
    # 🚀 CrewAI Multi-Agent
    # =====================
    st.subheader("🤖 CrewAI Agent Pipeline")
    anomaly_rows = df[df['Prediction'] == 'Anomaly']

    if not anomaly_rows.empty:
        explanations = []

        # Pick one anomaly from each severity
        for severity_level in ["Critical", "Major", "Minor"]:
            sample = anomaly_rows[anomaly_rows["Severity"] == severity_level].head(1)

            if not sample.empty:
                sample = sample.iloc[0]
                block_id = sample["BlockId"]
                error = sample["Reconstruction Error"]
                sequence = sample.drop(["Reconstruction Error", "Prediction", "Severity"]).tolist()

                result = crew.kickoff(inputs={
                    "block_id": str(block_id),
                    "error": float(error),
                    "sequence": [str(s) for s in sequence]
                })

                # Default values
                reason, action = "N/A", "N/A"

                if hasattr(result, "tasks_output") and result.tasks_output:
                    outputs = result.tasks_output
                    if len(outputs) > 0:
                        reason = outputs[0].raw
                    if len(outputs) > 2:
                        action = outputs[2].raw

                explanations.append({
                    "BlockId": block_id,
                    "Reason": reason,
                    "Severity": severity_level,
                    "Suggested Action": action
                })

        # Convert to dataframe for display
        final_df = pd.DataFrame(explanations)
        st.write("### 📝 One Example per Severity")
        st.dataframe(final_df)

        # (Optional) Expand to show all anomalies with severity assigned
        with st.expander("🔍 Full Anomaly List with Severity Buckets"):
            st.dataframe(anomaly_rows)

    else:
        st.write("✅ No anomalies detected to analyze.")

    # Download results
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results", csv, "results.csv", "text/csv")
