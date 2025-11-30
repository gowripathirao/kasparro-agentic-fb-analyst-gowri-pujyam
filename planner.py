"""Simple planner driver that reads data and calls evaluator + generator.
Usage: python agents/planner.py --data-path data/synthetic_fb_ads_undergarments.csv --out outputs/
"""
import argparse
import os
from utils import load_data
from evaluator import Evaluator
from generator import Generator

def main(data_path, out_dir):
    print('Planner: loading data ->', data_path)
    df = load_data(data_path)

    # Basic plan (in practice this would be more detailed)
    plan = {
        'tasks': [
            'compute_overall_kpis',
            'segment_by_creative',
            'detect_anomalies',
            'generate_creative_suggestions',
            'create_report'
        ]
    }

    evaluator = Evaluator(df)
    eval_results = evaluator.run_checks()

    generator = Generator(df, eval_results, out_dir)
    generator.run_all()

    print('Planner: pipeline finished. Outputs saved to', out_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', required=True)
    parser.add_argument('--out', dest='out_dir', default='outputs/')
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    main(args.data_path, args.out_dir)
