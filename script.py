import os
import subprocess
import sys

def install_packages():
    """Install necessary packages listed in requirements.txt."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

def main():
    """Main function to set up the environment."""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.isfile(requirements_path):
        print(f"{requirements_path} does not exist.")
        sys.exit(1)
    
    install_packages()

if __name__ == "__main__":
    main()
