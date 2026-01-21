#!/usr/bin/env python3
import subprocess
import sys
import time
import configparser
import os

def is_ollama_running():
    try:
        # Check if any process contains 'ollama' in its name
        result = subprocess.run(['pgrep', '-f', 'ollama'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking Ollama status: {e}")
        return False

def main():
    debug = False
    model = None
    args = sys.argv[1:]
    # Parse flags
    if '--debug' in args:
        debug = True
        args.remove('--debug')
    if '--model' in args:
        idx = args.index('--model')
        if idx + 1 < len(args):
            model = args[idx + 1]
            del args[idx:idx+2]
        else:
            print("Error: --model flag requires a value.")
            sys.exit(1)
    # Read config file if model not set
    config_path = os.path.join(os.path.dirname(__file__), 'settings.cfg')
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
        if model is None:
            model = config.get('ollama', 'model', fallback=None)
    # If model is set, update config file
    if model:
        if not config.has_section('ollama'):
            config.add_section('ollama')
        config.set('ollama', 'model', model)
        with open(config_path, 'w') as f:
            config.write(f)
    if len(args) < 1:
        print("Usage: python3 eyeball_jar.py 'Your question here' [--debug] [--model MODEL]")
        sys.exit(1)
    question = args[0]
    print(f"Question: {question}")
    if not is_ollama_running():
        print("Ollama is NOT running. Attempting to start Ollama...")
        try:
            # Start Ollama in the background
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Wait for Ollama to start
            for _ in range(10):
                time.sleep(1)
                if is_ollama_running():
                    print("jiggling the eyeball jar")
                    break
            else:
                print("Failed to start Ollama.")
                sys.exit(1)
        except Exception as e:
            print(f"Error starting Ollama: {e}")
            sys.exit(1)
    else:
        print("jiggling the eyeball jar")
    try:
        # Use Ollama CLI to send the question
        if not model:
            print("Error: No model specified. Use --model flag or set in settings.cfg.")
            sys.exit(1)
        result = subprocess.run([
            "ollama", "run", model, question
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if debug:
            print("--- DEBUG: Ollama CLI stdout ---")
            print(result.stdout)
            print("--- DEBUG: Ollama CLI stderr ---")
            print(result.stderr)
            print(f"--- DEBUG: Return code: {result.returncode} ---")
        if result.returncode == 0:
            print("The eyeballs speak:")
            print(result.stdout.strip())
        else:
            print(f"Failed to get response from Ollama CLI. Error: {result.stderr.strip()}")
    except Exception as e:
        print(f"Error communicating with Ollama CLI: {e}")

if __name__ == "__main__":
    main()
