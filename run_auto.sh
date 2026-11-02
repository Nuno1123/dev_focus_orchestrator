cat << 'EOF' > run_auto.sh
#!/usr/bin/env bash

# Impede a execução ao fim de semana (1 = Segunda, 7 = Domingo)
DAY_OF_WEEK=$(date +%u)
if [ "$DAY_OF_WEEK" -gt 5 ]; then
  exit 0
fi

ACTION="${1:-start}"
PROJECT_DIR="/Users/nunomonteiro/development/dev_focus_orchestrator"

# Abre o Terminal do macOS em primeiro plano e corre o script
osascript <<APPLESCRIPT
tell application "Terminal"
    activate
    do script "cd $PROJECT_DIR && python3 main.py $ACTION"
end tell
APPLESCRIPT
EOF

chmod +x run_auto.sh