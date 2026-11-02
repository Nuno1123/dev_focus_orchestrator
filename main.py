# main.py
import sys
from src.evaluate_state import generate_daily_plan
from src.debrief import run_debrief

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "start":
        plan = generate_daily_plan("context.json")
        with open("daily_plan.md", "w") as f:
            f.write(plan)
        print(plan)
        print("\n✅ Plano gerado em daily_plan.md!")
        
    elif sys.argv[1] == "end":
        run_debrief("context.json")

if __name__ == "__main__":
    main()