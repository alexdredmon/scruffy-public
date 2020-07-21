import os
import shlex
import subprocess


def bash_source_file(filename):
	"""
	Equivalent of BASH "source" command to evaluate a script and set env vars
	"""
	if os.path.exists(filename):
	    command = shlex.split(f"bash -c 'source {filename} && env'")
	    proc = subprocess.Popen(command, stdout = subprocess.PIPE)
	    for line in proc.stdout:
	        (key, _, value) = line.decode().partition("=")
	        os.environ[key] = value.replace("\n", "")
	    proc.communicate()


def format_date(date):
    return date.strftime("%m-%d %a")


def get_env_var(key, default=None, data_type=str):
	value = os.environ.get(key, default)
	return data_type(value)


def growl_notification(
	text,
	title=None,
	subtitle=None,
	sound=None,
):
	"""
	Displays Growl notification
	:sound: refers to a file in one of the following directories:
		~/Library/Sounds
	     /System/Library/Sounds 
	"""
	command = f"display notification \"{text}\""
	if title:
		command += f" with title \"{title}\""
	if subtitle:
		command += f" subtitle \"{subtitle}\""
	if sound:
		command += f" sound name \"{sound}\""
	os.system(f"osascript -e '{command}'")


def set_icon(filename, icon):
	os.system(f"fileicon set {filename} {icon}")
