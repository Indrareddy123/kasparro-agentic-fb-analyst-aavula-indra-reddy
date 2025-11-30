import argparse
from src.orchestrator.pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Kasparro Agentic FB Analyst")
    parser.add_argument("query", type=str, help="User query, e.g. 'Analyze ROAS drop'")
    args = parser.parse_args()

    paths = run_pipeline(args.query)
    print("Done.")
    print("Insights:", paths["insights_path"])
    print("Creatives:", paths["creatives_path"])
    print("Report:", paths["report_path"])

if __name__ == "__main__":
    main()
