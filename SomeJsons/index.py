import json 
from typing import Any, Dict

def LoadConfig(*file_paths:str) -> Dict[str, Any]:
    combined_config = {}

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
                print(f"Содержимое файла {file_path}:")
                print(json.dumps(config, indent=4, ensure_ascii=False))
                combined_config.update(config)
        except FileNotFoundError: print(f"Файл {file_path} не найден.")
        except json.JSONDecodeError as e: print(f"Ошибка декодирования JSON из файла {file_path}: {e}")
    
    return combined_config

print(LoadConfig("test1.json", "test2.json"))