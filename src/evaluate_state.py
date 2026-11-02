# src/evaluate_state.py
import json
from datetime import datetime
from src.monday_radar import get_monday_radar

def get_schedule_blocks(p0_tasks, p1_tasks):
    first_task = p0_tasks[0]['name'] if p0_tasks else (p1_tasks[0]['name'] if p1_tasks else "Milestone Técnico")
    second_task = p1_tasks[0]['name'] if (p0_tasks and p1_tasks) else "Hands-on & PoC"

    return [
        {
            "time": "09:30",
            "type": "Foco 1",
            "title": "🎯 Foco 1: " + first_task[:30],
            "message": f"Tarefa: {first_task}\nObjetivo: Fechar pendência crítica / teste unitário.",
            "deliverable": "Módulo liquidado / teste unitário"
        },
        {
            "time": "10:20",
            "type": "Pausa",
            "title": "☕ Pausa Ativa (15 min)",
            "message": "Larga o teclado e afasta-te do monitor. Vai buscar café/água e caminha um pouco.",
            "deliverable": "Desconexão total"
        },
        {
            "time": "10:35",
            "type": "Foco 2",
            "title": "🎯 Foco 2: " + second_task[:30],
            "message": f"Tarefa: {second_task}\nObjetivo: Hands-on / Implementação prática.",
            "deliverable": "Notas estruturadas ou commit local"
        },
        {
            "time": "11:25",
            "type": "Micro-Pausa",
            "title": "🧘 Micro-Pausa (10 min)",
            "message": "Alongamentos rápidos e reset de postura.",
            "deliverable": "Reset de foco"
        },
        {
            "time": "11:35",
            "type": "Foco 3",
            "title": "🎯 Foco 3: Engenharia Prática",
            "message": "Aprofundar SDD ou construção de ferramentas Kiro.",
            "deliverable": "Spec ou código implementado"
        },
        {
            "time": "12:45",
            "type": "Almoço",
            "title": "🍽️ Hora de Almoço (1h15)",
            "message": "Pausa para almoço e descanso completo até às 14h00.",
            "deliverable": "Baterias recarregadas"
        },
        {
            "time": "14:00",
            "type": "Foco 4",
            "title": "🎯 Foco 4: Construção / Laboratório",
            "message": "Bloco pós-almoço: trabalho prático direto no código.",
            "deliverable": "Funcionalidade validada"
        },
        {
            "time": "14:50",
            "type": "Pausa",
            "title": "🚶 Pausa Ativa (15 min)",
            "message": "Combate a quebra de energia da tarde com movimento físico.",
            "deliverable": "Caminhada curta"
        },
        {
            "time": "15:05",
            "type": "Foco 5",
            "title": "🎯 Foco 5: Consolidação & Testes",
            "message": "Refactoring, documentação de specs e limpeza de código.",
            "deliverable": "Código limpo e documentado"
        },
        {
            "time": "16:00",
            "type": "Micro-Pausa",
            "title": "☕ Micro-Pausa (15 min)",
            "message": "Descompressão final antes da última hora.",
            "deliverable": "Respiro mental"
        },
        {
            "time": "16:15",
            "type": "Buffer",
            "title": "🛡️ Bloco Buffer / Overflow",
            "message": "Resolução de imprevistos do dia ou exploração de novas ferramentas.",
            "deliverable": "Sem pendências para amanhã"
        },
        {
            "time": "17:15",
            "type": "Debrief",
            "title": "🏁 Fim do Dia: Debrief",
            "message": "Abre o terminal e corre 'python3 main.py end' para atualizar o context.json.",
            "deliverable": "context.json sincronizado"
        }
    ]

def generate_daily_plan(context_path="context.json"):
    with open(context_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    today = datetime.now().date()
    p0_urgent = []
    p1_regular = []

    for track in data.get("trainings", []):
        modules = track.get("modules", [track])
        for mod in modules:
            if mod.get("status") != "done":
                deadline_str = mod.get("deadline")
                hours = mod.get("estimated_hours_left", 1)
                name = mod.get("name", track.get("track", "Módulo"))

                if deadline_str:
                    dl = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                    if (dl - today).days <= 2:
                        p0_urgent.append({"name": name, "hours": hours, "deadline": deadline_str})
                        continue
                p1_regular.append({"name": name, "hours": hours})

    schedule = get_schedule_blocks(p0_urgent, p1_regular)
    radar_content = get_monday_radar()

    md = [f"# 📅 Plano Diário - {today.strftime('%d/%m/%Y')}\n"]
    if radar_content:
        md.append(radar_content)

    md.append("## 🎯 Prioridades do Dia")
    if p0_urgent:
        for item in p0_urgent:
            md.append(f"- 🔴 **[P0 - Prazo Crítico]** {item['name']} — {item['hours']}h restantes (Deadline: {item['deadline']})")
    for item in p1_regular:
        md.append(f"- 🟡 **[P1 - Regular]** {item['name']} — {item['hours']}h restantes")
    if not p0_urgent and not p1_regular:
        md.append("- 🟢 Todas as tarefas em dia!")

    md.append("\n---\n")
    md.append("## ⏱️ Grelha de Execução (Blocos 50/10)\n")
    md.append("| Horário | Bloco | Objetivo / Tarefa | Entregável Mensurável |")
    md.append("| :--- | :--- | :--- | :--- |")

    for b in schedule:
        md.append(f"| **{b['time']}** | {b['type']} | {b['title']} | {b['deliverable']} |")

    return "\n".join(md), schedule