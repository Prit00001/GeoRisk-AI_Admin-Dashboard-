# 🌍 Disaster Risk Monitoring Dashboard

A comprehensive Streamlit dashboard for monitoring **Landslide** and **Flood** risks across Manipur districts using machine learning models.

## 📋 Features

### 🏔️ Landslide Risk Assessment
- Grid-based analysis across district boundaries
- Multiple risk levels (High, Medium, Low, Minimal)
- Interactive map visualization
- Environmental factor analysis (elevation, slope, rainfall)
- Downloadable CSV reports

### 🌊 Flood Risk Assessment
- 3-day advance flood prediction
- All 16 Manipur districts covered
- Real-time weather parameter input
- Risk gauge visualization
- District-specific information (rivers, elevation, flood-prone scores)

## 🚀 Quick Start

### Prerequisites
```bash
pip install streamlit pandas numpy plotly scikit-learn joblib
```

### File Structure
```
project/
├── streamlit_app.py          # Main dashboard application
├── flood.py                   # Flood prediction module
├── landslide_core.py          # Your landslide prediction module (to be added)
└── model_export/              # Flood model files
    ├── manipur_flood_model.joblib
    ├── manipur_encoders.joblib
    ├── manipur_predictor.py
    └── model_metadata.json
```

### Running the Dashboard

1. **Place all files in the same directory**

2. **Run the Streamlit app:**
```bash
streamlit run streamlit_app.py
```

3. **Open your browser** to `http://localhost:8501`

## 📖 Usage Guide

### Landslide Risk Assessment

1. Click the **"🏔️ Landslide Risk Assessment"** button
2. Select a district from the dropdown
3. Click **"Generate Landslide Risk Map"**
4. View:
   - Risk metrics (High/Medium/Low zones)
   - Interactive map with color-coded risk levels
   - Detailed data grid
   - Download CSV report

### Flood Risk Assessment

1. Click the **"🌊 Flood Risk Assessment"** button
2. Select a district from the dropdown
3. (Optional) Expand "Advanced Parameters" to customize:
   - Rainfall (3-day cumulative)
   - Temperature, Humidity, Wind Speed
   - River water level
   - Soil moisture, Drainage capacity
   - Dam release status, Season
4. Click **"Generate Flood Risk Assessment"**
5. View:
   - Flood probability percentage
   - Risk level (Critical/High/Moderate/Low)
   - Warnings and alerts
   - District information
   - Risk gauge chart
   - Download report

## 🔧 Integrating Your Landslide Model

The current code has a **PLACEHOLDER** for landslide predictions. Replace this section in `streamlit_app.py`:

```python
# CURRENT (Line ~183):
# DUMMY DATA for demonstration (remove this and use your actual function)
result = {
    "risk_level": np.random.choice([...]),
    "landslide_probability": np.random.uniform(0.1, 0.9)
}
```

**REPLACE WITH:**
```python
# Import your module at the top
from landslide_core import predict_with_free_apis

# Then use it:
result, env = predict_with_free_apis(lat, lon)
```

Make sure your `predict_with_free_apis()` function returns:
- `result`: dict with keys `risk_level` and `landslide_probability`
- `env`: dict with keys `elevation`, `slope`, `rainfall`

## 🐛 Troubleshooting

### Issue 1: "Scikit-learn version mismatch"

**Error:**
```
AttributeError: Can't get attribute '__pyx_unpickle_CyHalfBinomialLoss'
```

**Solution:**
The flood model was trained with scikit-learn 1.x. Upgrade your version:
```bash
pip install --upgrade scikit-learn
# or
pip install scikit-learn==1.3.0
```

### Issue 2: "Module 'landslide_core' not found"

**Solution:**
1. Create your `landslide_core.py` file with the `predict_with_free_apis()` function
2. Place it in the same directory as `streamlit_app.py`
3. Make sure it's properly imported

### Issue 3: "Flood model files not found"

**Solution:**
1. Ensure the `model_export/` folder is in the same directory
2. Check that these files exist:
   - `manipur_flood_model.joblib`
   - `manipur_encoders.joblib`
   - `manipur_predictor.py`

### Issue 4: Dark theme not displaying

**Solution:**
The dashboard uses dark theme by default. If colors look off:
1. Go to Streamlit Settings (☰ menu)
2. Settings → Theme → Choose "Dark"

## 📊 Supported Districts

### All 16 Manipur Districts:
- **Valley Districts (6):** Imphal West, Imphal East, Bishnupur, Thoubal, Kakching, Jiribam
- **Hill Districts (10):** Senapati, Kangpokpi, Tamenglong, Noney, Ukhrul, Kamjong, Churachandpur, Pherzawl, Chandel, Tengnoupal

## 🎯 Model Details

### Flood Prediction Model
- **Type:** Gradient Boosting Classifier
- **Features:** 17 input features
- **Output:** Flood probability (0-100%)
- **Prediction Window:** 3 days advance
- **Accuracy:** Optimized for Manipur's geographical and climatic conditions

### Landslide Prediction Model
- **Type:** [Add your model details]
- **Features:** [Add your feature list]
- **Output:** Risk level and probability

## 📝 Notes

1. **Auto-detection:** The flood model auto-detects season based on current date if not specified
2. **Default Values:** If advanced parameters are not provided, the model uses reasonable defaults based on season
3. **Grid Resolution:** Landslide analysis uses optimized grid sizes (4-6 points) per district for balanced speed and accuracy

## 🤝 Contributing

To improve the dashboard:
1. Add more districts to the `DISTRICTS` dictionary
2. Enhance visualization (add heatmaps, contour plots)
3. Integrate real-time weather APIs
4. Add historical data comparison

## 📄 License

[Add your license information]

## 👥 Authors

[Add your team/author information]

---

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the model documentation in `model_export/README.md`
3. Contact the development team

**Last Updated:** January 30, 2026