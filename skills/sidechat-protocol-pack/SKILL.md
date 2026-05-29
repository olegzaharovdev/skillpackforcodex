---
name: sidechat-protocol-pack
description: Create or update a durable Russian-language Sidechat Protocol Pack and optional machine export when the user asks to close, preserve, protocol, hand off, recover, summarize, export, index, or continue a side conversation. Also use this skill when the user asks to save a protocol into an explicit folder path, for example "сохрани протокол в D:\\..." or "протокол D:\\...". Trigger on short Russian commands like "Сделай протокол", "запротоколлируй", or "протокол". Use for side chats, interrupted chats, architectural decisions, bot/runtime bug discussions, research sprints, Obsidian dialogue indexes, JSON/JSONL sidechat exports, and requests to save a transcript, protocol, handoff, question map, decisions, tasks, addendum, or reusable continuation prompt without dumping the full protocol into chat.
metadata:
  short-description: File-backed sidechat protocol and handoff
---

# Sidechat Protocol Pack

## Purpose

Use this skill to preserve a side conversation as files, not as a long chat response. The default output language is Russian.

Trigger phrases include: `/protocol`, `Сделай протокол`, `сделай протокол`, `запротоколлируй`, `протокол`, `сохрани протокол`, `сохрани протокол в папку`, `протокол D:\\...`, `протокол <path>`, `экспорт бокового чата`, `sidechat export`, `JSON export`, `JSONL timeline`, `индекс в Obsidian`, `прочитать протоколы`, `обнови протоколы`, `освежи контекст по протоколам`, `собери решения из протоколов`, `настрой протоколы`, `настройки протоколов`, `покажи настройки протоколов`, `измени папку протоколов`, `измени папку export`, `измени vault Obsidian`, `связи протоколов`, `закрой боковую беседу`, `сохрани переписку`, `handoff`, `raw transcript`, `карта вопросов`, `запиши решения`, `чтобы основная ветка подхватила`, `создай пакет протокола`.

## Core Rule

Do not print the full protocol into chat. Create or update files, then answer only with a short summary and the protocol folder path.

If file creation is not possible, say briefly that a proper protocol requires files and ask for permission or a different target folder.

## Explicit Target Folder

If the user provides a folder path in the protocol request, treat it as an explicit one-run target. This is useful for intermediate research, Kimi/Claude/Codex result folders, customer analysis folders, or any case where the protocol belongs next to the work result rather than in the general project protocol archive.

Recognize patterns like:

```text
сохрани протокол в D:\GWD\Разработка\ИИ\AiDrevo\Исследования\20260529 Анализ что уже можно продавать\Результаты\Kimi
сохрани протокол в папку D:\path\to\folder
протокол D:\path\to\folder
Сделай протокол в D:\path\to\folder
```

Target-folder rule:

1. Do not overwrite unrelated files in the target folder.
2. By default, create a protocol-pack subfolder inside the provided target folder:

```text
<explicit_target_folder>/YYYY-MM-DD_<short_slug>/
```

3. If the user explicitly says `прямо в эту папку` or the target folder already appears to be a final protocol-pack folder, write the protocol files directly there.
4. An explicit target folder applies only to the current protocol run. Do not save it into `.codex/sidechat-protocol-pack.json` unless the user asks to make it the project default.
5. If the folder does not exist, create it after confirming it is inside the intended workspace or an explicitly provided absolute path.
6. In the chat response, show the final folder actually used, not just the parent target.
## Folder Layout

Use per-project storage. Never send protocols from an unrelated workspace into an AiDrevo/Viktor2.0 folder unless the current project explicitly configured that path.

Project config file:

```text
.codex/sidechat-protocol-pack.json
```

Config shape:

```json
{
  "protocol_root": ".protocols/sidechats",
  "machine_export_enabled": true,
  "machine_export_root": "D:\\\\.CodexProtocolsDontMove",
  "obsidian_enabled": false,
  "obsidian_dialog_root": "",
  "obsidian_project_name": "",
  "obsidian_note_visibility": "show_path"
}
```

Resolution order:

1. If the user gives a target folder in the request, use it for this run and offer to save it into project config.
2. If `.codex/sidechat-protocol-pack.json` exists in the current workspace, use `protocol_root` from it.
3. If no config exists, ask once where to save protocols for this project.
4. Recommended default for new projects:

