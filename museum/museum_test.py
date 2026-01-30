import json as js

entries = js.load(open("museum/sample_entry.json"))
for title in entries["database"]:
    print(title["title"])