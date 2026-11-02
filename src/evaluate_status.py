# src/evaluate_state.py
import json
from datetime import datetime
from src.monday_radar import get_monday_radar

def generate_daily_plan(context_path="context.json"):
    with open(context_path, "r") as f:
        data = json.load(f)

    # 1. Puxa as novidades se for 2ª feira
    radar_section = get_monday_radar()

    # 2. Avaliação determinística das tarefas (P0, P1, P2...)
    today = datetime.now().date()
    p0_tasks = []
    
    for track in data.get("trainings", []):
        for mod in track.get("modules", []):
            if mod.get("status") != "done":
                deadline_str = mod.get("deadline")
                if deadline_str:
                    dl = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                    if (dl - today).days <= 2:
                        p0_tasks.append(mod)

    # 3. Montagem do Markdown
    plan_md = f"# Plano Diário - {today.strftime('%d/%m/%Y')}\n\n"
    if radar_section:
        plan_md += radar_section
        
    plan_md += "## Prioridades Críticas Identificadas\n"
    for t in p0_tasks:
        plan_md += f"- **[P0]** {t['name']} (Prazo: {t['deadline']} | Falta: {t['estimated_hours_left']}h)\n"

    # Resto da lógica que gera a tabela com blocos 50/10...
    return plan_md