```text
.protocols/sidechats/YYYY/YYYY-MM/YYYY-MM-DD_<short_slug>/
```

5. If the user chooses a custom project path, save it to `.codex/sidechat-protocol-pack.json` so the next run in this project does not ask again.
6. Treat Obsidian settings as per-project settings, not global personal settings. A user can have several Obsidian vaults, so never reuse a vault from another project unless the current project config explicitly points to it.

Examples of valid `protocol_root` values:

```text
.protocols/sidechats
AiDrevo_OS/01_Protocols/SideChats
_docs/protocols/sidechats
```

The full protocol folder is always:

```text
<protocol_root>/YYYY/YYYY-MM/YYYY-MM-DD_<short_slug>/
```

Create these files for a first Markdown protocol:

```text
00_INDEX.md
01_PROTOCOL.md
02_HANDOFF_FOR_MAIN_THREAD.md
03_RAW_TRANSCRIPT.md
04_QUESTION_MAP.md
05_DECISIONS_AND_TASKS.md
06_ARTICLE_MATERIALS.md
```

Use Russian headings and Russian prose. Keep technical identifiers, paths, IDs, command names, URLs, and error text unchanged.

## Sidechat Export Mode

Sidechat Export is the machine-readable companion to the Markdown protocol. It is not an official Codex thread import format.

Use Sidechat Export by default when the side conversation contains decisions, tasks, architecture, bug analysis, research, handoff value, or the user asks to preserve/export/recover the side chat. For tiny operational notes, Markdown-only is acceptable if the user explicitly asks for a lightweight protocol.

Machine export root:

```text
<machine_export_root>/exports/YYYY/MM/DD/<protocol_id>/
```

Recommended default:

```text
D:\.CodexProtocolsDontMove
```

This root is intentionally outside both Codex system folders and project folders:

- do not put long-lived protocol registry data under Codex app/system directories because app updates can change internal layouts;
- do not put all JSON/JSONL exports inside every project by default because these files are mainly for automation, not daily reading;
- keep human Markdown close to the project or explicit target folder, and keep machine-readable exports in one durable registry root.

The folder name `D:\.CodexProtocolsDontMove` is the current recommended default. It is intentionally explicit and slightly inconvenient-looking so the user understands it is a durable system archive, not a normal working folder.

Machine export files:

```text
manifest.json
normalized.json
timeline.jsonl
```

Registry files:

```text
<machine_export_root>/registry/sidechat_protocol_registry.jsonl
<machine_export_root>/registry/sidechat_protocol_registry_index.json
```

Do not store machine JSON/JSONL inside Obsidian by default. Obsidian should receive a compact index note, not raw automation files.

### NORMALIZED JSON

`normalized.json` is a structured snapshot for Project OS, the main thread, another model, future Event Ledger/PostgreSQL/RAG, and audits.

It also enables the main thread to refresh itself after several side chats were run in parallel. A future/current command such as `обнови протоколы` or `прочитай протоколы` can read the project registry plus normalized exports, then restore important decisions, changed assumptions, tasks, risks, and source links without asking the user to paste every side chat manually.

Required top-level fields:

```json
{
  "schema": "sidechat_protocol.normalized.v0.2",
  "protocol_id": "",
  "created_at": "",
  "language": "ru",
  "status": "normalized_export_not_official_codex_import",
  "topic": "",
  "project": "",
  "workspace": "",
  "privacy_scope": "",
  "parent_thread_id": "",
  "source_thread_id": "",
  "human_protocol_folder": "",
  "machine_export_folder": "",
  "summary": {},
  "decisions": [],
  "tasks": [],
  "links": [],
  "created_files": [],
  "limitations": []
}
```

### TIMELINE JSONL

`timeline.jsonl` is an append-friendly event stream. One line is one valid JSON object.

Use JSONL for meaningful events only. Do not write routine agent status chatter such as `accepted`, `started`, `sync started`, tool progress, or other technical noise. Save only useful conversation events, decisions, tasks, created/updated files, links, errors, constraints, limitations, and protocol update events.

Recommended event types:

```text
session_meta
limitation
user_message
assistant_message
user_request
assistant_response
decision
task
file_created
file_updated
link
telegram_post
error
constraint
recommended_next_step
```

Every event should include `type`. Add `created_at`, `summary`, `path`, `url`, `id`, or `status` when relevant.

### Manifest

