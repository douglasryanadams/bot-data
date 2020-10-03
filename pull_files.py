import os
import paramiko
import yaml


with open(r'config.yml') as f:
    """
    Config Foramt:
    hosts:
      -
        ipv4:
        ipv6:
        domain:
        price:
        vps:
        location:
        root_password:
        username:
        password:
        log_directory:
    output_directory:
    """
    config = yaml.load(f, Loader=yaml.FullLoader)

output_dir = config['output_directory']
os.makedirs(output_dir, exist_ok=True)

ssh = paramiko.SSHClient()

ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))

for host in config['hosts']:
  ipv4 = host['ipv4']
  username = host['username']
  password = host['password']

  log_dir = host['log_directory']
  remote_path = f"{log_dir}/access_v4.log"
  local_path = f"{output_dir}/{ipv4}_access_v4.log"

  print(f"Connecting to <{ipv4}> as <{username}>")
  ssh.connect(ipv4, username=username, password=password)
  sftp = ssh.open_sftp()
  print(f"Pulling {ipv4}:{remote_path} to {local_path}")
  sftp.get(remote_path, local_path)

  sftp.close()
  ssh.close()

