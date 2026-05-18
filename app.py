import streamlit as st
from pipeline import run_research_pipeline

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main {
    padding-top: 2rem;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
    font-weight: bold;
}

.report-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("🔎 AI Multi-Agent Research Assistant")
st.markdown(
    "Research any topic using Search Agent, Reader Agent, Writer Agent & Critic Agent."
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.info("Enter a topic and generate a complete research report.")

# -----------------------------
# Input Section
# -----------------------------
topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Future of Agentic AI"
)

# -----------------------------
# Run Button
# -----------------------------
if st.button("🚀 Generate Research Report"):

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    # Progress Area
    progress = st.progress(0)

    try:
        # -----------------------------
        # Run Pipeline
        # -----------------------------
        with st.spinner("Running Research Pipeline..."):

            progress.progress(10)

            result = run_research_pipeline(topic)

            progress.progress(100)

        st.success("Research Completed Successfully ✅")

        # -----------------------------
        # Tabs
        # -----------------------------
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Search Results",
            "📚 Scraped Content",
            "📝 Final Report",
            "🧠 Critic Feedback"
        ])

        # -----------------------------
        # Search Results
        # -----------------------------
        with tab1:
            st.subheader("Search Results")
            st.write(result.get("search_results", "No data"))

        # -----------------------------
        # Scraped Content
        # -----------------------------
        with tab2:
            st.subheader("Detailed Scraped Content")
            st.write(result.get("Scraped_content", "No data"))

        # -----------------------------
        # Final Report
        # -----------------------------
        with tab3:
            st.subheader("Generated Research Report")

            st.markdown(
                f"""
                <div class="report-box">
                {result.get("report", "No report generated")}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Download button
            st.download_button(
                label="📥 Download Report",
                data=result.get("report", ""),
                file_name=f"{topic}_report.txt",
                mime="text/plain"
            )

        # -----------------------------
        # Critic Feedback
        # -----------------------------
        with tab4:
            st.subheader("Critic Feedback")
            st.write(result.get("feedback", "No feedback"))

    except Exception as e:
        st.error(f"Error Occurred: {e}")