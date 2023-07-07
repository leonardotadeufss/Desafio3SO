import subprocess
import shutil
import sys
import os

def ls_clusters(host_name, filters=None):
    try:
        # Local ls command
        local_command = ["ls"]
        if filters:
            local_command.append(filters)
        os.chdir('home/so/Desafio3SO')
        local_output = subprocess.check_output(local_command).decode().splitlines()

        # Remote SSH ls command
        remote_command = ["ssh", host_name, "ls"]
        if filters:
            remote_command.append(filters)
        remote_command.append('/home/so/Desafio3SO')
        remote_output = subprocess.check_output(remote_command).decode().splitlines()

        # Compare file lists
        if local_output == remote_output:
            print("Files are the same:")
            print('\n'.join(local_output))
        else:
            print("Error: Files are not equal!")
    except subprocess.CalledProcessError as e:
        print("An error occurred:", str(e))


def copy_file(host_name, source_path, destination_path):
    try:
        # Local copy
        os.chdir('/home/so/Desafio3SO')
        shutil.copy(source_path, destination_path)
        print("File copied locally.")

        # Remote copy using SCP
        try:
            subprocess.run(['scp', source_path, f'{host_name}:/home/so/Desafio3SO/{destination_path}'], check=True)
            print("File copied to the remote machine.")
        except subprocess.CalledProcessError as e:
            print("An error occurred during remote copy:", str(e))
            # Undo the local copy if an error occurs on remote copy
            os.chdir(destination_path)
            os.remove(source_path)
            print("Local copy undone due to remote copy error.")
    except IOError as e:
        print("An error occurred during local copy:", str(e))


def move_file(host_name, source_path, destination_path):
    try:
        # Local move
        os.chdir('/home/so/Desafio3SO')
        shutil.move(source_path, destination_path)
        print("File moved locally.")

        # Remote move using SCP
        try:
            subprocess.run(['ssh', host_name, f'mv {source_path} /home/so/Desafio3SO/{destination_path}'], check=True)
            print("File moved to the remote machine.")
        except subprocess.CalledProcessError as e:
            print("An error occurred during remote move:", str(e))
            # Undo the local move if an error occurs on remote move
            shutil.move(destination_path, source_path)
            print("Local move undone due to remote move error.")
    except FileNotFoundError as e:
        print("An error occurred during local move:", str(e))



def change_file_permissions(host_name, file_name, permissions_list):
    try:
        # Local change of file permissions
        os.chdir('/home/so/Desafio3SO')
        subprocess.run(['chmod', permissions_list, file_name], check=True)
        print("File permissions changed locally.")

        # Remote change of file permissions using SSH
        try:
            subprocess.run(['ssh', host_name, f'chmod {permissions_list} /home/so/Desafio3SO/{file_name}'], check=True)
            print("File permissions changed on the remote machine.")
        except subprocess.CalledProcessError as e:
            print("An error occurred during remote change of file permissions:", str(e))
            # Undo the local change of file permissions if an error occurs on remote change
            os.chdir('/home/so/Desafio3SO')
            subprocess.run(['chmod', permissions_list, file_name], check=True)
            print("Local change of file permissions undone due to remote change error.")
    except subprocess.CalledProcessError as e:
        print("An error occurred during local change of file permissions:", str(e))


def create_user(host_name, username):
    try:
        # Local user creation
        subprocess.run(['sudo', 'useradd', username], check=True)
        print("User created locally.")

        # Remote user creation using SSH
        try:
            subprocess.run(['ssh', host_name, f'sudo useradd {username}'], check=True)
            print("User created on the remote machine.")
        except subprocess.CalledProcessError as e:
            print("An error occurred during remote user creation:", str(e))
            # Undo the local user creation if an error occurs on remote user creation
            subprocess.run(['sudo', 'userdel', '-r', username], check=True)
            print("Local user creation undone due to remote user creation error.")
    except subprocess.CalledProcessError as e:
        print("An error occurred during local user creation:", str(e))


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