`manifest.json` connects the human protocol, machine export, registry entry, project, workspace, source thread, parent thread, and validation result.

Required fields:

```json
{
  "schema": "sidechat_protocol.manifest.v0.2",
  "protocol_id": "",
  "human_protocol_folder": "",
  "machine_export_folder": "",
  "normalized_json": "",
  "timeline_jsonl": "",
  "project": "",
  "workspace": "",
  "source_thread_id": "",
  "parent_thread_id": "",
  "not_official_codex_thread": true,
  "validation": {}
}
```

### Required Limitation Text

Every Markdown protocol, normalized JSON, manifest, and relevant registry entry must include this meaning:

```text
Это не официальный импортируемый Codex thread. Это переносимый экспорт боковой беседы для Project OS, основной ветки, другой модели и будущего Event Ledger/PostgreSQL/RAG.
```

## Obsidian Index Mode

Obsidian index is optional and per-project. Ask the user once whether they use Obsidian and want a dialogue/protocol index note there. Save the answer in `.codex/sidechat-protocol-pack.json`.

Important: Obsidian vault selection is per-project. The same user can have several vaults: one large personal vault, one vault per project, and one temporary research vault. The skill must not reuse a vault from another project unless the current project config explicitly points to it.

If `obsidian_enabled` is true but `obsidian_dialog_root` is empty or ambiguous, do not write the note. Ask the user to choose the project-specific vault/folder and then save it in the current project's `.codex/sidechat-protocol-pack.json`.

Use Obsidian only for compact human navigation:

- topic;
- date;
- participants;
- linked protocol pack;
- linked machine export;
- summary;
- decisions;
- tasks;
- what to read next.

Do not put full raw transcript or bulky JSON/JSONL into Obsidian by default.

Before creating or updating an Obsidian note, include the exact destination in the final chat response:

```text
Obsidian index note: <full path to note>
```

If the note was not created because Obsidian is disabled or not configured, say this briefly and do not treat it as an error.

Recommended Obsidian note path:

```text
<obsidian_dialog_root>/<topic_folder>/YYYY-MM-DD - <title>.md
```

Follow this frontmatter pattern:

```yaml
---
тип: диалог
дата: YYYY-MM-DD
тема: ...
участники: [Oleg, Codex]
связано:
  - "[[...]]"
теги: [тип/диалог, тип/протокол, система/codex, статус/черновик]
protocol_id: ...
human_protocol_folder: ...
machine_export_folder: ...
---
```

Body sections:

```text
# YYYY-MM-DD - <title>

## Резюме
## Контекст разговора
## Ключевые решения
## Задачи
## Ссылки на протоколы и export
## Что дальше
```

## First Protocol Workflow

1. Identify the conversation boundary and source material available in context.
2. If full raw transcript is unavailable, explicitly state that limitation in `03_RAW_TRANSCRIPT.md`.
3. Build a human protocol in `01_PROTOCOL.md`: why opened, what discussed, what decided, what not decided, risks, next steps.
4. Build `02_HANDOFF_FOR_MAIN_THREAD.md`: technical findings, files/registries to check, mini-ADR draft, links, what must not be lost.
5. Build `04_QUESTION_MAP.md`: discussed questions, open questions, questions that became tasks, questions for the main thread.
6. Build `05_DECISIONS_AND_TASKS.md`: decisions, statuses, tasks, risks, contradictions, confirmations needed.
7. Build `06_ARTICLE_MATERIALS.md` only when useful; otherwise keep it compact.
8. Update `00_INDEX.md` with status, language, version, created files, export files, Obsidian note if any, and what to pass to the main thread.
9. If Sidechat Export applies, create `manifest.json`, `normalized.json`, and `timeline.jsonl` under `machine_export_root`, then append a row to `sidechat_protocol_registry.jsonl`.
10. If Obsidian index is enabled, create or update the compact Obsidian note.
11. Keep the final chat response compact: say that the protocol was created/updated, show the human protocol folder, machine export folder if created, and Obsidian note path if created.

Do not paste long technical logs into chat. Do not write routine chat-status messages such as `started`, `accepted`, `sync started`, or tool progress into Markdown, JSON, or JSONL. The protocol should preserve the work, not the agent's mechanical status stream.

## Repeat Protocol Workflow

If the protocol folder already exists, do not recreate the full pack from scratch.

Create an incremental update:

