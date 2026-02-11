# Eyeball Jar

A simple python script to talk to an Ollama install on your machine.

I gave it a more meaningful name. 

I had an idea for a trivial task so I put copilot on it. Then I fiddled with it some more.

Perhaps I dream of making this a local instance of warp.dev? Do I dream?


## Usage

This script lets you send a question to an Ollama model running locally. It will attempt to start Ollama if it is not already running.

### Basic usage

```sh
python3 eyeball_jar.py "Your question here"
```

### Set the model

You can specify the model to use with the `--model` flag:

```sh
python3 eyeball_jar.py "Your question here" --model mistral:7b
```

The model setting will be saved in `settings.cfg` and used as the default for future runs. You can also edit `settings.cfg` directly:

```ini
[ollama]
model = mistral:7b
```

### Interactive mode

Add `--interactive` to enter a chat loop with the Ollama model. Each prompt is sent as a new question, and you can exit by typing `exit` or `quit`.

```sh
python3 eyeball_jar.py --interactive
```

You can combine with `--model` and `--debug`:

```sh
python3 eyeball_jar.py --interactive --model mistral:7b --debug
```

### Debug mode

Add `--debug` to print extra information about the Ollama CLI call:

```sh
python3 eyeball_jar.py "Your question here" --debug
```

### Example

```sh
python3 eyeball_jar.py "name all the albums released by the band Genesis"
```

---

I will probably work on this more when I have free time. Or you can help?