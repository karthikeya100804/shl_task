import streamlit as st
import requests

# === CONFIG ===
API_URL = "https://shl-task-qz8g.onrender.com/recommend"  

# === UI ===
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("🔍 SHL Assessment Recommendation Tool")

query = st.text_area("Enter a job description or hiring requirement:", height=200)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            try:
                response = requests.get(API_URL, params={"text": query})
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    if not results:
                        st.info("No assessments matched the query.")
                    else:
                        for idx, item in enumerate(results, start=1):
                            st.markdown(f"### {idx}. [{item['Test Name']}]({item['Test Link']})")
                            st.markdown(f"- **Test Type:** {item['Test Type']}")
                            st.markdown(f"- **Remote Testing:** {item['Remote Testing']}")
                            st.markdown(f"- **Adaptive/IRT:** {item['Adaptive/IRT']}")
                            st.markdown(f"- **Duration:** {item['Duration (min)']} minutes")
                            st.markdown("---")
                else:
                    st.error("Failed to fetch recommendations. Try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
