# Blueprint de Migração: Dev Focus Orchestrator (CLI macOS ➔ React Native SDD)

## 1. Visão Geral do Produto

O **Dev Focus Orchestrator** é uma aplicação desenhada para programadores que dispersam facilmente quando confrontados com tarefas teóricas, ambíguas ou sem prazo fechado. O seu propósito é forçar clareza diária através de:
1. **Priorização determinística:** Ordenação estrita de prioridades baseada em prazos reais (P0/P1/P2) sem depender de decisões subjetivas diárias.
2. **Ciclos de Foco 50/10:** Estrutura horária rígida (09h30–17h30) com blocos de 50 minutos de trabalho e 10–15 minutos de pausa obrigatória ativa.
3. **Notificações Ativas:** Alarmes e notificações locais disparadas a cada transição de bloco (focos e pausas).
4. **Digest Semanal (Monday Tech Radar):** Injeção condicional de novidades de SDD e AI Development às segundas-feiras.
5. **Debrief de Fecho:** Checkout interativo às 17h15 para sincronizar o progresso no estado local.

---

## 2. Contratos de Dados (TypeScript Schemas)

Estes contratos devem ser integrados na camada de tipos do boilerplate (`types/planner.ts`):

```typescript
export type ModuleStatus = "not_enrolled" | "enrolled" | "in_progress" | "done" | "pending";
export type TaskPriority = "p0" | "p1" | "p2" | "p3";

export interface TrainingModule {
  name: string;
  status: ModuleStatus;
  current: boolean;
  deadline: string | null; // ISO YYYY-MM-DD
  estimated_hours_left: number | null;
}

export interface TrainingTrack {
  track: string;
  modules?: TrainingModule[];
  status?: ModuleStatus;
  current?: boolean;
  deadline?: string | null;
  estimated_hours_left?: number | null;
}

export interface ProjectTask {
  id: string;
  title: string;
  deliverable: string;
  estimated_hours: number;
  priority: "high" | "medium" | "low";
  status: "todo" | "in_progress" | "done";
}

export interface AppState {
  in_project: boolean;
  project_name: string | null;
  project_tasks: ProjectTask[];
  trainings: TrainingTrack[];
  next_milestones: string[];
}

export interface ScheduleBlock {
  id: string;
  time: string;           // "HH:MM"
  endTime: string;        // "HH:MM"
  type: "focus" | "break" | "lunch" | "buffer" | "debrief";
  title: string;
  message: string;
  deliverable: string;
  priorityLevel?: TaskPriority;
}
```

---

## 3. Regras de Negócio e Motor Determinístico

A lógica de negócio deve residir em funções puras (ex.: `src/core/scheduler.ts`):

### 3.1. Hierarquia de Precedência
1. **P0 (Urgente / Bloqueador):**
   * Condição: Tarefa ou módulo com `deadline` a $\le 48\text{ horas}$ da data atual e `status != 'done'`.
   * Ação: Ocupa imperativamente o **Bloco 1 (09h30–10h20)**.
2. **P1 (Operação Primária):**
   * Se `in_project === true`: Tarefas de projeto ocupam 70% a 80% dos blocos disponíveis.
   * Se `in_project === false`: Módulos de formação ativos com menor `estimated_hours_left` (fechos rápidos de dopamina).
3. **P2 (Milestones Técnicos / Hands-on):**
   * Tópicos da lista `next_milestones`.
   * Obrigatório ter entregável tangível (PoC, spec, commit ou teste).
4. **P3 (Backlog Frio):**
   * Módulos sem prazo iminente ou em estado `not_enrolled`.

### 3.2. Estrutura Temporal Fixa (09h30 – 17h30)

| Início | Fim | Tipo | Duração | Descrição Típica |
| :--- | :--- | :--- | :--- | :--- |
| **09h30** | **10h20** | `focus` | 50m | Bloco 1: Prioridade P0 (crítica) ou P1 principal |
| **10h20** | **10h35** | `break` | 15m | Pausa Ativa: Afastar do ecrã, hidratação/café |
| **10h35** | **11h25** | `focus` | 50m | Bloco 2: Hands-on / Implementação prática |
| **11h25** | **11h35** | `break` | 10m | Micro-Pausa: Reset postural e respiração |
| **11h35** | **12h45** | `focus` | 70m | Bloco 3: Engenharia Prática & SDD |
| **12h45** | **14h00** | `lunch` | 75m | Almoço: Desconexão obrigatória |
| **14h00** | **14h50** | `focus` | 50m | Bloco 4: Construção / Laboratório de código |
| **14h50** | **15h05** | `break` | 15m | Pausa Ativa: Caminhada / combate ao sono pós-prandial |
| **15h05** | **16h00** | `focus` | 55m | Bloco 5: Testes, refactoring e consolidação |
| **16h00** | **16h15** | `break` | 15m | Micro-Pausa: Café e respiro mental |
| **16h15** | **17h15** | `buffer`| 60m | Buffer: Resolução de derrapagens sem culpa |
| **17h15** | **17h30** | `debrief`| 15m | Fecho: Check-out diário e sincronização de dados |

