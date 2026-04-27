# 📈 E-commerce User Funnel & Cohort Analyzer

An interactive web application for analyzing user behavior in e-commerce products. Drop in user event data and instantly see two of the most important product-analytics views: **purchase funnel drop-offs** and **cohort retention curves**.

🔗 **Live demo:** (https://funnel-cohort-akshay.streamlit.app/)

---

## 🎯 What This Project Does

This tool answers the two questions every product team starts with:

1. **"Where in the user journey are we losing people?"** → Funnel analysis
2. **"Are the users we acquire actually sticking around?"** → Cohort retention analysis

It's the foundational toolkit a Product Analyst uses to evaluate user growth and monetization opportunities.

---

## 🛠️ Tech Stack

- **Python** — pandas, numpy
- **Statistics** — funnel conversion math, cohort retention pivots
- **Streamlit** — interactive web UI
- **matplotlib / seaborn** — visualization
- **Deployed on** Streamlit Community Cloud

---

## 🚀 Quick Start

### Run locally

```bash
git clone https://github.com/AkshaySarwade/funnel-cohort-analyzer.git
cd funnel-cohort-analyzer

pip install -r requirements.txt

streamlit run app.py
```

Opens at `http://localhost:8501`.

### Or use the live demo

Visit the deployed app, upload your CSV (or use the simulated sample data with 2,000 users moving through realistic e-commerce stages), and explore.

---

## 📂 Input Data Format

Your CSV needs three columns:

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | string / int | Unique user identifier |
| `event_name` | string | e.g. `browse`, `add_to_cart`, `checkout`, `purchase` |
| `event_date` | datetime | When the event happened |

Example:

```csv
user_id,event_name,event_date
1,browse,2025-01-02 10:15:00
1,add_to_cart,2025-01-02 11:30:00
1,checkout,2025-01-02 12:00:00
1,purchase,2025-01-02 12:15:00
2,browse,2025-01-03 09:00:00
2,add_to_cart,2025-01-03 09:30:00
```

---

## 🪜 Funnel Analysis

For each ordered stage, the app calculates:

- **Users at stage** — unique user count
- **Stage conversion %** — what fraction of the previous stage made it here
- **Overall conversion %** — what fraction of the top-of-funnel reached this stage
- **Drop-off %** — the inverse of stage conversion

It then highlights the **biggest leak** — the stage transition with the largest drop-off. That's almost always the highest-leverage place to focus product work.

The math is simple but specific: at each step, count **only the users who reached every previous stage in order**. A user who skips `add_to_cart` and goes straight to `checkout` doesn't count for either, because that's not a real funnel.

---

## 📊 Cohort Retention Analysis

The app builds a retention table:

- **Rows:** each cohort (defined by acquisition week — the week of a user's first event)
- **Columns:** weeks since that cohort was acquired
- **Cells:** percentage of the cohort still active in that week (i.e. produced the chosen retention event)

Then it plots:

1. **Heatmap** — visualizes retention strength across cohorts and time
2. **Average retention curve** — the typical decay pattern across all cohorts

This is the key view for answering "is our product getting stickier over time?" If recent cohorts retain better than older ones, the product is improving. If they retain worse, you have a problem to investigate.

---

## 📈 What You'll See

1. **Configuration sidebar** — choose Funnel, Cohort, or Both
2. **Data preview** — verify your data loaded correctly
3. **Funnel section** — metrics, table, chart, and biggest-drop-off insight
4. **Cohort section** — cohort sizes, retention heatmap, average retention curve

---

## 🔬 The Logic

### Funnel conversion (per stage)

```
stage_conversion(i) = users_at_stage(i) / users_at_stage(i-1)
overall_conversion(i) = users_at_stage(i) / users_at_top
drop_off(i) = 1 - stage_conversion(i)
```

### Cohort retention

```
cohort = week of user's first event
retention(cohort, w) = unique active users in week w / cohort size
```

For most product use cases, weekly cohorts are the right granularity — daily is too noisy, monthly hides too much.

---

## 🔮 Future Enhancements

- [ ] Time-window filtering (last 30 days, last quarter)
- [ ] Segment funnels by user property (country, device, plan)
- [ ] Compare two cohorts side-by-side
- [ ] LTV calculation using cohort revenue data
- [ ] Anomaly detection on funnel drops (alert if drop-off jumps suddenly)

---

## 📚 Why I Built This

I work inside a production data pipeline and I've watched first-hand how much business decision-making depends on understanding *where* users drop off and *whether* retention is improving over time. Funnel and cohort analysis are the two tools every product analyst reaches for first — but a lot of teams build them ad-hoc in spreadsheets every time, which is error-prone and slow. I wanted to build a clean, reusable tool that makes both views available in one place, on real data, in seconds.

---

## 👤 Author

**Akshay Sarwade**
🔗 [LinkedIn](https://www.linkedin.com/in/akshay0sarwade) • [GitHub](https://github.com/AkshaySarwade) • akshaysarwade00@gmail.com

---

## 📄 License

MIT — feel free to fork, learn from, and build on this.
