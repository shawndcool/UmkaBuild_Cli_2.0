import os
import json


SAVE_PATH = "build_config_save.json"

def load_the_json():
	default_data = {
		"language": "uk",
		"options_name": ["--noconfirm", "--onefile", "--windowed", "--clean", "--noupx", "--hidden-import=plyer.platforms.win.notification"],
		"save_commands": []
	}
	if os.path.exists(SAVE_PATH):
		if os.path.getsize(SAVE_PATH) == 0:
			print(
				"ℹ️ Файл конфігурації існує, але порожній. Створюємо нову структуру.\n"
				"ℹ️ The configuration file exists, but is empty. Creating a new structure.\n"
				)
			save_build_to_json(default_data)
			return default_data
		with open(SAVE_PATH, "r", encoding = "utf-8") as f:
			try:
				return json.load(f)
			except json.JSONDecodeError:
				print(
					"⚠️ Помилка при читанні JSON. Файл пошкоджений або має неправильний формат. Видаліть файл 'build_config_save.json' та перезапустіть програму.\n"
					"⚠️ Error reading JSON. The file is corrupt or has an incorrect format. Delete the file 'build_config_save.json' and restart the application.\n"
					)
				save_build_to_json(default_data)
				return default_data
	else:
		print(
			"📄 Файл конфігурації не знайдено. Створюємо новий.\n"
			"📄 Configuration file not found. Creating a new one.\n"
			)
		save_build_to_json(default_data)
		return default_data

def save_build_to_json(data):
	with open(SAVE_PATH, "w", encoding = "utf-8") as f:
		json.dump(data, f, indent = 4, ensure_ascii = False)