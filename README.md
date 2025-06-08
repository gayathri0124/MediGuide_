# 🩺 MediGuide – Your AI-Powered Health Assistant

**MediGuide** is a smart healthcare assistant built with **Streamlit**. It allows users to search hospitals, predict diseases from symptoms, receive medicine recommendations, view interactive hospital maps, and explore Indian government health schemes.

---

## 🚀 Features 

- 🔍 **Hospital Search**  
  Search for hospitals by **state**, **city**, or **pincode** using built-in filters.

- 🧠 **Disease Prediction**  
  Enter symptoms from a list of 130+ medical conditions. An ML model will suggest a likely disease.

- 💊 **Medicine Recommendation**  
  Recommend suitable drugs using a similarity-based engine trained on drug-condition relationships.

- 🗺️ **Interactive Hospital Maps**  
  View the exact location of selected hospitals with **Folium-based maps** inside Streamlit.

- 📜 **Government Schemes**  
  Explore central and state-level health-related schemes and their eligibility.

---

## 🧠 Technologies Used

- **Frontend/UI**: Streamlit, HTML/CSS (custom styling inside Streamlit)
- **Machine Learning**: Scikit-learn, Joblib, Pickle
- **Maps**: Folium, Streamlit-Folium
- **Data Handling**: Pandas, CSV
- **Logic Modules**: Python (`help.py`, `pp.py`)
- **Model Storage**: `drugs_dict.pkl`, `similarity.pkl`, `random_f.joblib`

---

## ⚙️ Getting Started

To run MediGuide locally:

### 1. Clone the repository
```bash
git clone https://github.com/gayathri0124/MediGuide.git
cd MediGuide

python -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate

pip install -r requirements.txt

streamlit run MediGuide.py

```

---

“Health is Wealth” – MediGuide bridges the gap between symptoms and solutions with smart healthcare tools.

