# Code Collect

Interactive CLI tool to collect and format multiple code files for sharing with LLMs. Select files with a fuzzy finder, get perfectly formatted output copied to your clipboard.

## Why?

When working with LLMs on coding tasks, you often need to share multiple files for context. Code Collect makes this effortless by:

- 🎯 **Interactive selection** - Pick exactly the files you need with fuzzy search
- 📋 **Perfect formatting** - Files formatted with paths and syntax highlighting  
- 🚀 **One command** - From selection to clipboard in seconds
- 🧠 **Smart filtering** - Ignores binaries, build files, and common junk

## Demo

```bash
$ code-collect
Scanning /Users/you/project...
Found 34 eligible files.
# Interactive fzf interface opens
Processing 6 files...
✅ Copied 6 files to clipboard!
```

Output format:
```
// src/components/Button.tsx
```typescript
export const Button = () => {
  return <button>Click me</button>
}
```

// src/utils/helpers.py  
```python
def format_data(data):
    return data.strip()
```
```

## Installation

### Prerequisites
- Python 3.6+
- [fzf](https://github.com/junegunn/fzf) - `brew install fzf` (macOS) or `apt install fzf` (Ubuntu)

### Quick Install
```bash
curl -sSL https://raw.githubusercontent.com/amadsalman/code-collect/main/install.sh | bash
```

### Manual Install
```bash
# Clone the repository
git clone https://github.com/amadsalman/code-collect.git
cd code-collect

# Run the install script
./install.sh
```

### Alternative Manual Install
```bash
# Download the script directly
curl -o code-collect https://raw.githubusercontent.com/amadsalman/code-collect/main/code-collect
chmod +x code-collect

# Make it globally available
sudo mv code-collect /usr/local/bin/
```

## Usage

```bash
# Run in current directory
code-collect

# Run in specific directory  
code-collect /path/to/project
```

### Controls
- **Arrow keys** - Navigate files
- **Tab** - Multi-select files
- **Enter** - Confirm selection
- **Esc** - Cancel

## Features

- **Smart file detection** - Only shows text files, skips binaries
- **Intelligent filtering** - Ignores `.git`, `node_modules`, build directories
- **Size limits** - Skips files over 1MB
- **Syntax highlighting** - Proper language detection for 30+ file types
- **Cross-platform** - Works on macOS, Linux, Windows (with WSL)

## What gets ignored?

- Binary files and executables
- Common build/cache directories (`.git`, `node_modules`, `dist`, `build`, etc.)
- IDE files (`.vscode`, `.idea`)
- Large files (>1MB)

## Contributing

Issues and PRs welcome! This tool was built to scratch a specific itch - making LLM context sharing effortless.

## License

MIT
