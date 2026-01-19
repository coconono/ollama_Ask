#!/usr/bin/env python3
import subprocess
import sys
import time

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
    args = sys.argv[1:]
    if '--debug' in args:
        debug = True
        args.remove('--debug')
    if len(args) < 1:
        print("Usage: python3 ask_ollama.py 'Your question here' [--debug]")
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
                    print("Ollama started successfully.")
                    break
            else:
                print("Failed to start Ollama.")
                sys.exit(1)
        except Exception as e:
            print(f"Error starting Ollama: {e}")
            sys.exit(1)
    else:
        print("Ollama is running.")
    try:
        # Use Ollama CLI to send the question
        result = subprocess.run([
            "ollama", "run", "ministral-3:3b", question
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if debug:
            print("--- DEBUG: Ollama CLI stdout ---")
            print(result.stdout)
            print("--- DEBUG: Ollama CLI stderr ---")
            print(result.stderr)
            print(f"--- DEBUG: Return code: {result.returncode} ---")
        if result.returncode == 0:
            print("Ollama response:")
            print(result.stdout.strip())
        else:
            print(f"Failed to get response from Ollama CLI. Error: {result.stderr.strip()}")
    except Exception as e:
        print(f"Error communicating with Ollama CLI: {e}")

if __name__ == "__main__":
    main()
