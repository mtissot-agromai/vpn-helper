import sys
import os
import subprocess

COLOR = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m',

    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',

    'bg_black': '\033[40m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
    'bg_magenta': '\033[45m',
    'bg_cyan': '\033[46m',
    'bg_white': '\033[47m',
}

BASE_COMMAND = "openvpn3 "

def UNREACHABLE(args):
	print("This should be unreachable.\n")
	print("Arguments:")
	for arg in args:
		print(f"{arg}")
	exit(1)

def bw(text):
	return f"{COLOR['bold']}{text}{COLOR['reset']}"

def usage():
	print("\n")
	print("="*20)
	print("\nUSAGE:")
	print(f"{bw('vpn.py -l')} | {bw('vpn.py --list')}                 -> List all available configurations.")
	print(f"{bw('vpn.py -s')} | {bw('vpn.py --sessions')}             -> List all active sessions.")
	print(f"{bw('vpn.py -c CONFIG_NAME')}                     -> Connect to CONFIG_NAME.")
	print(f"{bw('vpn.py -d CONFIG_NAME')}                     -> Disconnect from CONFIG_NAME.")
	print(f"{bw('vpn.py --new CONFIG_FILE.ovpn CONFIG_NAME')} -> Create a configuration named CONFIG_NAME from CONFIG_FILE")
	print(f"{bw('vpn.py --rmc CONFIG_NAME')}                  -> Remove a configuration named CONFIG_NAME the configurations")
	print(f"{bw('vpn.py -h')} | {bw('vpn.py --help')}                 -> To see USAGE.")
	print()

