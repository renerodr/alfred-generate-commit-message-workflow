#!/usr/bin/python3
import sys
import os
import subprocess
import traceback
import json
import urllib.request

STYLES = {"conventional", "detailed", "short"}

STYLE_INSTRUCTIONS = {
    "conventional": (
        "Strictly follow Conventional Commits: <type>(<scope>): <description>. "
        "Always include a scope in parentheses — infer it from the context if not stated explicitly. "
        "Type must be one of: feat, fix, refactor, docs, chore, test, perf, style."
    ),
    "detailed": (
        "Write a subject line (under 72 characters, imperative mood) followed by a blank line "
        "and a short body (2-4 sentences) explaining what changed and why."
    ),
    "short": (
        "Write the shortest possible commit message — ideally under 40 characters. "
        "Imperative mood, no period."
    ),
}

def notify(title, message):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def main():
    raw = " ".join(sys.argv[1:]).strip()
    if not raw:
        notify("Generate Commit Message", "No description provided.")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        notify("Generate Commit Message", "OPENAI_API_KEY is not set.")
        sys.exit(1)

    words = raw.split()
    style = None
    if words[0].lower() in STYLES:
        style = words[0].lower()
        description = " ".join(words[1:]).strip()
    else:
        description = raw

    if not description:
        notify("Generate Commit Message", "No description provided.")
        sys.exit(1)

    system_prompt = (
        "You are an expert software developer writing git commit messages. "
        "Always produce a ready-to-use commit message — never ask for more context, never ask clarifying questions, never explain your output. "
        "Follow these rules strictly:\n"
        "1. ALWAYS start with a conventional commit type prefix: feat, fix, refactor, docs, chore, test, perf, or style.\n"
        "2. If the input already contains a conventional commit prefix (e.g. 'refactor(auth):'), preserve it exactly — do not change the type or scope.\n"
        "3. Include a scope in parentheses when the input mentions a specific area (e.g. auth, api, ui, db). Omit scope when generic.\n"
        "4. Write the subject in imperative mood, lowercase after the colon (e.g. 'feat: add retry logic').\n"
        "5. Keep the subject line under 72 characters.\n"
        "6. Output the subject line only — no body, no bullet points, no explanation.\n"
        "7. Distill long descriptions to the essential 'what', not the 'how'.\n"
        "Return ONLY the commit message subject line — no preamble, no quotes."
    )

    style_suffix = f"\n\n{STYLE_INSTRUCTIONS[style]}" if style else ""
    user_content = f"Write a git commit message for these changes:\n\n{description}{style_suffix}"

    few_shot_messages = [
        {"role": "user", "content": "Write a git commit message for these changes:\n\nfixed the login bug"},
        {"role": "assistant", "content": "fix: resolve login bug causing session expiry on refresh"},
        {"role": "user", "content": "Write a git commit message for these changes:\n\nupdated readme"},
        {"role": "assistant", "content": "docs: update README with setup instructions"},
        {"role": "user", "content": "Write a git commit message for these changes:\n\nrefactor(auth): implement strategy pattern for OAuth providers\nExtracted provider-specific logic into separate strategy classes implementing IOAuthProvider."},
        {"role": "assistant", "content": "refactor(auth): implement strategy pattern for OAuth providers"},
        {"role": "user", "content": "Write a git commit message for these changes:\n\nimplement query handling feature"},
        {"role": "assistant", "content": "feat: implement query handling"},
    ]

    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            *few_shot_messages,
            {"role": "user", "content": user_content},
        ],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    commit_msg = data["choices"][0]["message"]["content"].strip()

    subprocess.run(["pbcopy"], input=commit_msg.encode("utf-8"), check=True)
    notify("Generate Commit Message", "Commit message copied — press ⌘V to paste")

try:
    main()
except Exception as e:
    notify("Generate Commit Message", f"Error: {e}")
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
