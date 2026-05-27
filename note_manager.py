#!/usr/bin/env python3
"""
Personal Note Manager - консольное приложение для управления заметками.
Поддерживает добавление, удаление, поиск и просмотр всех заметок.

Использование:
    python note_manager.py

Команды:
    add     - добавить заметку
    list    - показать все заметки
    search  - найти заметки по ключевому слову
    delete  - удалить заметку по ID
    exit    - выйти из программы
"""
# Team Project: Git training
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


# ============== НАСТРОЙКИ ==============
NOTES_FILE = "notes.json"


# ============== РАБОТА С ФАЙЛАМИ ==============
def load_notes() -> List[Dict]:
    """Загружает заметки из JSON-файла."""
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_notes(notes: List[Dict]) -> None:
    """Сохраняет заметки в JSON-файл."""
    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=4, ensure_ascii=False)


# ============== ОСНОВНЫЕ ФУНКЦИИ ==============
def add_note(title: str, content: str) -> Dict:
    """Добавляет новую заметку и возвращает её."""
    notes = load_notes()
    
    # Генерируем новый ID
    new_id = max([note["id"] for note in notes], default=0) + 1
    
    note = {
        "id": new_id,
        "title": title,
        "content": content,
        "created_at": datetime.now().isoformat(),
    }
    notes.append(note)
    save_notes(notes)
    return note


def delete_note(note_id: int) -> bool:
    """Удаляет заметку по ID. Возвращает True, если удаление успешно."""
    notes = load_notes()
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            notes.pop(i)
            save_notes(notes)
            return True
    return False


def list_notes() -> List[Dict]:
    """Возвращает список всех заметок."""
    return load_notes()


def search_notes(keyword: str) -> List[Dict]:
    """Ищет заметки по ключевому слову в заголовке или содержимом."""
    notes = load_notes()
    keyword_lower = keyword.lower()
    return [
        note for note in notes
        if keyword_lower in note["title"].lower()
        or keyword_lower in note["content"].lower()
    ]


def get_note_by_id(note_id: int) -> Optional[Dict]:
    """Возвращает заметку по ID или None, если не найдена."""
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            return note
    return None


def edit_note(note_id: int, new_title: str = None, new_content: str = None) -> bool:
    """Редактирует существующую заметку. Возвращает True, если успешно."""
    notes = load_notes()
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            if new_title:
                notes[i]["title"] = new_title
            if new_content:
                notes[i]["content"] = new_content
            notes[i]["updated_at"] = datetime.now().isoformat()
            save_notes(notes)
            return True
    return False


# ============== ОТОБРАЖЕНИЕ ==============
def display_note(note: Dict, detailed: bool = True) -> None:
    """Красиво выводит одну заметку в консоль."""
    print(f"\n📌 [{note['id']}] {note['title']}")
    if detailed:
        print(f"   {note['content']}")
        print(f"   🕒 Создано: {note['created_at'][:19].replace('T', ' ')}")
        if "updated_at" in note:
            print(f"   ✏️  Изменено: {note['updated_at'][:19].replace('T', ' ')}")
    else:
        # Краткий вывод (только для list)
        preview = note['content'][:50] + "..." if len(note['content']) > 50 else note['content']
        print(f"   {preview}")


def display_help() -> None:
    """Выводит справку по командам."""
    print("\n📖 Доступные команды:")
    print("   add     - добавить новую заметку")
    print("   list    - показать все заметки")
    print("   view    - показать подробно одну заметку")
    print("   search  - найти заметки по ключевому слову")
    print("   edit    - редактировать заметку")
    print("   delete  - удалить заметку")
    print("   help    - показать эту справку")
    print("   exit    - выйти из программы\n")


# ============== ГЛАВНАЯ ФУНКЦИЯ ==============
def main():
    """Главная функция-обработчик команд."""
    print("\n" + "="*50)
    print("   📓 PERSONAL NOTE MANAGER v2.0")
    print("   Простое приложение для заметок")
    print("="*50)
    display_help()

    while True:
        try:
            command = input("\n> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n\nДо свидания!")
            break

        # Выход
        if command == "exit":
            print("До свидания!")
            break

        # Справка
        elif command == "help":
            display_help()

        # Добавление заметки
        elif command == "add":
            title = input("  Заголовок: ").strip()
            if not title:
                print("  ⚠️ Заголовок не может быть пустым")
                continue
            content = input("  Текст: ").strip()
            if not content:
                print("  ⚠️ Текст не может быть пустым")
                continue
            note = add_note(title, content)
            print(f"  ✅ Заметка добавлена (ID: {note['id']})")

        # Список всех заметок (кратко)
        elif command == "list":
            notes = list_notes()
            if not notes:
                print("  📭 Нет заметок. Используйте 'add' чтобы создать первую заметку")
            else:
                print(f"\n  Всего заметок: {len(notes)}\n")
                print("  " + "-"*40)
                for note in notes:
                    display_note(note, detailed=False)
                    print("  " + "-"*40)

        # Просмотр одной заметки подробно
        elif command == "view":
            try:
                note_id = int(input("  ID заметки: "))
                note = get_note_by_id(note_id)
                if note:
                    display_note(note, detailed=True)
                else:
                    print(f"  ❌ Заметка с ID {note_id} не найдена")
            except ValueError:
                print("  ⚠️ ID должен быть числом")

        # Поиск заметок
        elif command == "search":
            keyword = input("  Ключевое слово: ").strip()
            if not keyword:
                print("  ⚠️ Введите ключевое слово для поиска")
                continue
            results = search_notes(keyword)
            if not results:
                print("  ❌ Ничего не найдено")
            else:
                print(f"\n  🔍 Найдено: {len(results)} заметок\n")
                for note in results:
                    display_note(note, detailed=True)

        # Редактирование заметки
        elif command == "edit":
            try:
                note_id = int(input("  ID заметки для редактирования: "))
                note = get_note_by_id(note_id)
                if not note:
                    print(f"  ❌ Заметка с ID {note_id} не найдена")
                    continue
                
                print(f"  Текущий заголовок: {note['title']}")
                new_title = input("  Новый заголовок (оставьте пустым для сохранения): ").strip()
                
                print(f"  Текущий текст: {note['content']}")
                new_content = input("  Новый текст (оставьте пустым для сохранения): ").strip()
                
                if edit_note(note_id, new_title or None, new_content or None):
                    print("  ✅ Заметка обновлена")
                else:
                    print("  ❌ Ошибка при обновлении")
            except ValueError:
                print("  ⚠️ ID должен быть числом")

        # Удаление заметки
        elif command == "delete":
            try:
                note_id = int(input("  ID заметки для удаления: "))
                # Подтверждение удаления
                confirm = input(f"  Вы уверены? Удалить заметку {note_id}? (y/N): ").strip().lower()
                if confirm in ['y', 'yes', 'да']:
                    if delete_note(note_id):
                        print("  🗑️ Заметка удалена")
                    else:
                        print("  ❌ Заметка с таким ID не найдена")
                else:
                    print("  ℹ️ Удаление отменено")
            except ValueError:
                print("  ⚠️ ID должен быть числом")

        # Неизвестная команда
        else:
            print("  ❓ Неизвестная команда. Введите 'help' для списка команд")


if __name__ == "__main__":
    main()