def main(args):
	if len(sys.argv)>1:
		if "-l" in args or "--list" in args:
			verbose = False
			if ("-v" in args) or ("--verbose" in args):
				verbose = True
			print("Listing all configurations" + verbose*" in a verbose way" + ":")
			cmd = BASE_COMMAND + "configs-list" + verbose*" --verbose"
			proc = subprocess.run(cmd, shell=True)
			if proc.returncode == 0:
				return
			else:
				UNREACHABLE([f"{proc.returncode=}"])
			return
		if "-s" in args or "--sessions" in args:
			print("Listing all active sessions:")
			cmd = BASE_COMMAND + "sessions-list"
			proc = subprocess.run(cmd, shell=True)
			if proc.returncode == 0:
				return
			else:
				UNREACHABLE([f"{proc.returncode=}"])
			return
		if "-c" in args:
			index = args.index("-c")
			try:
				config_name = args[index+1]
			except Exception as e:
				print("You didn't provide a configuration name to connect to.")
				usage()
				exit(1)
			check_connections = subprocess.run("openvpn3 sessions-list", shell=True, capture_output=True, text=True)
			output = check_connections.stdout
			if f"Config name: {config_name}" in output and "Status: Connection, Client connected" in output:
				print(f"""{COLOR['red']}Connection to {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']} {COLOR['red']}unsuccessful{COLOR['reset']}.
You are already connected to this VPN""")
				return

			cmd = BASE_COMMAND + "session-start --config " + config_name
			proc = subprocess.run(cmd, shell=True)
			try:
				returnc = proc.returncode
				if returnc == 0:
					print(f"{COLOR['cyan']}Succesfully {COLOR['bold']}connected{COLOR['reset']}{COLOR['cyan']} to {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']}")
				else:
					print(f"""{COLOR['red']}Connection to {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']} {COLOR['red']}unsuccessful{COLOR['reset']}.
Check the available configurations using 'vpn.py -l' or 'vpn.py --list'""")
			except Exception as e:
				print(f"Exception: {e}")
				print(f"""Invalid config name: {config_name}.
-- Run {COLOR['bold']}vpn -l{COLOR['reset']} or {COLOR['bold']}vpn --list{COLOR['reset']} first to see available configurations.
-- You can also run {COLOR['bold']}vpn -h{COLOR['reset']} or {COLOR['bold']}vpn --help{COLOR['reset']} to see how to use the script.""")
			return
		if "-d" in args:
			if ("-h" in args) or ("--help" in args):
				print(f"""If you are having difficulty disconnecting, you can try removing it using the connection path.
Run {COLOR['bold']}vpn.py -s {COLOR['reset']}to show the path associated with each connection. Copy the path of the connection you want to disconnect from.
Run {COLOR['bold']}vpn.py -d -p PATH{COLOR['reset']} to remove it using its unique path.""")
				return
			path = False
			index = args.index("-d")
			if ("-p" in args):
				index = args.index("-p")
				path = True
			try:
				config_name = args[index+1]
			except Exception as e:
				print("You didn't provide a configuration name to disconnect from.")
				usage()
				exit(1)
			cmd_normal = BASE_COMMAND + "session-manage --config " + config_name + " --disconnect"
			cmd_path = BASE_COMMAND + "session-manage --path " + config_name + " --disconnect"
			cmd = cmd_path if path else cmd_normal
			proc = subprocess.run(cmd, shell=True)
			try:
				returnc = proc.returncode
				if returnc == 0:
					print(f"{COLOR['cyan']}Succesfully {COLOR['red']}{COLOR['bold']}disconnected {COLOR['reset']}{COLOR['cyan']}from {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']}")
				else:
					print(f"""{COLOR['red']}Could not disconnect from {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']}.
Check the available configurations using {COLOR['bold']}vpn -l{COLOR['reset']} or {COLOR['bold']}vpn --list{COLOR['reset']}.
Check the active sessions using {COLOR['bold']}vpn -s{COLOR['reset']} or {COLOR['bold']}vpn --sessions{COLOR['reset']}""")
					usage()
			except Exception as e:
				print(f"Exception: {e}")
				print(f"""Invalid config name: {config_name}.
-- Run {COLOR['bold']}vpn -s{COLOR['reset']} or {COLOR['bold']}vpn --sessions{COLOR['reset']} first to see active sessions.
-- Run {COLOR['bold']}vpn -l{COLOR['reset']} or {COLOR['bold']}vpn --list{COLOR['reset']} first to see available configurations.
-- You can also run {COLOR['bold']}vpn -h{COLOR['reset']} or {COLOR['bold']}vpn --help{COLOR['reset']} to see how to use the script.""")
				usage()
			return
		if ("--new" in args):
			index = args.index("--new")
			try:
				config_file = args[index+1]
				config_name = args[index+2]
			except Exception as e:
				print("You didn't provide a configuration file or configuration name.")
				usage()
				exit(1)
			cmd = BASE_COMMAND + "config-import --config " + config_file + " --name " + config_name
			proc = subprocess.run(cmd, shell=True)
			try:
				returnc = proc.returncode
				if returnc == 0:
					print(f"{COLOR['cyan']}Succesfully {COLOR['red']}{COLOR['bold']}created {COLOR['reset']}{COLOR['cyan']}config {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']} {COLOR['cyan']}from configuration file {COLOR['bold']}{config_file}{COLOR['reset']}")
				else:
					print(f"""{COLOR['red']}Could not create config {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']}{COLOR['cyan']} from {COLOR['bold']}{config_file}{COLOR['reset']}.""")
					usage()
			except Exception as e:
				print(f"Exception: {e}")
				print(f"""Invalid configuration file: {config_file}.
-- Run 'vpn -h' or 'vpn --help' to see how to use the script.""")
				usage()
		if ("--rmc" in args):
			path = False
			if ("-h" in args) or ("--help" in args):
				print(f"""If you are having difficulty removing the configuration, you can try removing it using the configuration path.
Run {COLOR['bold']}vpn.py -l -v {COLOR['reset']}to show the path associated with each configuration. Copy the path of the configuration you want to delete.
Run {COLOR['bold']}vpn.py --rmc -p PATH{COLOR['reset']} to remove it using its unique path.""")
				return
			index = args.index("--rmc")
			if ("-p" in args):
				index = args.index("-p")
				path = True
			try:
				config_name = args[index+1]
			except Exception as e:
				print("You didn't provide a configuration name.")
				usage()
				exit(1)
			cmd_normal = BASE_COMMAND + "config-remove --config " + config_name
			cmd_path   = BASE_COMMAND + "config-remove --path " + config_name
			cmd = (not path)*cmd_normal + (path)*cmd_path
			proc = subprocess.run(cmd, shell=True)
			try:
				returnc = proc.returncode
				if returnc == 0:
					print(f"\n{COLOR['cyan']}Succesfully {COLOR['red']}{COLOR['bold']}removed {COLOR['reset']}{COLOR['cyan']}config {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']}")
				else:
					print(f"""\n{COLOR['red']}Could not remove config {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']}.
Are you sure this configuration exists? Try running {COLOR['bold']}vpn.py -l{COLOR['reset']} to make sure.
If you are typing the config name correctly, try running {COLOR['bold']}vpn.py --rmc -h{COLOR['reset']} to get help.""")
					usage()
			except Exception as e:
				print(f"\nException: {e}")
				print(f"""Invalid configuration name: {config_name}.
-- Run {COLOR['bold']}vpn -h{COLOR['reset']} or {COLOR['bold']}vpn --help{COLOR['reset']} to see how to use the script.""")
				usage()
		if "-h" in args or "--help" in args:
			usage()
			return
	else:
		usage()

if __name__ == '__main__':
	main(sys.argv)
