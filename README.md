# TravelTech B2B Support Agent

A small Streamlit college-project demo for B2B technical support.

## Run locally

```bash
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Deploy and share

1. Upload `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. Deploy the repository on Streamlit Community Cloud with `app.py` as the entry point.
3. Share the resulting URL with your group.

## Demo limitations

This prototype uses sample support scenarios and keyword/TF-IDF-style routing (scenario matching), not a real LLM, company manuals, account system, or ticketing backend. Tickets are simulated and not stored permanently. Replace example procedures with verified platform documentation before production use.
