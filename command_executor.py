import subprocess
import shlex
import os
import re
import getpass

def evaluate_arithmetic(command):
    pattern = r'^\s*(-?\d+(?:\.\d*)?)\s*([\+\-\*/])\s*(-?\d+(?:\.\d*)?)\s*$'
    match = re.match(pattern, command)
    if match:
        num1, op, num2 = match.groups()
        num1, num2 = float(num1), float(num2)
        try:
            if op == '+':
                return str(num1 + num2) + "\n"
            elif op == '-':
                return str(num1 - num2) + "\n"
            elif op == '*':
                return str(num1 * num2) + "\n"
            elif op == '/':
                if num2 == 0:
                    return "Error: Division by zero\n"
                return str(num1 / num2) + "\n"
        except Exception as e:
            return f"Error: {str(e)}\n"
    return None

def execute_command(command, current_dir):
    command = command.strip()
    if not command:
        return "", current_dir

    # Check arithmetic
    arithmetic_result = evaluate_arithmetic(command)
    if arithmetic_result is not None:
        return arithmetic_result, current_dir

    # Built-in commands
    if command == "clear":
        return "\033c", current_dir

    if command.startswith("cd "):
        path = command[3:].strip()
        try:
            new_dir = os.path.abspath(os.path.join(current_dir, os.path.expanduser(path)))
            if os.path.isdir(new_dir):
                return "", new_dir
            else:
                return f"cd: no such directory: {path}\n", current_dir
        except Exception as e:
            return f"cd error: {str(e)}\n", current_dir

    if command == "pwd":
        return current_dir + "\n", current_dir

    if command == "ls":
        try:
            files = os.listdir(current_dir)
            return "\n".join(files) + "\n", current_dir
        except Exception as e:
            return f"ls error: {str(e)}\n", current_dir

    # New commands:

    if command.startswith("mkdir "):
        folder = command[6:].strip()
        try:
            os.mkdir(os.path.join(current_dir, folder))
            return "", current_dir
        except Exception as e:
            return f"mkdir error: {str(e)}\n", current_dir

    if command.startswith("rmdir "):
        folder = command[6:].strip()
        try:
            path = os.path.join(current_dir, folder)
            if os.path.isdir(path):
                os.rmdir(path)
                return "", current_dir
            else:
                return f"rmdir: no such directory: {folder}\n", current_dir
        except Exception as e:
            return f"rmdir error: {str(e)}\n", current_dir

    if command.startswith("rm "):
        file = command[3:].strip()
        try:
            path = os.path.join(current_dir, file)
            if os.path.isfile(path):
                os.remove(path)
                return "", current_dir
            else:
                return f"rm: no such file: {file}\n", current_dir
        except Exception as e:
            return f"rm error: {str(e)}\n", current_dir

    if command.startswith("touch "):
        file = command[6:].strip()
        try:
            path = os.path.join(current_dir, file)
            with open(path, 'a'):
                os.utime(path, None)
            return "", current_dir
        except Exception as e:
            return f"touch error: {str(e)}\n", current_dir

    if command.startswith("cat "):
        file = command[4:].strip()
        try:
            path = os.path.join(current_dir, file)
            with open(path, 'r') as f:
                content = f.read()
            return content + "\n", current_dir
        except Exception as e:
            return f"cat error: {str(e)}\n", current_dir

    if command.startswith("echo "):
        text = command[5:].strip()
        return text + "\n", current_dir

    if command == "whoami":
        user = getpass.getuser()
        return user + "\n", current_dir

    # External commands
    try:
        result = subprocess.run(shlex.split(command), cwd=current_dir,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        output = result.stdout + result.stderr
        return output, current_dir
    except Exception as e:
        return f"Error: {str(e)}\n", current_dir
