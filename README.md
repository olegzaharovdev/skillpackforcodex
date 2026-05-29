# skillpackforcodex

Коллекция переиспользуемых skills для Codex.

Репозиторий задуман как общий skillpack: каждый skill лежит в отдельной папке внутри `skills/`, имеет свой `SKILL.md` и при необходимости дополнительные файлы в `agents/`, `references/`, `scripts/` или `assets/`.

## Зачем Это Нужно

Codex-сессии, боковые чаты и рабочие обсуждения легко теряются: окно можно закрыть, контекст может compact-иться, а важные решения остаются только в переписке. Skills из этого репозитория переводят повторяемые рабочие процессы в файловые правила, которые можно переиспользовать в разных проектах.

`sidechat-protocol-pack` нужен, чтобы:

- закрывать боковой чат не сообщением в чат, а файловым protocol pack;
- сохранять решения, вопросы, задачи и handoff для основной ветки;
- не терять архитектурные договоренности после закрытия side chat;
- обновлять протокол инкрементально через addendum/delta, если после первого протокола беседа продолжилась;
- хранить протоколы в текущем проекте, а не в случайной глобальной папке.

## Структура

```text
skillpackforcodex/
  skills/
    sidechat-protocol-pack/
      SKILL.md
      agents/
        openai.yaml
```

Один Git-репозиторий хранит всю коллекцию. Отдельный `.git` внутри каждой папки skill не нужен.

## Установка Skill

Склонируйте репозиторий:

```powershell
git clone https://github.com/olegzaharovdev/skillpackforcodex.git
```

Скопируйте нужный skill в локальную папку Codex skills:

```powershell
Copy-Item -Recurse -Force `
  ".\skillpackforcodex\skills\sidechat-protocol-pack" `
  "$env:USERPROFILE\.agents\skills\sidechat-protocol-pack"
```

После этого перезапустите Codex или откройте новую сессию, чтобы skill попал в список доступных.

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

## Хранение Протоколов

`sidechat-protocol-pack` использует per-project настройку. В каждом проекте можно создать файл:

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

## Публикация Изменений

```powershell
git add skills/<skill-name>
git commit -m "Add <skill-name> skill"
git push
```

Для обновления существующего skill:

```powershell
git add skills/<skill-name>
git commit -m "Update <skill-name>"
git push
```
