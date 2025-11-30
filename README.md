# kasparro-agentic-fb-analyst-gowri-pujyam

Mini production-grade agentic pipeline for the Kasparro Agentic Facebook Ads Analyst assignment.

## Structure

```
/data/
/agents/
/outputs/
/logs/
README.md
requirements.txt
EVAL_CHECKLIST.md
```

## Quickstart

1. Clone repo
2. Put `synthetic_fb_ads_undergarments.csv` into `data/`
3. Create and activate a Python venv
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

4. Run the planner (which triggers pipeline):
```bash
python agents/planner.py --data-path data/synthetic_fb_ads_undergarments.csv --out outputs/
```

5. Outputs will appear in `outputs/`: `insights.json`, `creatives.json`, `report.md`

## Deliverables for submission
- `insights.json`
- `creatives.json`
- `report.md`
- Public GitHub repo with tag `v1.0`
