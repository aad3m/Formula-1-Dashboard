[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://<your-app-subdomain>.streamlit.app)
# 🏁 Modern Formula 1 Dashboard

A **live Formula 1 analytics dashboard** built with **Streamlit + Plotly**, powered by the **Jolpica F1 API** — a fully *Ergast-compatible* replacement since Ergast shut down in 2024.

---

## 🚀 Features

✅ **Live data** from Jolpica (schedule, standings, race results)  
✅ **Clean, responsive UI** with modern KPIs and charts  
✅ **Fantasy Helper tab** with tunable scoring based on form & consistency  
✅ **Offline mode** if API is unreachable (no crashes!)  
✅ **Modular codebase** — data, services, and UI split across folders  
✅ **Automated tests + CI** via GitHub Actions  

---

## 📂 Project Structure
```f1-dashboard/
├─ app.py                     # Streamlit entrypoint
├─ requirements.txt
├─ .streamlit/config.toml      # Theme & server setup
├─ src/
│  └─ f1dash/
│     ├─ config.py
│     ├─ utils/http.py
│     ├─ data/
│     │  ├─ client.py
│     │  └─ providers/jolpica.py
│     ├─ services/fantasy.py
│     └─ ui/layout.py
└─ tests/
├─ test_http.py
├─ test_client.py
├─ test_fantasy.py
├─ test_schedule.py
└─ conftest.py
```

---

## 🧰 Installation

```bash
# 1️⃣ Clone the repo
git clone https://github.com/aad3m/formula-1-dashboard.git
cd formula-1-dashboard

# 2️⃣ Create a virtual environment
python -m venv .venv
source .venv/bin/activate     # or .venv\Scripts\activate on Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt
```

## 🏎️ Run the App
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser.


## ⚙️ Data Source
This dashboard uses Jolpica F1 API, a drop-in replacement for the discontinued Ergast API.

## 🧱 Tech Stack
	•	Streamlit — interactive web app framework
	•	Plotly Express — rich charts
	•	Pandas — data manipulation
	•	Jolpica F1 API — Ergast-compatible data
	•	Pytest — unit testing framework
	•	GitHub Actions — CI/CD automation