# Campaign Diagnostics Report

Generated at: 2025-11-30T11:45:00Z

## Executive Summary
Total impressions: 145320
Total clicks: 4120
CTR: 0.028351

## Observations
- Top ads by CTR are ad_17 and ad_3. Verify event tagging and post-click conversion tracking for these ads.
- No evidence of extreme bot-like CTR activity in primary checks, but continue monitoring for sudden spikes.

## Recommendations
- Run post-click conversion quality check on top CTR ads.
- A/B test the three creative variations in `creatives.json` for the next 2 weeks (split by audience: 18-24, 25-34, 35-44).
- Reallocate 10% of budget from lowest-performing quartile to top-performing ads and monitor CPA changes.
- Add server-side event verification for purchases to reduce attribution leakage.
