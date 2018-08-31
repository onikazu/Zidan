import subprocess
import a

if __name__ == "__main__":
    cmd = "python3 a.py"
    server = subprocess.Popen(cmd.split())
    while True:
        if a.flag == True:
            break

    print("a flag changed!!")