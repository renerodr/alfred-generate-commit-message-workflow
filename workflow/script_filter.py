#!/usr/bin/python3
import sys
import json

STYLES = {"conventional", "detailed", "short"}

query = " ".join(sys.argv[1:]).strip()

def item(title, subtitle="", arg="", valid=True):
    return {"title": title, "subtitle": subtitle, "arg": arg, "valid": valid}

if not query:
    output = {"items": [item("Type or paste a description of your changes…", valid=False)]}
    print(json.dumps(output))
    sys.exit(0)

words = query.split()
if words[0].lower() in STYLES:
    style = words[0].lower()
    label = style.capitalize()
    output = {"items": [item(f"Generate Commit Message [{label}]", subtitle=query, arg=query)]}
    print(json.dumps(output))
    sys.exit(0)

output = {"items": [
    item("Generate Commit Message", subtitle=query, arg=query),
    item("Generate Commit Message [Conventional]", subtitle=query, arg=f"conventional {query}"),
    item("Generate Commit Message [Detailed]", subtitle=query, arg=f"detailed {query}"),
    item("Generate Commit Message [Short]", subtitle=query, arg=f"short {query}"),
]}
print(json.dumps(output))
