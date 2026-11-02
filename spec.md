# SPECIFICATION: Daily Focus & Priority Orchestrator (macOS CLI & Kiro Agent)

## 1. Visão Geral e Objetivos

O **Daily Focus & Priority Orchestrator** é uma ferramenta local de produtividade desenhada para programadores que operam em ciclos curtos de atenção e necessitam de metas acionáveis e pausas estritas.

O sistema corre localmente em macOS (com disparo automático via `launchd` às 09h30), consome o estado atual do utilizador a partir de um ficheiro `state.json`, aplica uma matriz determinística de priorização e gera uma agenda diária estruturada em blocos de foco (50 min) e pausas obrigatórias (10–15 min), terminando às 17h30.

### Objetivos Principais

- **Zero Ambiguity:** Nenhuma tarefa entra na agenda sem um entregável mensurável (ficheiro, teste, commit ou spec).
- **Priorização Determinística:** Separação entre cálculo de datas/prazos (Python/Node) e formatação/revisão contextual (Kiro LLM Agent).
- **Compatibilidade SDD:** Estrutura de dados pensada desde o início para partilha de contratos com o boilerplate interno de React Native da empresa.

---

## 2. Contrato de Dados (Schema)

O ficheiro central de estado é `~/.planner/state.json`.

```typescript
// types/planner.ts

export type ModuleStatus =
	| "not_enrolled"
	| "enrolled"
	| "in_progress"
	| "done"
	| "pending";

export interface TrainingModule {
	name: string;
	status: ModuleStatus;
	current: boolean;
	deadline: string | null; // Formato YYYY-MM-DD
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
}

export interface PlannerState {
	in_project: boolean;
	project_name: string | null;
	project_tasks: ProjectTask[];
	trainings: TrainingTrack[];
	next_milestones: string[];
}
```
