# src/notifier.py
import subprocess
import time
from datetime import datetime

def show_popup(title: str, message: str):
    """Dispara um pop-up nativo do macOS com som de alerta por cima de todas as janelas."""
    # Escapar aspas duplas para não quebrar o AppleScript
    safe_title = title.replace('"', '\\"')
    safe_msg = message.replace('"', '\\"')
    
    script = f'''
    tell application "System Events"
        activate
        display alert "{safe_title}" message "{safe_msg}" as informational buttons {{"Entendido"}} default button "Entendido"
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=False)

def run_scheduler(schedule: list):
    """
    Percorre a lista de blocos do dia e dorme até à hora de cada um.
    schedule: lista de dicts com {"time": "HH:MM", "title": "...", "message": "..."}
    """
    now = datetime.now()
    
    for item in schedule:
        block_time_str = item["time"]
        hour, minute = map(int, block_time_str.split(":"))
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Se o bloco ainda não passou hoje
        wait_seconds = (target_time - datetime.now()).total_seconds()
        if wait_seconds > 0:
            time.sleep(wait_seconds)
            show_popup(item["title"], item["message"])

if __name__ == "__main__":
    # Teste rápido se executado diretamente
    show_popup("🎯 Teste de Bloco", "Isto é um teste do teu notificador de foco e pausas.")