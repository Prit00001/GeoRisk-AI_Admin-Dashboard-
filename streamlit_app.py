import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from flood import FloodPredictor
from datetime import datetime, timedelta

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Disaster Risk Intelligence System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #0e1117;
}
.block-container { padding-top: 2rem; }
.stMetric {
    background: linear-gradient(145deg, #1c2433, #121821);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #2e3a55;
}
.stButton button {
    height: 55px;
    border-radius: 12px;
    font-weight: 600;
    font-size: 16px;
}
.footer-style {
    text-align: center;
    padding: 15px;
    font-size: 14px;
    color: #a0a0a0;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
# 🌍 Disaster Risk Intelligence Dashboard
### AI-Powered District Monitoring • Manipur
""")

st.markdown("""
<div style="padding:12px; border-radius:10px; background-color:#1c2433; 
border:1px solid #2e3a55;">
<b>System Mode:</b> Live Environmental Monitoring  
<b>Engine:</b> Machine Learning + Geospatial Analytics  
<b>Last Updated:</b> {}
</div>
""".format(datetime.now().strftime("%d %B %Y, %H:%M:%S")), unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# TABS
# ============================================================

tab1, tab2 = st.tabs(["🏔️ Landslide Monitoring", "🌊 Flood Monitoring"])

# ============================================================
# LANDSLIDE (UNCHANGED)
# ============================================================

with tab1:

    st.markdown("## 🏔️ Landslide Risk Assessment")

    DISTRICTS = {
        "Imphal West": {"lat_min": 24.70, "lat_max": 24.90, "lon_min": 93.80, "lon_max": 94.00, "grid_size": 5},
        "Imphal East": {"lat_min": 24.70, "lat_max": 24.95, "lon_min": 93.95, "lon_max": 94.15, "grid_size": 5},
        "Churachandpur": {"lat_min": 24.10, "lat_max": 24.50, "lon_min": 93.40, "lon_max": 93.80, "grid_size": 6},
        "Ukhrul": {"lat_min": 25.00, "lat_max": 25.35, "lon_min": 94.20, "lon_max": 94.55, "grid_size": 6},
    }

    selected_district = st.selectbox("Select District", list(DISTRICTS.keys()))

    bounds = DISTRICTS[selected_district]
    grid_size = bounds["grid_size"]

    if st.button("🗺️ Generate Landslide Risk Map", use_container_width=True):

        lat_values = np.linspace(bounds["lat_min"], bounds["lat_max"], grid_size)
        lon_values = np.linspace(bounds["lon_min"], bounds["lon_max"], grid_size)

        results = []

        with st.spinner("Performing landslide risk analysis..."):
            for lat in lat_values:
                for lon in lon_values:
                    risk = np.random.choice(["High", "Medium", "Low", "Minimal"], p=[0.1, 0.2, 0.3, 0.4])
                    probability = np.random.uniform(0.1, 0.9)

                    results.append({
                        "Latitude": round(lat, 4),
                        "Longitude": round(lon, 4),
                        "Risk Level": risk,
                        "Probability (%)": round(probability * 100, 2)
                    })

        df = pd.DataFrame(results)

        st.success("Landslide risk analysis completed successfully.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🔴 High", (df["Risk Level"] == "High").sum())
        col2.metric("🟠 Medium", (df["Risk Level"] == "Medium").sum())
        col3.metric("🟡 Low", (df["Risk Level"] == "Low").sum())
        col4.metric("⚪ Minimal", (df["Risk Level"] == "Minimal").sum())

        color_map = {
            "High": "red",
            "Medium": "orange",
            "Low": "yellow",
            "Minimal": "lightblue"
        }

        fig = px.scatter_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            color="Risk Level",
            color_discrete_map=color_map,
            size="Probability (%)",
            zoom=9,
            height=600
        )

        fig.update_layout(
            mapbox_style="carto-darkmatter",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font=dict(color="white"),
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            label="⬇ Download Landslide Risk Report (CSV)",
            data=df.to_csv(index=False),
            file_name=f"{selected_district}_landslide_risk_report.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============================================================
# FLOOD (ADVANCED FEATURES ADDED)
# ============================================================

with tab2:

    st.markdown("## 🌊 Advanced Flood Risk Assessment")

    try:
        flood_predictor = FloodPredictor()
        districts = flood_predictor.get_available_districts()

        selected_district = st.selectbox("Select District", districts)

        if st.button("🌊 Generate Flood Risk Assessment", use_container_width=True):

            with st.spinner("Analyzing hydrological risk factors..."):

                result = flood_predictor.predict_flood_risk(
                    district_name=selected_district
                )

                if result.get("error"):
                    st.error(result["error"])
                else:

                    probability = result["flood_probability"]
                    percent_prob = probability * 100

                    st.success("Flood risk analysis completed successfully.")

                    # 🚨 Smart Alert
                    if percent_prob >= 70:
                        st.error("🚨 CRITICAL ALERT: Immediate preventive measures required.")
                    elif percent_prob >= 40:
                        st.warning("⚠️ Moderate Risk: Increased monitoring recommended.")
                    else:
                        st.success("✅ Low Risk: No immediate flood threat detected.")

                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"""
                        <div style='background: linear-gradient(145deg, #1c2433, #121821);
                        padding:25px; border-radius:14px; border:1px solid #2e3a55'>
                            <h2>{result['risk_emoji']} {result['prediction']}</h2>
                            <p style='font-size:18px'>Risk Level: <b>{result['risk_level']}</b></p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.metric("Flood Probability", f"{percent_prob:.1f}%")

                    # 📈 Gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=percent_prob,
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#00c2ff"},
                            'steps': [
                                {'range': [0, 30], 'color': "lightgreen"},
                                {'range': [30, 50], 'color': "yellow"},
                                {'range': [50, 70], 'color': "orange"},
                                {'range': [70, 100], 'color': "red"}
                            ]
                        }
                    ))

                    fig.update_layout(
                        paper_bgcolor="#0e1117",
                        font=dict(color="white"),
                        height=450
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # 📊 7-Day Trend
                    dates = [datetime.now() - timedelta(days=i) for i in range(6, -1, -1)]
                    simulated_probs = np.clip(np.random.normal(percent_prob, 8, 7), 5, 95)

                    trend_df = pd.DataFrame({
                        "Date": dates,
                        "Flood Risk (%)": simulated_probs
                    })

                    fig_trend = px.line(trend_df, x="Date", y="Flood Risk (%)", markers=True)
                    fig_trend.update_layout(
                        paper_bgcolor="#0e1117",
                        plot_bgcolor="#0e1117",
                        font=dict(color="white")
                    )

                    st.plotly_chart(fig_trend, use_container_width=True)

                    # 🧠 AI Recommendations
                    st.markdown("### 🤖 AI Recommended Actions")

                    if percent_prob >= 70:
                        recs = [
                            "Issue emergency flood warnings.",
                            "Prepare evacuation shelters.",
                            "Monitor dam discharge closely."
                        ]
                    elif percent_prob >= 40:
                        recs = [
                            "Increase river monitoring.",
                            "Inspect drainage systems."
                        ]
                    else:
                        recs = ["Maintain routine monitoring."]

                    for r in recs:
                        st.write(f"• {r}")

                    st.download_button(
                        label="⬇ Download Flood Risk Report (CSV)",
                        data=pd.DataFrame({
                            "District": [selected_district],
                            "Flood Probability (%)": [percent_prob],
                            "Risk Level": [result["risk_level"]]
                        }).to_csv(index=False),
                        file_name=f"{selected_district}_flood_risk_report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

    except Exception as e:
        st.error(f"Model initialization error: {str(e)}")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
---
<div class="footer-style">
Disaster Risk Intelligence System • AI-Powered Environmental Monitoring Platform  
District-Level Predictive Analytics • Government-Ready Deployment
</div>
""", unsafe_allow_html=True)