```text
07_PROTOCOL_ADDENDUM_002.md
08_DECISION_DIFF_002.md
09_RAW_TRANSCRIPT_DELTA_002.md
```

Use the next available number for later updates.

The repeat update should:

- capture only messages and decisions after the previous protocol checkpoint;
- update `00_INDEX.md` with current version, latest addendum, active decisions, and superseded decisions;
- preserve old decisions instead of silently rewriting them;
- mark changed decisions with `superseded`, `Superseded by`, and `Reason`.
- create new machine export files for the update instead of overwriting prior export files;
- append a new registry event for the addendum/update.

Decision status values:

```text
draft
accepted
superseded
rejected
```

## Main Thread Protocol Refresh Workflow

Use this mode when the user in the main thread asks:

- `обнови протоколы`
- `прочитай протоколы`
- `освежи контекст по протоколам`
- `собери решения из протоколов`
- similar wording that asks to refresh project context from sidechat protocols.

Purpose:

- let the main thread catch up after several side chats were run in parallel;
- recover decisions from side chats that may already be closed or deleted;
- avoid asking the user to manually paste every sidechat handoff;
- rebuild the main thread's current understanding from Markdown protocol packs plus JSON/JSONL registry data.

Procedure:

1. Resolve current project config from `.codex/sidechat-protocol-pack.json`.
2. Identify the human protocol root for this project and the machine export root.
3. Read the registry/index if available.
4. Filter protocol entries for the current project/workspace first.
5. Summarize only relevant recent or requested protocols; do not dump full JSON/JSONL into chat.
6. Extract accepted decisions, changed decisions, open questions, tasks, risks, created files, and recommended next actions.
7. If sidechat protocols conflict, report a decision diff instead of merging silently.
8. Return a compact main-thread refresh summary and include paths to the source protocol folders.

This mode should not create a new protocol unless the user also asks to save the refresh result.

## Settings Management Workflow

Use this mode when the user asks to view, edit, connect, relink, or reset protocol storage settings.

Trigger phrases:

- `настрой протоколы`
- `настройки протоколов`
- `покажи настройки протоколов`
- `измени папку протоколов`
- `измени папку export`
- `измени vault Obsidian`
- `связи протоколов`
- similar wording about where Markdown, JSON/JSONL, registry, or Obsidian notes are saved.

Purpose:

- make storage routing visible and editable;
- prevent protocols from being saved into the wrong project or vault;
- let the user manage current-project paths without editing JSON manually;
- distinguish current project config from global recommended defaults.

Settings file for the current project:

```text
.codex/sidechat-protocol-pack.json
```

Editable settings:

- `protocol_root`: where human Markdown protocol packs are saved for the current project.
- `machine_export_enabled`: whether JSON/JSONL exports are created.
- `machine_export_root`: where machine exports and registry are stored.
- `obsidian_enabled`: whether compact Obsidian index notes are created.
- `obsidian_dialog_root`: project-specific Obsidian folder for dialogue/protocol index notes.
- `obsidian_project_name`: project label used in Obsidian frontmatter and summaries.
- `obsidian_note_visibility`: whether to show the note path in final chat responses.

Recommended response when showing settings:

```text
Текущие связи протоколов для проекта:

Markdown protocol root:
<path>

Machine export root:
<path or disabled>

Obsidian index root:
<path or disabled/not configured>

Config file:
.codex/sidechat-protocol-pack.json
```

When changing settings:

1. If the requested change is explicit, update only that field.
2. If the user says "настрой протоколы" without concrete paths, show current settings and ask which path to change.
3. Do not overwrite unrelated config keys.
4. Do not change another project's config.
5. If a target folder is outside the current workspace, it is allowed only when the user explicitly provided it or approved it.
6. For Obsidian, ask for the exact project-specific vault/folder path if not provided.
7. After saving, show the updated routing summary.

Do not create a protocol during settings management unless the user also asks to protocol the current conversation.

## Source Integrity

Never use a previously mistaken chat-pasted protocol as source of truth unless the user explicitly says to use it.

Prefer sources in this order:

1. Current visible conversation.
2. User-provided manual transcript files.
3. Existing protocol pack files.
4. Local Codex session/rollout/log files, if the user asks to recover a closed chat.
5. Memory summaries, only as secondary context and clearly marked if stale.

If something is inferred, label it as inferred. If something is not confirmed, label it as not confirmed.

