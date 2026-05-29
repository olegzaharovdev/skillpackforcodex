---
name: sidechat-protocol-pack
description: Create or update a durable Russian-language Sidechat Protocol Pack when the user asks to close, preserve, protocol, hand off, recover, summarize, or continue a side conversation. Trigger on short Russian commands like "Сделай протокол", "запротоколлируй", or "протокол". Use for side chats, interrupted chats, architectural decisions, bot/runtime bug discussions, and requests to save a transcript, protocol, handoff, question map, decisions, tasks, addendum, or reusable continuation prompt without dumping the full protocol into chat.
metadata:
  short-description: File-backed sidechat protocol and handoff
---

# Sidechat Protocol Pack

## Purpose

Use this skill to preserve a side conversation as files, not as a long chat response. The default output language is Russian.

Trigger phrases include: `/protocol`, `Сделай протокол`, `сделай протокол`, `запротоколлируй`, `протокол`, `закрой боковую беседу`, `сохрани переписку`, `handoff`, `raw transcript`, `карта вопросов`, `запиши решения`, `чтобы основная ветка подхватила`, `создай пакет протокола`.

## Core Rule

Do not print the full protocol into chat. Create or update files, then answer only with a short summary and the protocol folder path.

If file creation is not possible, say briefly that a proper protocol requires files and ask for permission or a different target folder.

## Folder Layout

Default project path:

```text
AiDrevo_OS/01_Protocols/SideChats/YYYY/YYYY-MM/YYYY-MM-DD_<short_slug>/
```

Create these files for a first protocol:

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

## First Protocol Workflow

1. Identify the conversation boundary and source material available in context.
2. If full raw transcript is unavailable, explicitly state that limitation in `03_RAW_TRANSCRIPT.md`.
3. Build a human protocol in `01_PROTOCOL.md`: why opened, what discussed, what decided, what not decided, risks, next steps.
4. Build `02_HANDOFF_FOR_MAIN_THREAD.md`: technical findings, files/registries to check, mini-ADR draft, links, what must not be lost.
5. Build `04_QUESTION_MAP.md`: discussed questions, open questions, questions that became tasks, questions for the main thread.
6. Build `05_DECISIONS_AND_TASKS.md`: decisions, statuses, tasks, risks, contradictions, confirmations needed.
7. Build `06_ARTICLE_MATERIALS.md` only when useful; otherwise keep it compact.
8. Update `00_INDEX.md` with status, language, version, created files, and what to pass to the main thread.

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

Decision status values:

```text
draft
accepted
superseded
rejected
```

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

## Chat Response

After creating or updating files, respond briefly:

```text
Пакет протокола создан/обновлен:
<folder path>

Коротко: <1-3 sentences>.

Главные файлы:
00_INDEX.md
02_HANDOFF_FOR_MAIN_THREAD.md
05_DECISIONS_AND_TASKS.md
```

For clickable paths in Codex UI, prefer giving the folder as plain text plus filenames separately; long Cyrillic Windows paths render poorly as cards.
