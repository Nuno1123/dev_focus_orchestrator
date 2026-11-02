  # src/monday_radar.py
import os
from datetime import datetime

def get_monday_radar() -> str:
    # 0 = Segunda-feira no datetime do Python
    if datetime.now().weekday() != 0:
        return ""

    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "\n> ⚠️ *Monday Radar ignorado: Nenhuma API Key configurada nas variáveis de ambiente.*\n\n"

    try:
        # Exemplo com API (ou podes usar o cliente da OpenAI/Anthropic aqui)
        # O prompt pede 3 itens rápidos em SDD / AI Dev / Mobile com comando para aprofundar
        radar_content = """
## 📡 Monday Tech Radar (15 min)
1. **Spec-Driven Agent Contracts:** Como usar schemas estritos para validar outputs de agentes antes de tocarem no código.
2. **Context Compaction:** Boas práticas para reduzir poluição de contexto em prompts longos.
3. **Local CLI Tools para Devs:** Integração limpa de scripts Python em workflows de terminal.

*Para aprofundar algum tema, pergunta ao Kiro ou corre o comando dedicado.*
--------------------------------------------------------------------------------
"""
        return radar_content
    except Exception as e:
        return f"\n> ⚠️ *Erro ao carregar o Monday Radar: {str(e)}*\n\n"