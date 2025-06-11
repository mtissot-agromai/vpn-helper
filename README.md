# VPN Helper

Helper script to connect and disconnect from VPNs using [OpenVPN3](https://openvpn.net/cloud-docs/tutorials/configuration-tutorials/connectors/operating-systems/linux/tutorial--learn-to-install-and-control-the-openvpn-3-client.html)

### Quickstart

How to list all available configurations, connect to a configuration, see all active sessions and then disconnect:
```sh
python vpn.py -l
python vpn.py -c CONFIG_NAME
python vpn.py -s
python vpn.py -d CONFIG_NAME
```

To create a new configuration named `config_name` from a `config_file.ovpn`, run:
```sh
python vpn.py --new config_file.ovpn config_name
```

To remove a configuration named `config_to_remove` from your configurations, run:
```sh
python vpn.py --rmc config_to_remove
```

For help, use
```sh
python vpn.py -h
python vpn.py --help
```

### Good practices:
Add an alias to your .bash_aliases with
```bash
alias vpn='python /path/to/vpn.py'
```

If you only ever connect to one VPN, consider creating an alias for connecting/disconnecting from that VPN:
```bash
alias vpn='python /path/to/vpn.py'
alias vpnc='python /path/to/vpn.py -c CONFIG_NAME'
alias vpnd='python /path/to/vpn.py -d CONFIG_NAME'
```

#### To-dos:
Consider contributing by adding one or more of the features below:
1. Ability to connect to multiple configs from the same `-c` command, using `vpn -c CONFIG1 CONFIG2`
2. Ability to disconnect from multiple connections from the same `-d` command, using `vpn -d CONFIG1 CONFIG2`
3. Ability to add a new config from a config file `config.ovpn` by using `vpn -a config.ovpn CONFIG_NAME` or `vpn --add config.ovpn CONFIG_NAME`

These suggestions are all pretty easy, but I have't had the need for any of them yet, so they are on the backlog.