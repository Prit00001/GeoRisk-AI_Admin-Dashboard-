# 🌍 GeoRisk AI — Disaster Risk Monitoring Dashboard

> **AI-powered flood and landslide risk prediction for all 16 districts of Manipur, India.**  
> Built during the **IIM Shillong North-East Hackathon** by Team GeoRisk AI, IIIT Manipur.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![Live App](https://img.shields.io/badge/Live%20App-georisk1ai.streamlit.app-green)](https://georisk1ai.streamlit.app)

---

## 🎯 What This Does

Manipur faces recurring natural disasters — valley districts flood every monsoon, hill districts face landslides year-round. Yet no accessible, district-level risk tool existed for first responders or administrators.

**GeoRisk AI solves this.** It takes real-world environmental parameters as input and outputs an actionable risk score with 3-day advance warning — no data science background required to use it.

---

## ✨ Key Features

### 🌊 Flood Risk Prediction
- **3-day advance flood prediction** for all 16 Manipur districts
- Powered by a **Gradient Boosting Classifier** trained on 17 environmental features
- Smart seasonal defaults — auto-detects monsoon vs winter and adjusts baselines
- Outputs flood probability (0–100%), risk level (Critical / High / Moderate / Low), and actionable warnings
- Downloadable PDF/CSV risk reports

### 🏔️ Landslide Risk Mapping
- **Grid-based spatial analysis** across district boundaries
- Predicts risk zones (High / Medium / Low / Minimal) at coordinate level
- Uses elevation, slope gradient, and rainfall as core features
- Interactive color-coded map visualization
- Downloadable CSV with zone-level breakdown

---

## 🧠 Model Details

### Flood Prediction Model
| Property | Details |
|---|---|
| Algorithm | Gradient Boosting Classifier |
| Features | 17 (meteorological + physical + infrastructural) |
| Output | Flood probability % + risk level |
| Prediction window | 3 days in advance |
| Districts covered | All 16 Manipur districts |
| Serialization | joblib |

**Input Features:**
| Category | Features |
|---|---|
| Meteorological | 3-day cumulative rainfall, temperature, humidity, wind speed, season |
| Physical | River water level, soil moisture, terrain elevation |
| Infrastructural | Drainage capacity, dam release status |

**Why these features?**
- River water level indicates upstream discharge buildup — the most direct flood precursor
- Soil moisture reveals whether ground can absorb more rainfall or will cause runoff
- 3-day cumulative rainfall (not single-day) captures how flood risk builds over time
- Dam release status accounts for flash flood risk independent of rainfall

### Landslide Prediction Model
| Property | Details |
|---|---|
| Algorithm | Random Forest |
| Features | Elevation, slope gradient, rainfall intensity |
| Output | Risk level per grid point + probability |
| Spatial resolution | 4–6 grid points per district |

---

## 📊 Data Sources

| Source | Data Type | Used For |
|---|---|---|
| NDMA (National Disaster Management Authority) | Historical disaster event records, district vulnerability indices | Model training, risk baseline |
| NDMI (National Disaster Management Institute) | Risk assessment frameworks, regional risk scores | Feature engineering |
| CWC (Central Water Commission) | River water level readings | Flood feature |
| IMD / Weather APIs | Rainfall, temperature, humidity, wind speed | Meteorological features |
| SRTM / Terrain APIs | Elevation and slope data | Landslide features |

---

## 🗺️ Supported Districts

**Valley Districts (Flood-prone):**
Imphal West · Imphal East · Bishnupur · Thoubal · Kakching · Jiribam

**Hill Districts (Landslide-prone):**
Senapati · Kangpokpi · Tamenglong · Noney · Ukhrul · Kamjong · Churachandpur · Pherzawl · Chandel · Tengnoupal

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install streamlit pandas numpy plotly scikit-learn==1.3.0 joblib
```

### File Structure
```
GeoRisk-AI/
├── streamlit_app.py          # Main dashboard
├── flood.py                  # Flood prediction module
├── landslide_core.py         # Landslide prediction module
├── requirements.txt
├── runtime.txt
└── model_export/
    ├── manipur_flood_model.joblib
    ├── manipur_encoders.joblib
    ├── manipur_predictor.py
    └── model_metadata.json
```

### Run Locally
```bash
git clone https://github.com/Prit00001/GeoRisk-AI_Admin-Dashboard-
cd GeoRisk-AI_Admin-Dashboard-
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Open `http://localhost:8501` in your browser.

---

## 📖 How to Use

**Flood Assessment:**
1. Select a district from the dropdown
2. Optionally expand "Advanced Parameters" to input live readings:
   - 3-day cumulative rainfall (mm)
   - River water level (m), Soil moisture (%), Drainage capacity
   - Dam release status, Temperature, Humidity, Wind speed
3. Click **Generate Flood Risk Assessment**
4. View probability score, risk level, warnings, and download the report

**Landslide Assessment:**
1. Select a district
2. Click **Generate Landslide Risk Map**
3. View color-coded zone map and download CSV

> **Note:** All parameters have intelligent seasonal defaults — the model auto-detects the current month and fills in appropriate baseline values if you don't have live data.

---

## 🐛 Troubleshooting

**`AttributeError: __pyx_unpickle_CyHalfBinomialLoss`**
```bash
pip install scikit-learn==1.3.0
```
The model was serialized with scikit-learn 1.x — version must match.

**`ModuleNotFoundError: landslide_core`**
Ensure `landslide_core.py` is in the same directory as `streamlit_app.py`. The function signature expected:
```python
# Returns: (result_dict, env_dict)
result, env = predict_with_free_apis(lat, lon)
# result keys: risk_level, landslide_probability
# env keys: elevation, slope, rainfall
```

**`FileNotFoundError: manipur_flood_model.joblib`**
Ensure the `model_export/` folder is present with all four files intact.

---

## 🔮 Roadmap

- [ ] Real-time CWC river level API integration
- [ ] IMD live rainfall feed
- [ ] Historical risk comparison (year-over-year)
- [ ] SMS/email alert system for Critical zones
- [ ] Expand coverage to other North-East states

---

## 👥 Team

Built at the **IIM Shillong North-East Hackathon** by students of **IIIT Manipur**.

| Name | Role |
|---|---|
| Pratyush Pandey | Data pipeline, Admin Dashboard, Visualisation |
| Kumar Gaurav |  |
| Rishabh Pandey | ML Engineer |

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.

---

*Last updated: June 2026*
