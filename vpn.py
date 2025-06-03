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

def usage():
	print("\n")
	print("="*20)
	print("\nUSAGE:")
	print("vpn.py -l | vpn.py --list -> List all available configurations.")
	print("vpn.py -s | vpn.py --sessions -> List all active sessions.")
	print("vpn.py -c CONFIG_NAME -> Connect to CONFIG_NAME.")
	print("vpn.py -d CONFIG_NAME -> Disconnect from CONFIG_NAME.")
	print("vpn.py -h | vpn.py --help -> To see USAGE.")

def main(args):
	if len(sys.argv)>1:
		if "-h" in args or "--help" in args:
			print(f"You have added the flag for help. Voiding all other flags added.")
			usage()
			return
		if "-l" in args or "--list" in args:
			print("Listing all configurations:")
			cmd = BASE_COMMAND + "configs-list"
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
-- Run 'vpn -l' first to see available configurations.
-- You can also run 'vpn -h' or 'vpn --help' to see how to use the script.""")
			return
		if "-d" in args:
			index = args.index("-d")
			try:
				config_name = args[index+1]
			except Exception as e:
				print("You didn't provide a configuration name to disconnect from.")
				usage()
				exit(1)
			cmd = BASE_COMMAND + "session-manage --config " + config_name + " --disconnect"
			proc = subprocess.run(cmd, shell=True)
			try:
				returnc = proc.returncode
				if returnc == 0:
					print(f"{COLOR['cyan']}Succesfully {COLOR['red']}{COLOR['bold']}disconnected {COLOR['reset']}{COLOR['cyan']}from {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']}")
				else:
					print(f"""{COLOR['red']}Could not disconnect from {COLOR['yellow']}{COLOR['bold']}{config_name}{COLOR['reset']}.
Check the available configurations using 'vpn.py -l' or 'vpn.py --list'.
Check the active sessions using 'vpn.py -s' or 'vpn.py --sessions'""")
					usage()
			except Exception as e:
				print(f"Exception: {e}")
				print(f"""Invalid config name: {config_name}.
-- Run 'vpn -s' or 'vpn --sessions' first to see active sessions.
-- Run 'vpn -l' or 'vpn --list' first to see available configurations.
-- You can also run 'vpn -h' or 'vpn --help' to see how to use the script.""")
				usage()
			return
	else:
		usage()

if __name__ == '__main__':
	main(sys.argv)