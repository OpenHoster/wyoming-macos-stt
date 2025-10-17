# Wyoming macOS STT

[Wyoming protocol](https://github.com/rhasspy/wyoming) server for Speech-to-Text on macOS, using [yap](https://github.com/finnvoor/yap) CLI tool to transcribe speech natively on Apple silicon for voice pipelines in Home Assistant.

## Features
- Single install command to run in the background and automatically on login
- Supports multiple [languages](wyoming_macos_stt/info.py)

For Text-to-Speech on macOS, check out [wyoming-macos-tts](https://github.com/openhoster/wyoming-macos-tts)

## Getting Started

### Requirements
- macOS 26
- [uv](https://github.com/astral-sh/uv)
- [yap](https://github.com/finnvoor/yap)

> These can be installed using [Homebrew](https://brew.sh) - `brew install uv finnvoor/tools/yap`

### Installing

1. Clone this repository and navigate into it:
    ```bash
    git clone https://github.com/openhoster/wyoming-macos-stt
    cd wyoming-macos-stt
    ```
2. Run the installer and follow the prompts:
    ```bash
    uv run script/install.py
    ```
    This will create a launcher file and optionally set it to run in the background and on login.
    
    By default the server will be available externally for devices on the local network. You can change this and other arguments by editing the launcher file `WyomingSTT`. 
    
    > To see all the available arguments, run: `uv run -m wyoming_macos_stt --help`
3. Adding to Home Assistant:  
   Add a new Wyoming service with the Mac’s host/IP and port `10300`.

### Uninstalling

Re-run the installer and, when prompted: `Run in the background and on login?` enter `n`

To completely remove all resources, delete the cloned repository folder.

### Development

- Install dev dependencies: 
    ```bash
    uv sync --extra dev
    ```
- Running in a terminal session:
    ```bash 
    uv run -m wyoming_macos_stt --help
    ```
- Running tests:
    ```bash 
    uv run -m pytest tests
    ```

---

If you find this usefull and want to support future projects:

<a href="https://www.buymeacoffee.com/openhoster" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50"/>
</a>