## Main Thread Handoff

Every protocol pack should answer:

- What should the main thread know?
- Which decisions are active?
- Which decisions are drafts?
- Which decisions were superseded?
- Which tasks were created or proposed?
- Which runtime/code changes must not be done from the side thread?
- What verification is still missing?

## Acceptance Criteria

For Markdown-only protocol:

- Markdown protocol pack exists.
- `00_INDEX.md` lists created files and limitations.
- Full protocol is not dumped into chat.
- Main thread can continue from `02_HANDOFF_FOR_MAIN_THREAD.md` without reading the full side conversation.

For Sidechat Export:

- Markdown protocol pack exists.
- `manifest.json` exists.
- `normalized.json` exists and is valid JSON.
- `timeline.jsonl` exists and every non-empty line is valid JSON.
- `normalized.json` contains `schema`, `protocol_id`, `topic`, `project`, `workspace`, `human_protocol_folder`, `machine_export_folder`, and `limitations`.
- `timeline.jsonl` events contain `type`.
- Registry JSONL has an entry for the protocol or addendum.
- Protocol and export explicitly say they are not an official importable Codex thread.

For Obsidian Index:

- Obsidian note exists only if enabled/configured or explicitly requested.
- Obsidian note links to the Markdown protocol folder and machine export folder.
- Obsidian note is compact and does not duplicate bulky JSON/JSONL.

## Validation

When a machine export is created, validate JSON and JSONL before claiming completion. Use `scripts/validate_sidechat_export.py` if available.

Validation command:

```powershell
py -3 scripts\validate_sidechat_export.py --export-dir "<machine_export_folder>"
```

## Chat Response

After creating, updating, or refreshing protocols, respond briefly:

```text
Пакет протокола создан/обновлен:
<folder path>

Коротко: <1-3 sentences>.

Главные файлы:
00_INDEX.md
02_HANDOFF_FOR_MAIN_THREAD.md
05_DECISIONS_AND_TASKS.md

Machine export:
<folder path or "не создавался">

Obsidian index note:
<note path or "не настроен">
```

For clickable paths in Codex UI, prefer giving the folder as plain text plus filenames separately; long Cyrillic Windows paths render poorly as cards.



## Codex Sidechat Tree Model

Use this mental model when explaining or applying the skill.

A long Codex project is the tree trunk. The main thread is the trunk line: it keeps stable direction, project memory, root decisions, long-term context, and the current operating plan. Side chats are branches and leaves: short focused sprints that grow from the trunk to solve one question without overloading the main thread.

Recommended interpretation:

- Trunk: the main Codex thread, project OS, WIP files, stable rules, active roadmap, shared context.
- Branch: a side chat opened from the main thread for one bounded topic, research question, bug, design decision, or experiment.
- Leaf: the short sprint result inside the side chat: conclusion, decision, prompt, patch idea, risk, task, or reusable artifact.
- Fallen leaf risk: if the side chat is closed without protocol, the leaf dries out and the project loses the decision trail.
- Protocol pack: the process of pressing the leaf into the project herbarium, so it becomes durable and searchable.
- Markdown layer: human-readable pressed leaf, suitable for the main thread and project notes.
- JSON/JSONL layer: machine-readable veins of the leaf, suitable for registry, Event Ledger, RAG, PostgreSQL, and later automation.
- Obsidian note: the catalog card that places the leaf into the knowledge graph and topic map.

Behavior rules:

- Do not turn every side chat into a huge document by default. Preserve the useful leaf: context, reasoning, decisions, tasks, links, files, and limitations.
- If the side chat changed an earlier decision, write this explicitly as a decision diff instead of silently replacing the old protocol.
- If the side chat only adds new information, create an addendum/delta.
- If the side chat produced a reusable instruction for the main thread, create a handoff prompt.
- If the side chat produced research or article material, preserve it in the human Markdown layer and summarize it in JSON.
- Treat side chats as sprint leaves, not as a second trunk. The main thread should remain the place where integrated project direction is accepted.

Suggested explanation to the user:

> Think of the main Codex conversation as the project tree trunk. A side chat is a leaf-sprint: it can quickly grow an answer, test an idea, or decide a narrow issue. The protocol pack saves that leaf back into the tree: Markdown for humans and the main branch, JSON/JSONL for automation, and optional Obsidian notes for the knowledge graph.
