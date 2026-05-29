# skillpackforcodex

Набор переиспользуемых skills для Codex.

Этот репозиторий задуман как личная и командная библиотека рабочих навыков: каждый skill оформляет повторяемый процесс в виде короткой инструкции, которую Codex может подхватывать в разных проектах.

## Зачем Нужен Skillpack

В длинных проектах много процессов повторяется:

- закрыть боковой чат протоколом;
- сделать handoff для другой ветки;
- оформить архитектурное решение;
- подготовить ревью;
- создать continuation prompt;
- собрать материалы для статьи или кейса;
- зафиксировать задачи, решения и риски.

Если каждый раз держать такие правила только в переписке, они теряются, устаревают и по-разному исполняются разными AI-сессиями. Skillpack переносит эти правила в файлы, которые можно версионировать, улучшать и устанавливать на другой компьютер.

## Структура Репозитория

```text
skillpackforcodex/
  skills/
    <skill-name>/
      SKILL.md
      agents/
        openai.yaml
      references/
      scripts/
      assets/
```

Обязателен только `SKILL.md`. Остальные папки добавляются, когда skill реально нуждается в метаданных, справочниках, скриптах или шаблонах.

Один Git-репозиторий хранит всю коллекцию. Отдельный `.git` внутри каждой папки skill не нужен.

## Установка

Склонируйте репозиторий:

```powershell
git clone https://github.com/olegzaharovdev/skillpackforcodex.git
```

Скопируйте нужный skill в локальную папку Codex skills:

```powershell
Copy-Item -Recurse -Force `
  ".\skillpackforcodex\skills\<skill-name>" `
  "$env:USERPROFILE\.agents\skills\<skill-name>"
```

Пример:

```powershell
Copy-Item -Recurse -Force `
  ".\skillpackforcodex\skills\sidechat-protocol-pack" `
  "$env:USERPROFILE\.agents\skills\sidechat-protocol-pack"
```

После установки откройте новую Codex-сессию или перезапустите Codex, чтобы skill попал в список доступных.

## Доступные Skills

### sidechat-protocol-pack

Создает или обновляет файловый протокол боковой беседы: человеческий протокол, handoff для основной ветки, raw transcript notes, карту вопросов, решения, задачи и материалы для будущих статей/курсов.

Примеры вызова:

```text
/protocol
```

```text
Сделай протокол
```

```text
запротоколлируй
```

```text
протокол
```

Первый вызов создает полный protocol pack. Повторный вызов в той же беседе должен создавать addendum/delta и decision diff, не перезаписывая историю молча.

## Per-Project Настройки

Некоторые skills могут хранить настройки внутри конкретного проекта, чтобы не смешивать разные рабочие контуры.

Для `sidechat-protocol-pack` используется файл:

```text
.codex/sidechat-protocol-pack.json
```

Пример универсального конфига:

```json
{
  "protocol_root": ".protocols/sidechats"
}
```

Тогда итоговые папки будут создаваться так:

```text
.protocols/sidechats/YYYY/YYYY-MM/YYYY-MM-DD_<short_slug>/
```

Для проекта со своим контуром протоколов можно задать другой путь:

```json
{
  "protocol_root": "AiDrevo_OS/01_Protocols/SideChats"
}
```

Если project config отсутствует, skill должен спросить, куда сохранять протоколы для текущего проекта, и предложить сохранить выбор в `.codex/sidechat-protocol-pack.json`.

## Добавление Нового Skill

Рекомендуемый формат:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
```

Правила:

- `skill-name` пишется в lowercase kebab-case.
- `SKILL.md` обязателен.
- `agents/openai.yaml` желателен для читаемого отображения в UI.
- Не добавляйте лишние README/CHANGELOG внутрь каждого skill без необходимости.
- Подробные материалы лучше класть в `references/`, если они нужны только иногда.
- Скрипты для повторяемых действий кладите в `scripts/`.
- Шаблоны и ассеты кладите в `assets/`.

## Публикация Изменений

Добавление нового skill:

```powershell
git add skills/<skill-name>
git commit -m "Add <skill-name> skill"
git push
```

Обновление существующего skill:

```powershell
git add skills/<skill-name>
git commit -m "Update <skill-name>"
git push
```

Обновление README:

```powershell
git add README.md
git commit -m "Update README"
git push
```