### 3.3. Gatilho de Segunda-Feira (Monday Tech Radar)
* Se `new Date().getDay() === 1`:
  * A app injeta um card/bloco no topo da visualização diária com 3 novidades sintetizadas em:
    * **SDD (Spec-Driven Development)**
    * **AI Agents & Workflows**
    * **Mobile & Architecture**
  * Cada item apresenta: Resumo (3 linhas) + botão "Aprofundar" (que expande exemplos de implementação).

---

## 4. Requisitos para a App React Native

### 4.1. Persistência Local (Local-First)
* Utilizar o mecanismo de storage padrão do boilerplate da empresa (ex.: MMKV, AsyncStorage ou SQLite local).
* O estado inicial deve poder ser importado via JSON ou configurado num ecrã de definições.

### 4.2. Sistema de Notificações Push Locais
A app não requer servidor backend; utiliza agendamento local de notificações (ex.: via Notifee ou Expo Notifications, conforme o boilerplate):
1. **Ao abrir a app ou às 09h30:**
   * O motor calcula os blocos do dia.
   * Cancela agendamentos anteriores e cria notificações locais para cada entrada de `ScheduleBlock`.
2. **Formato das Notificações:**
   * **Início de Foco:** `[🎯 FOCO] {Título do Bloco}` — *"Entregável: {deliverable}"*.
   * **Pausa:** `[☕ PAUSA ATIVA] Afasta-te do ecrã!` — *"Tens 15 min de descanso. Levanta-te e bebe água."*.
   * **Almoço:** `[🍽️ HORA DE ALMOÇO] Baterias a recarregar até às 14h00."*.
   * **Debrief (17h15):** `[🏁 CHECK-OUT] Abre a app para registar o progresso do dia."*.
3. **Ações Rápidas (Interactive Notifications):**
   * A notificação das 17h15 deve permitir tocar para abrir diretamente o ecrã modal de Debrief.

### 4.3. Ecrãs Necessários (Fluxo UI)
1. **Home / Timeline Diária:**
   * Indicador visual do bloco ativo no momento (com barra de progresso do bloco).
   * Lista cronológica de blocos 50/10 do dia.
   * Banner superior do *Monday Tech Radar* visível apenas às segundas-feiras.
2. **Modal / Fluxo de Debrief (17h15):**
   * Lista checklist de tarefas e módulos trabalhados no dia.
   * Opções: *"Concluído"*, *"Ainda em curso (quantas horas faltam?)"*.
   * Botão final: *"Encerrar Dia"*, que atualiza o storage local e desliga alertas até ao dia seguinte.
3. **Gestão de Backlog / Formações:**
   * Visualização das tracks e módulos com deadlines, permitindo alterar estados (`enrolled`, `done`, datas limite).

---

## 5. Roteiro de Execução com o Kiro sobre o Boilerplate

Quando tiveres acesso ao boilerplate da empresa amanhã, o fluxo com o Kiro segue a metodologia SDD:

1. **Step 1: Ingestão de Arquitetura**
   * Abre o boilerplate e pede ao Kiro:
     > *"Analisa este repositório boilerplate (state management, router, design tokens e storage). Mapeia onde devem residir os modelos do 'dev-focus-orchestrator' respeitando as guidelines internas."*
2. **Step 2: Core Domain (Sem UI)**
   * Pedir ao agente de implementação do Kiro para criar:
     * O ficheiro `types/planner.ts`.
     * As funções puras `calculateSchedule(state: AppState): ScheduleBlock[]`.
     * Testes unitários Jest para garantir que o módulo que expira em $\le 48\text{h}$ fica sempre no primeiro bloco.
3. **Step 3: Notificações Locais**
   * Configurar a biblioteca de notificações do boilerplate com a função `scheduleDayNotifications(blocks: ScheduleBlock[])`.
4. **Step 4: UI / Componentes**
   * Criar os componentes consumindo os design tokens e UI kits internos do boilerplate:
     * `<BlockTimeline />`
     * `<ActiveBlockCard />`
     * `<MondayRadarCard />`
     * `<DebriefModal />`
5. **Step 5: Validação com Agente Revisor do Kiro**
   * Executar o agente de revisão para validar se o código gerado respeita o linting, formatação e convenções estritas da empresa.