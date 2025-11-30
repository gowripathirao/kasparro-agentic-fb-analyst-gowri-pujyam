import numpy as np

class Evaluator:
    def __init__(self, df):
        self.df = df.copy()

    def run_checks(self):
        out = {}
        out['row_count'] = int(len(self.df))
        out['missing_values'] = {c: int(self.df[c].isna().sum()) for c in self.df.columns}

        # Basic KPI calculations (assumes columns: impressions, clicks, spend, purchases)
        for col in ['impressions', 'clicks', 'spend', 'purchases']:
            if col not in self.df.columns:
                out.setdefault('kpi_warnings', []).append(f'Missing column: {col}')

        # compute CTR and CPA if possible
        try:
            impressions = self.df['impressions'].sum()
            clicks = self.df['clicks'].sum()
            spend = self.df['spend'].sum()
            purchases = self.df['purchases'].sum()

            ctr = (clicks / impressions) if impressions > 0 else np.nan
            cpa = (spend / purchases) if purchases > 0 else np.nan
            avg_cpc = (spend / clicks) if clicks > 0 else np.nan

            out['kpis'] = {
                'impressions': int(impressions),
                'clicks': int(clicks),
                'spend': float(spend),
                'purchases': int(purchases),
                'ctr': float(ctr),
                'cpa': float(cpa) if not np.isnan(cpa) else None,
                'avg_cpc': float(avg_cpc) if not np.isnan(avg_cpc) else None
            }
        except Exception as e:
            out.setdefault('kpi_warnings', []).append('Failed to compute KPIs: ' + str(e))

        # Quick anomaly detection: campaigns with CTR > 0.3 or spend spikes
        try:
            df = self.df
            if 'ad_id' in df.columns:
                grouped = df.groupby('ad_id').agg({'impressions':'sum','clicks':'sum','spend':'sum'}).reset_index()
                grouped['ctr'] = grouped.apply(lambda r: r['clicks']/r['impressions'] if r['impressions']>0 else 0, axis=1)
                anomalies = grouped[grouped['ctr']>0.3]
                out['anomalous_ads'] = anomalies[['ad_id','ctr']].to_dict(orient='records')
        except Exception:
            out.setdefault('kpi_warnings', []).append('Anomaly detection failed')

        return out
