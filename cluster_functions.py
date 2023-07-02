import subprocess
import shutil
import sys

def ls_clusters(host_name, filters=None):
    # Local ls command
    local_command = ["ls"]
    if filters:
        local_command.append(filters)
    local_output = subprocess.check_output(local_command)
    print("Local host - Files and directories:")
    print(local_output.decode())

    # Remote SSH ls command
    remote_command = ["ssh", host_name, "ls"]
    if filters:
        remote_command.append(filters)
    remote_output = subprocess.check_output(remote_command)
    print(f"{host_name} - Files and directories:")
    print(remote_output.decode())


def copy_file(host_name, source_path, destination_path):
    # Local copy
    shutil.copy(source_path, destination_path)

    # Remote copy using SCP
    try:
        subprocess.run(['scp', source_path, f'{host_name}:{destination_path}'], check=True)
        print("File copied to the remote machine.")
    except subprocess.CalledProcessError as e:
        print("An error occurred:", str(e))


def move_file(host_name, source_path, destination_path):
    # Local move
    shutil.move(source_path, destination_path)

    # Remote move using mv
    try:
        subprocess.run(['ssh', host_name, 'mv', source_path, destination_path], check=True)
        print("File moved to the remote machine.")
    except subprocess.CalledProcessError as e:
        print("An error occurred:", str(e))



def change_file_permissions(host_name, file_name, permissions_list):
    # Local execution
    try:
        subprocess.run(['chmod', permissions_list, file_name], check=True)
        print("File permissions changed locally.")
    except subprocess.CalledProcessError as e:
        print("An error occurred during local execution:", str(e))

    # Remote execution using SSH
    try:
        subprocess.run(['ssh', host_name, f'chmod {permissions_list} {file_name}'], check=True)
        print("File permissions changed on the remote machine.")
    except subprocess.CalledProcessError as e:
        print("An error occurred during remote execution:", str(e))


def create_user(host_name, username):
    # Local user creation
    try:
        subprocess.run(['sudo', 'useradd', username], check=True)
        print("User created locally.")
    except subprocess.CalledProcessError as e:
        print("An error occurred during local user creation:", str(e))

    # Remote user creation using SSH
    try:
        subprocess.run(['ssh', host_name, f'sudo useradd {username}'], check=True)
        print("User created on the remote machine.")
    except subprocess.CalledProcessError as e:
        print("An error occurred during remote user creation:", str(e))

def help():
    commands = {
        '[host_name] copy_file': ('Copy a file locally from source path to destination path and do the same on a remote machine.',
                      '[source_path]', '[destination_path]'),
        '[host_name] move_file': ('Move a file locally  from source path to destination path and do the same on a remote machine.',
                      '[source_path]', '[destination_path]'),
        '[host_name] change_file_permissions': ('Change the permissions of a file on a local and remote machine.',
                                    '[file_name]', '[permissions_list]'),
        '[host_name] create_user': ('Create a new user locally and on a remote machine.',
                        '[username]'),
        '[host_name] ls': ('List files and directories in a given path.','[filters]')
    }

    print()
    print("Available commands:")
    for command, info in commands.items():
        description, *parameters = info
        parameters_string = ' '.join(parameters)
        print(f"{command} {parameters_string}: {description}")
    print()
def main():
    command = sys.argv[1:]
    if len(command) == 0 or command[0] == "help" :
        help()
        return
    host_name = command[0]
    function_name = command[1]
    args = command[2:]


    if function_name == "ls":
        ls_clusters(host_name, *args)

    elif function_name == "copy_file":
        source_path = args[0]
        destination_path = args[1]
        copy_file(host_name,source_path, destination_path)

    elif function_name == "move_file":
        source_path = args[0]
        destination_path = args[1]
        move_file(host_name,source_path, destination_path)

    elif function_name == "change_file_permissions":
        file_name = args[0]
        permissions_list = args[1:]
        change_file_permissions(host_name, file_name, permissions_list)
    elif function_name == "create_user":
        username = args[0]
        create_user(host_name,username)
    else:
        print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
