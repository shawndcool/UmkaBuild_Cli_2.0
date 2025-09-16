import os
import json
import shutil
import subprocess
from core.storage import load_the_json, save_build_to_json
from core.language import select_language, set_language, get_saved_language


SOURCE_PATH = "source_files"

def show_ascii_logo(lang):
	tagline = lang.get('logo', '🚀 UmkaBuild 🚀')
	copyright = lang.get('copyright', '© 2025 UmkaBuild')
	site = "🌐 umua.pp.ua"
	logo = f"""
╔═════════════════════════════════════════════════════════════════════╗
                    ╦ ╦╔╗╔╗╦╔╔═╗╔╗ ╦ ╦╦╦  ╔╦╗╔═╗ ╔═╗
                    ║ ║║║║║╠╣╠═╣╠╩╗║ ║║║   ║║╔═╝ ║ ║
                    ╚═╝╝╚╝╚╩╚╩ ╩╚═╝╚═╝╩╚═╝═╩╝╚═╝o╚═╝
{tagline.center(69)}
{copyright.center(69)}
{site.center(69)}
╚═════════════════════════════════════════════════════════════════════╝
	"""
	print(logo)

class UmkaBuild:
	def __init__(self):
		self.builds = {
			"build": {
				"app_name": None,
				"app_entry_point": None,
				"app_icon": None,
				"app_options": [],
				"app_folder": []
			},
			"build_command_menu": {
				"1": self.settings,
				"2": self.fist_build,
				"3": self.new_options,
				"4": self.delete,
				"5": self.change_language
			}
		}

		self.loads = load_the_json()

		lang = get_saved_language(self.loads)
		if not lang:
			print("⚠️ Language dictionary not loaded. Falling back to Ukrainian.")
			self.lang = translations['uk']
			self.loads['language'] = lang
			save_build_to_json(self.loads)
		self.lang = set_language(lang)

		show_ascii_logo(self.lang)

		if self.is_source_emty():
			print(self.lang['source_empty'])
			return

		self.build_command = None
		self.list_commands = False
		self.autoload_add_data()
		self.build_menu()

	def autoload_add_data(self):
		if os.path.exists(SOURCE_PATH):
			for root, dirs, files in os.walk(SOURCE_PATH):
				for folder in dirs:
					full_path = os.path.join(root, folder)
					relative_path = os.path.relpath(full_path, SOURCE_PATH)

					if folder == '__pycache__':
						continue

					add_data = f'--add-data "{full_path};{relative_path}"'
					self.builds['build']['app_folder'].append(add_data)

	def detect_project_files(self):
		py_files = []
		ico_file = None

		for file in os.listdir(SOURCE_PATH):
			if file.endswith(".py"):
				py_files.append(file)
			elif file.endswith(".ico") and ico_file is None:
				ico_file = file

		if not py_files:
			print(self.lang['no_search_file'])
			return None, ico_file

		if len(py_files) == 1:
			print(self.lang['search_file'], py_files[0], "\n")
			entry_point = py_files[0]
		else:
			print(self.lang['search_multiple_file'])
			for i, file in enumerate(py_files, start = 1):
				print(f"[{i}]. {file}")

			choice = input(self.lang['enter_file_number']).strip()
			try:
				index = int(choice) -1
				entry_point = py_files[index]
			except (ValueError, IndexError):
				print(self.lang['invalid_selection'])
				return None, ico_file
		return os.path.join(SOURCE_PATH, entry_point), os.path.join(SOURCE_PATH, ico_file) if ico_file else None

	def item_lists(self, ids):
		items = self.loads.get(ids, [])
		if items:
			print(self.lang['list'])
			for i, item in enumerate(items, start = 1):
				n = '\n' if self.list_commands == True else ''
				print(f"[{i}]. {item}{n}")
		return items

	def build_menu(self):
		print(self.lang['menu'])
		self.build_command = input(self.lang['select_command'])
		if self.build_command in self.builds['build_command_menu']:
			self.builds['build_command_menu'][self.build_command]()

	def settings(self):
		name = input(self.lang['enter_name'])
		if not name:
			print(self.lang['no_application_name'])
			return
		entry_point, icon_path = self.detect_project_files()
		if not entry_point:
			return

		self.builds['build']['app_name'] = name
		self.builds['build']['app_entry_point'] = entry_point
		self.builds['build']['app_icon'] = icon_path
		if not self.options():
			return
		self.fist_build()

	def options(self):
		add_options = input(self.lang['add_options'])
		if not add_options in ('1', '0'):
			print(self.lang['invalid_selection'])
			return
		option_run = True if add_options == '1' else False
		
		if not option_run:
			return True
			
		name = 'options_name'
		items = self.item_lists(name)
		if not items:
			print(self.lang['list_is_empty'])
			return

		option = input(self.lang['enter_options']).strip()
		value_option = option.split(' ')
			
		invalid_input = False
		for value in value_option:
			try:
				i = int(value) -1
				if 0 <= i < len(items):
					self.builds['build']['app_options'].append(items[i])
				else:
					print(self.lang['invalid_option_id'], value, "\n")
					invalid_input = True
			except ValueError:
				print(self.lang['invalid_input_id'], f"'{value}'.", self.lang['enter_number'])
				invalid_input = True

		if invalid_input:
			print(self.lang['error_detected'])
			return False

		print(self.lang['selected_options'])
		for option in self.builds['build']['app_options']:
			print(f"{option}, ", end = '')
		return True

	def new_options(self):
		name = 'options_name'
		items = self.item_lists(name)
		if not items:
			print(self.lang['list_is_empty'])
			return

		option_run = True
		while option_run:
			option = input(self.lang['new_options'])
			self.loads['options_name'].append(option)
			save_build_to_json(self.loads)
			print(self.lang['option_successfull'])

			quit = input(self.lang['another_options'])
			option_run = True if quit == '1' else False

	def add_options_to_build(self):
		name = 'save_commands'
		self.list_commands = True
		items = self.item_lists(name)
		if not items:
			print(self.lang['list_is_empty'])
			return

		option = input(self.lang['enter_team_id'])
		try:
			i = int(option) -1
			if 0 <= i < len(items):
				option_save = self.loads['save_commands'][i]
				print(self.lang['selected_command'], option_save)
				return option_save
			else:
				print(self.lang['invalid_id'])
		except (ValueError, IndexError):
			print(self.lang['invalid_index'])

	def delete(self):
		delete_menu = input(self.lang['delete_input'])
		if delete_menu == '1':
			self.list_commands = True
			name = 'save_commands'
		elif delete_menu == '2':
			name = 'options_name'
		else:
			print(self.lang['invalid_selection'])
			return
		
		items = self.item_lists(name)
		if not items:
			print(self.lang['list_is_empty'])
			return

		delete = input(self.lang['enter_delete'])
		try:
			i = int(delete) -1
			if 0 <= i < len(items):
				removed = self.loads[name].pop(i)
				save_build_to_json(self.loads)
				print(self.lang['deleted'], removed, "\n")
			else:
				print(self.lang['invalid_id'])
		except (ValueError, IndexError):
			print(self.lang['invalid_index'])

	def fist_build(self):
		name = self.builds['build']['app_name']
		options = ' '.join(self.builds['build']['app_options'])
		folders = ' '.join(self.builds['build']['app_folder'])
		icon_path = self.builds['build']['app_icon']
		entry_point = self.builds['build']['app_entry_point']

		icon = ""
		if icon_path:
			icon = f'--add-data "{icon_path};." --icon={icon_path}'

		if self.build_command == '2':
			if self.loads['save_commands']:
				cmd = self.add_options_to_build()
			else:
				print(self.lang['saved_missing'])
				return
		else:
			cmd = f'--name "{name}" {options} {folders} {icon} {entry_point}'

		if cmd:
			if not self.list_commands:
				print(self.lang['generated_command'], cmd)

			build = input(self.lang['start_build'])
			if not build in ('1', '0'):
				print(self.lang['invalid_selection'])
				return
			build_run = True if build == '1' else False
			if build_run:
				self.build(cmd)
				self.list_commands = False

	def build(self, cmd):
		print(self.lang['build_ready'])
		self.check_pyinstaller()
		self.clean_provious_builds()
		subprocess.run(f'pyinstaller {cmd}', shell = True)
		print(self.lang['build_done'])

		save_command = input(self.lang['save_prompt'])
		if not save_command in ('1', '0'):
			print(self.lang['invalid_selection'])
			return
		build_to_save = True if save_command == '1' else False
		if build_to_save:
			self.loads['save_commands'].append(cmd)
			save_build_to_json(self.loads)
			print(self.lang['saved_success'])

	def change_language(self):
		lang = select_language()
		self.loads['language'] = lang
		save_build_to_json(self.loads)
		set_language(lang)

	def check_pyinstaller(self):
		try:
			subprocess.run(['pyinstaller', '--version'], check = True, stdout = subprocess.DEVNULL)
			return True
		except FileNotFoundError:
			print(self.lang['pyinstaller_missing'])
			return False

	def clean_provious_builds(self):
		for folder in ['build', 'dist']:
			if os.path.exists(folder):
				shutil.rmtree(folder)
		for file in os.listdir():
			if file.endswith(".spec"):
				os.remove(file)

	def is_source_emty(self):
		if not os.path.exists(SOURCE_PATH):
			os.makedirs(SOURCE_PATH)
			return True
		return not any(file.endswith('py') for file in os.listdir(SOURCE_PATH))


if __name__ == '__main__':
	if os.name == 'nt':
		subprocess.run('cls', shell = True)
	else:
		subprocess.run('clear', shell = True)
	UmkaBuild()