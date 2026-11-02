import json
import os

def run_debrief(context_path="context.json"):
    if not os.path.exists(context_path):
        print(f"❌ Erro: Ficheiro '{context_path}' não encontrado.")
        return

    with open(context_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n=== 🏁 CHECK-OUT DO DIA (DEBRIEF) ===")
    updated = False

    # 1. Tarefas de Projeto (se existirem)
    project_tasks = data.get("project_tasks", [])
    if project_tasks:
        print("\n📋 Tarefas de Projeto:")
        for task in project_tasks:
            ans = input(f"Concluíste a tarefa '{task.get('title')}'? [s/n]: ").strip().lower()
            if ans in ["s", "sim", "y", "yes"]:
                task["status"] = "done"
                updated = True

    # 2. Formações e Módulos pendentes
    trainings = data.get("trainings", [])
    print("\n🎓 Formações e Módulos:")
    for track in trainings:
        # Se a track contiver submódulos
        if "modules" in track and isinstance(track["modules"], list):
            for mod in track["modules"]:
                if mod.get("status") != "done":
                    name = mod.get("name")
                    ans = input(f"Concluíste o módulo '{name}'? [s/n]: ").strip().lower()
                    if ans in ["s", "sim", "y", "yes"]:
                        mod["status"] = "done"
                        mod["estimated_hours_left"] = 0
                        mod["current"] = False
                        updated = True
                        print(f"  ✨ '{name}' marcado como concluído.")
                    else:
                        cur_hours = mod.get("estimated_hours_left", 0)
                        val = input(f"  Horas restantes (atual: {cur_hours}h) [Enter para manter]: ").strip()
                        if val:
                            try:
                                mod["estimated_hours_left"] = float(val)
                                updated = True
                            except ValueError:
                                print("  ⚠️ Valor inválido. Valor mantido.")
        else:
            # Se for uma track direta sem lista de módulos
            if track.get("status") != "done":
                name = track.get("track")
                ans = input(f"Concluíste a track '{name}'? [s/n]: ").strip().lower()
                if ans in ["s", "sim", "y", "yes"]:
                    track["status"] = "done"
                    track["estimated_hours_left"] = 0
                    track["current"] = False
                    updated = True
                    print(f"  ✨ '{name}' marcado como concluído.")
                else:
                    cur_hours = track.get("estimated_hours_left", 0)
                    val = input(f"  Horas restantes (atual: {cur_hours}h) [Enter para manter]: ").strip()
                    if val:
                        try:
                            track["estimated_hours_left"] = float(val)
                            updated = True
                        except ValueError:
                            print("  ⚠️ Valor inválido. Valor mantido.")

    # 3. Guardar alterações no context.json
    if updated:
        with open(context_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 '{context_path}' atualizado com sucesso!")
    else:
        print("\nNenhuma alteração registada.")

    print("\nDia encerrado. Fecha o terminal e descansa! 🚀\n")

if __name__ == "__main__":
    run_debrief()