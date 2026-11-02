# main.py
import os
import subprocess
import sys
import json
from src.evaluate_state import generate_daily_plan
from src.debrief import run_debrief
from src.notifier import show_popup

PID_FILE = "/tmp/planner_notifier.pid"

def kill_previous_notifier():
    """Mata qualquer processo do notificador que ainda esteja a correr de dias anteriores."""
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 9)
        except Exception:
            pass
        finally:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)

def start_background_notifier(schedule):
    """Inicia o processo de background que vai agendar os pop-ups ao longo do dia."""
    kill_previous_notifier()

    # Guarda a agenda temporariamente para o subprocesso consumir
    schedule_file = "/tmp/current_schedule.json"
    with open(schedule_file, "w", encoding="utf-8") as f:
        json.dump(schedule, f)

    cmd = [
        sys.executable,
        "-c",
        f"import json; from src.notifier import run_scheduler; "
        f"schedule = json.load(open('{schedule_file}', 'r')); "
        f"run_scheduler(schedule)"
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True  # Garante que continua ativo após fechar o terminal
    )

    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "start"

    if action == "start":
        plan_md, schedule = generate_daily_plan("context.json")
        with open("daily_plan.md", "w", encoding="utf-8") as f:
            f.write(plan_md)
        print(plan_md)

        # Arranca o daemon de popups
        start_background_notifier(schedule)
        print("\n🔔 Notificador de pop-ups ativado para os blocos e pausas do dia!")

    elif action == "end":
        kill_previous_notifier()
        run_debrief("context.json")

    elif action == "test-popup":
        show_popup("🎯 Teste Imediato", "O sistema de pop-ups nativo está a funcionar corretamente!")
        print("✅ Pop-up de teste disparado com sucesso.")

if __name__ == "__main__":
    main()