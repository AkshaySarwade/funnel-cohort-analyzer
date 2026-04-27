# 🗓️ Build Plan — Funnel & Cohort Analyzer

This is your second project. You already know the workflow from the A/B Test Analyzer, so this should be **faster — about 6-8 hours over a weekend.**

---

## ✅ FILES IN THIS PACKAGE

- `app.py` — full Streamlit application (already tested, works)
- `requirements.txt` — relaxed versions for Streamlit Cloud
- `runtime.txt` — pins Python 3.11 (avoids the trap we hit last time)
- `README.md` — production-ready, just plug in your live URL
- `sample_data.csv` — small test dataset
- This plan

---

## 🚀 STEP-BY-STEP

### Step 1 — Set up the project (10 min)

```bash
# In Anaconda Prompt
cd C:\Users\admin

# Create the project folder
mkdir funnel-cohort-analyzer
cd funnel-cohort-analyzer
```

Copy the 5 files from this package into the folder.

### Step 2 — Run it locally (5 min)

```bash
streamlit run app.py
```

Browser opens at `http://localhost:8501`. Use sample data — you should see funnel metrics, a horizontal bar chart, and a cohort heatmap.

**Take screenshots as you scroll through.**

### Step 3 — Understand the code (1 hour)

Read through `app.py` slowly. The two functions you MUST understand are:

**`calculate_funnel(df, stages)`** — What it does:
- For each stage in order, it finds the unique users who reached it
- A user counts at stage N **only if they also reached stages 1 through N-1**
- This means it tracks the *true* funnel, not just stage counts

**`build_cohort_table(df, event_name)`** — What it does:
- For each user, finds their first event date → that's their "cohort week"
- Joins this back to all events
- Calculates `weeks_since_acquisition` for every event
- Pivots into a table: rows = cohort week, columns = weeks since, values = unique users
- Divides by cohort size → retention percentages

If something is unclear, paste the function back to me and I'll walk through it line by line.

### Step 4 — Find a real Kaggle dataset (30 min)

Search Kaggle for: **"e-commerce events" OR "user behavior"**

Top picks:

1. **"E-Commerce Behavior Data from a Multi-Category Store"** (Kechinov) — 285M rows, has `event_type` (view, cart, purchase) and `user_id`. Massive but you can sample 100K rows.
2. **"Online Retail II"** (UCI) — 1M+ transactions with InvoiceDate, CustomerID
3. **"Brazilian E-Commerce by Olist"** — Olist marketplace data

**Quick adjustment if dataset columns don't match:** rename the columns in pandas before saving:

```python
import pandas as pd
df = pd.read_csv('events.csv').sample(50000)
df = df.rename(columns={
    'event_type': 'event_name',
    'event_time': 'event_date'
})
df[['user_id', 'event_name', 'event_date']].to_csv('cleaned.csv', index=False)
```

### Step 5 — Push to GitHub (15 min)

Same flow as last time:

```bash
git init
git add .
git commit -m "Initial commit: Funnel & Cohort Analyzer"
git branch -M main
git remote add origin https://github.com/AkshaySarwade/funnel-cohort-analyzer.git
git push -u origin main
```

(Create the repo on github.com/new first, named `funnel-cohort-analyzer`.)

### Step 6 — Deploy on Streamlit Cloud (10 min)

Same as last time: share.streamlit.io → Create app → select repo → main → app.py → Deploy.

Subdomain suggestion: `funnel-cohort-akshay` or `akshay-funnel-cohort`.

Should be **fast this time** — runtime.txt pins Python 3.11, requirements.txt is relaxed.

### Step 7 — Polish (30 min)

1. Replace `[your-streamlit-cloud-link-here]` in README with your actual URL
2. Add screenshots to a `docs/` folder
3. Final commit & push

---

## 🎤 Interview Talking Points

**"Walk me through the funnel logic"**

> "The key thing about a real funnel is that you can't just count users at each event — you have to count users who reached **every previous stage in order**. So at each step I take the intersection of users at this stage with users from the previous stage. That gives you the true conversion path. The biggest drop-off is the largest stage-to-stage loss, and that's almost always the highest-leverage product fix."

**"How does cohort retention work?"**

> "Each user's cohort is defined by the week of their first event — that's their acquisition. For every later event, I calculate weeks-since-acquisition. Pivot that into rows = cohort, columns = weeks since, and you get a retention matrix. Divide by cohort size and you have retention percentages. The heatmap shows which cohorts retain better, and the average curve shows the typical decay pattern."

**"What's the difference between weekly and monthly cohorts?"**

> "Weekly is usually the right granularity — daily is too noisy, monthly hides too much. If you're measuring a high-frequency product like a daily-use app, you might go daily. For something with a longer cycle like SaaS billing, monthly might be enough. Weekly is the safe default."

**"What would you add next?"**

> "Three things — first, time-window filtering so you can compare 'this quarter' vs 'last quarter'. Second, segment-level funnels — splitting by country, device, or plan, because funnels often look very different across segments. Third, anomaly detection on the funnel drop-offs themselves, so the team gets alerted when conversion suddenly tanks."

---

## ✋ AFTER THIS IS LIVE

Update your resume — add this project alongside the A/B Test Analyzer. Your **two-project bundle** is now genuinely impressive for a Product Analyst role:

> 1. **A/B Test Analyzer** — experiment design, hypothesis testing, ship recommendations
> 2. **Funnel & Cohort Analyzer** — user behavior, drop-off analysis, retention curves

Together, that's the full toolkit a Product Analyst uses on day one.

I'll rebuild the A1apps resume with this project added — but **only after it's live**. Recruiters click. Don't promise what isn't there yet.

---

## 🚦 Done When

- [ ] App runs locally
- [ ] You can explain `calculate_funnel` and `build_cohort_table` line by line
- [ ] Real Kaggle dataset loaded successfully
- [ ] Code pushed to GitHub
- [ ] Deployed to Streamlit Cloud (live URL works)
- [ ] Screenshots in README
- [ ] You can answer the 4 interview questions without notes

When all 7 are checked, ping me. We rebuild the A1apps resume with both projects featured.

Jay Bhim, Akki. Second one is faster than the first. Go.
