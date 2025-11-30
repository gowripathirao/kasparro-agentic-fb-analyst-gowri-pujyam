import os
import pandas as pd
from utils import save_json, now_str

class Generator:
    def __init__(self, df, eval_results, out_dir):
        self.df = df.copy()
        self.eval = eval_results
        self.out = out_dir
        os.makedirs(self.out, exist_ok=True)

    def run_all(self):
        self.make_insights()
        self.make_creatives()
        self.make_report()

    def make_insights(self):
        insights = {}
        insights['meta'] = {'generated_at': now_str()}
        insights['summary'] = self.eval.get('kpis', {})

        # Top performing ads by CTR
        if 'ad_id' in self.df.columns:
            grp = self.df.groupby('ad_id').agg({'impressions':'sum','clicks':'sum','spend':'sum','purchases':'sum'}).reset_index()
            grp['ctr'] = grp.apply(lambda r: (r['clicks']/r['impressions']) if r['impressions']>0 else 0, axis=1)
            top = grp.sort_values('ctr', ascending=False).head(5)
            insights['top_ads_by_ctr'] = top[['ad_id','ctr','spend']].to_dict(orient='records')

        save_json(insights, os.path.join(self.out, 'insights.json'))
        print('Saved insights.json')

    def make_creatives(self):
        # Generate simple creative recommendations (3 variants)
        creatives = []
        creatives.append({
            'id': 'creative_variation_1',
            'headline': 'Comfort-first undergarments — Try 3 for 2',
            'body': 'Soft, breathable fabric designed for everyday comfort.',
            'reasoning': 'High CTR ads mention comfort in copy (data-driven).'
        })
        creatives.append({
            'id': 'creative_variation_2',
            'headline': 'Invisible fit. All day confidence.',
            'body': 'Lightweight, seamless design for any outfit.',
            'reasoning': 'Target younger demographics; emphasize stealth fit.'
        })
        creatives.append({
            'id': 'creative_variation_3',
            'headline': 'Eco fabric undergarments — gentle on skin, gentle on earth',
            'body': 'Sustainable materials; highlight certifications.',
            'reasoning': 'Sustainability angle to improve brand lift.'
        })

        save_json({'creatives': creatives, 'generated_at': now_str()}, os.path.join(self.out, 'creatives.json'))
        print('Saved creatives.json')

    def make_report(self):
        lines = []
        lines.append('# Campaign Diagnostics Report')
        lines.append('Generated at: ' + now_str())
        lines.append('\n## Executive Summary')
        kpis = self.eval.get('kpis', {})
        lines.append(f"Total impressions: {kpis.get('impressions', 'N/A')}")
        lines.append(f"Total clicks: {kpis.get('clicks', 'N/A')}")
        lines.append(f"CTR: {kpis.get('ctr', 'N/A')}")
        lines.append('\n## Observations')
        if self.eval.get('anomalous_ads'):
            lines.append('- Found anomalous ads with very high CTR — inspect for bot traffic or mis-tagged events.')
        else:
            lines.append('- No high-CTR anomalies detected in primary checks.')

        lines.append('\n## Recommendations')
        lines.append('- Run post-click conversion quality check on top CTR ads.')
        lines.append('- A/B test the three creative variations in `creatives.json` for next 2 weeks.')
        lines.append('- Reallocate 10% of budget from low-CTR to top-CTR ads and monitor CPA changes.')

        report_path = os.path.join(self.out, 'report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print('Saved report.md')
