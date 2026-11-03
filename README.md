# 🎯 Dev Focus Orchestrator

> Orquestrador diário e determinístico de produtividade e foco para engenharia de software no macOS.

O **Dev Focus Orchestrator** foi desenhado para combater a dispersão e a paralisia de análise em períodos de trabalho teórico, estudo aprofundado (upskilling, certificações, arquitetura) ou tarefas sem prazos fechados. Elimina a fadiga de decisão diária ao calcular deterministicamente a prioridade de cada bloco de trabalho e aplicar disciplina temporal através de pop-ups nativos do macOS.

---

## ⚡ Filosofia Central

- **Determinismo estrito:** Zero dependência de IA em runtime para planear o dia. O agendamento baseia-se em prazos reais (`deadline`), estimativas de esforço e regras matemáticas de precedência.
- **Ritmo 50/10 estruturado:** Jornada fixa (09h30 – 17h30) dividida em blocos de foco de 50 minutos alternados com pausas ativas obrigatórias para prevenir esgotamento cognitivo.
- **Interrupção ativa do ecrã:** Pop-ups nativos do macOS (`System Events`) sobrepõem-se ao IDE ou browser nas mudanças de bloco e início de pausas.
- **Spec-Driven Development (SDD):** Estado do utilizador centralizado num único contrato JSON (`context.json`) sincronizado em cada fecho de dia.

---

## 🚀 Funcionalidades

- **Motor de Prioridades P0–P3:**
  - **P0 (Crítico):** Qualquer módulo ou tarefa com entrega em $\le 48\text{h}$ assume automaticamente o primeiro bloco de foco da manhã (09h30).
  - **P1 (Operação Primária):** Módulos ativos com menor esforço restante (quick-wins) ou tarefas de projeto ativo.
  - **P2 / P3:** Hands-on técnico com entregável tangível obrigatório (PoC, spec ou commit) e backlog frio.
- **Monday Tech Radar:** Injeção condicional automática de atualizações técnicas (SDD, Agentes de IA e Arquitetura) exclusivamente às segundas-feiras.
- **Debrief Interativo (17h15):** Terminal interativo de check-out que recolhe horas despendidas, atualiza o progresso e marca entregas como concluídas no `context.json`.
- **Automação Nativa no macOS:** Integração via `launchd` combinada com ficheiros `.command` executados via `/usr/bin/open`, contornando restrições de permissões (TCC) do sistema.

---

## 📂 Estrutura do Projeto

```text
dev_focus_orchestrator/
├── context.json              # Fonte de verdade do estado (tarefas, formações, prazos)
├── daily_plan.md             # Plano diário gerado em Markdown (visualização limpa)
├── spec.md                   # Especificação formal da arquitetura e regras de negócio
├── main.py                   # Ponto de entrada da CLI
├── start.command             # Script executável do macOS para arranque (09h30)
├── end.command               # Script executável do macOS para debrief (17h15)
└── src/
    ├── __init__.py
    ├── evaluate_state.py     # Motor determinístico de cálculo de blocos e plano
    ├── monday_radar.py       # Gerador condicional do radar semanal
    ├── notifier.py           # Gestor de pop-ups nativos do macOS em background
    └── debrief.py            # Assistente de fecho de dia e sincronização de dados
```

---

## 🛠️ Instalação e Requisitos

- **macOS** (testado em versões modernas com suporte a AppleScript / `System Events`).
- **Python 3.10+** (sem dependências externas pesadas no core).

### 1. Clonar o Repositório
```bash
git clone https://github.com/teu-utilizador/dev-focus-orchestrator.git
cd dev-focus-orchestrator
```

### 2. Tornar os Scripts Executáveis
```bash
chmod +x start.command end.command
```

---

## 💻 Utilização Manual (CLI)

```bash
# Iniciar o dia (gera o plano em daily_plan.md e ativa o notificador em background)
python3 main.py start

# Encerrar o dia (abre o debrief interativo e atualiza o context.json)
python3 main.py end

# Testar se os pop-ups nativos do macOS estão a funcionar
python3 main.py test-popup
```

---

## ⏰ Configuração da Automação no macOS (`launchd`)

Para que o orquestrador abra o terminal sozinho às **09h30** (planeamento) e às **17h15** (debrief), configura os seguintes `LaunchAgents`:

### 1. Criar o Agente da Manhã (`com.nuno.planner.start.plist`)
Grava em `~/Library/LaunchAgents/com.nuno.planner.start.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nuno.planner.start</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/open</string>
        <string>/Users/nunomonteiro/development/dev_focus_orchestrator/start.command</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    <key>StandardErrorPath</key>
    <string>/tmp/planner_start.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/planner_start.out</string>
</dict>
</plist>
```

### 2. Criar o Agente da Tarde (`com.nuno.planner.end.plist`)
Grava em `~/Library/LaunchAgents/com.nuno.planner.end.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nuno.planner.end</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/open</string>
        <string>/Users/nunomonteiro/development/dev_focus_orchestrator/end.command</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>17</integer>
        <key>Minute</key>
        <integer>15</integer>
    </dict>
    <key>StandardErrorPath</key>
    <string>/tmp/planner_end.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/planner_end.out</string>
</dict>
</plist>
```

### 3. Registar os Agentes no Sistema
```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.nuno.planner.start.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.nuno.planner.end.plist
```

---

## 📋 Modelo de Dados (`context.json`)

Exemplo da estrutura esperada pelo motor determinístico:

```json
{
  "in_project": false,
  "project_name": null,
  "project_tasks": [],
  "trainings": [
    {
      "track": "Track 1: Architecting Cloud Native AI Agents",
      "modules": [
        {
          "name": "AI Architecture & Systems Design",
          "status": "in_progress",
          "current": true,
          "deadline": "2026-11-03",
          "estimated_hours_left": 0.4
        }
      ]
    }
  ],
  "next_milestones": [
    "Criar PoC com Kiro CLI e hooks determinísticos",
    "Estruturar spec formal para migração React Native"
  ]
}
```

---

## 🗺️ Roadmap

- [x] Motor de priorização determinístico (09h30–17h30) em Python puro.
- [x] Tech Radar automático para segundas-feiras.
- [x] Pop-ups nativos no macOS para blocos e pausas ativas.
- [x] Automação completa sem bloqueios de segurança via `launchd` + `.command`.
- [ ] **Fase 2:** Migração da arquitetura para aplicação móvel em **React Native** com push notifications locais (consulta `REACT_NATIVE_MIGRATION_CONTEXT.md`).
- [ ] **Fase 3:** Conector opcional com API do Jira para preenchimento de `project_tasks` quando alocado em cliente.
