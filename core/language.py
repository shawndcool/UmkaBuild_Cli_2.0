from core.translations import translations


def select_language():
	print("\n🌐 Оберіть мову / Select language:\n[1] Українська\n[2] English")
	choice = input("Ваш вибір / Your choice: ").strip()
	lang = "uk" if choice == '1' else "en"
	if not choice in ('1', '2'):
		print(translations[lang]['invalid_selection'])
	else:
		print(translations[lang]['language_successfull'])
	return lang

def set_language(lang):
	return translations.get(lang, translations['uk'])

def get_saved_language(data):
	return data.get("language")