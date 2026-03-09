# Alfred Generate Commit Message Workflow

An Alfred workflow that generates concise, meaningful git commit messages from a description of your changes — powered by GPT-4o mini.

## Features

- Always produces a conventional commit prefix (`feat`, `fix`, `refactor`, etc.) — inferred from context when not provided
- Preserves existing prefixes and scopes if already present in the input
- Four style variants: default, conventional (strict), detailed (with body), short
- Copies the result directly to the clipboard — no Alfred clipboard action involved

## Requirements

- [Alfred](https://www.alfredapp.com/) with Powerpack
- Python 3 (macOS system Python at `/usr/bin/python3`)
- An [OpenAI API key](https://platform.openai.com/)

## Installation

1. Double-click `dist/Generate-Commit-Message.alfredworkflow` to install into Alfred.

2. On first import, enter your OpenAI API key and optionally set a custom keyword (default: `commit`).

## Usage

Open Alfred and type your keyword followed by a description of your changes:

```
commit add retry logic for failed API requests
```

Four options appear:

| Option | Output style |
|--------|-------------|
| **Generate Commit Message** | Concise subject line with inferred type prefix |
| **Generate Commit Message [Conventional]** | Strict Conventional Commits — always includes scope |
| **Generate Commit Message [Detailed]** | Subject line + explanatory body |
| **Generate Commit Message [Short]** | Ultra-brief, under 40 characters |

Select an option and press Enter. The commit message is copied to your clipboard.

### Examples

| Input | Output |
|-------|--------|
| `add retry logic for failed API requests` | `feat: add retry logic for failed API requests` |
| `fixed null pointer in user session` | `fix: resolve null pointer in user session` |
| `refactor(auth): implement strategy pattern for OAuth providers` | `refactor(auth): implement strategy pattern for OAuth providers` |
| `update readme` | `docs: update README` |

## Configuration

| Setting | Description |
|---------|-------------|
| **OpenAI API Key** | Your key from platform.openai.com |
| **Keyword** | Alfred trigger keyword (default: `commit`) |
