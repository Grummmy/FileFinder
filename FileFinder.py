from sys import argv, exit
from os import walk, getcwd, startfile
from tqdm import tqdm

founds = {"Папки": []}

if len(argv) > 1 and argv[1][0] == "c":
    def slash(text: str):
        return text.replace("\\", '\033[90m\\\033[0m')

    def bold(text: str, b: str):
        i = text.lower().find(b.lower())
        return f"{text[:i]}\033[34m\033[1m{text[i:i+len(b)]}\033[0m{text[i+len(b):]}"

    def Result():
        global founds

        if not founds['Папки']:
            del founds['Папки']

        for ext, files in founds.items():
            print(f" -> {ext}:")
            i = 20
            for file in files:
                if i >= 20:
                    input(" - Press \033[1mEnter\033[0m to load more results ")
                    i = 0

                i += 1
                print(f"{file[0].ljust(30)}: {slash(file[1])}")

            print("")

        exit(0)

else:
    def slash(text: str):
        return text.replace("\\", '<span class="slash">\\</span>')

    def bold(text: str, b: str):
        i = text.lower().find(b.lower())
        return f"{text[:i]}<b>{text[i:i+len(b)]}</b>{text[i+len(b):]}"

    def Result():
        global founds
        log = []

        if not founds['Папки']:
            del founds['Папки']

        for ext, files in tqdm(founds.items(), desc="Логирование", unit="файл", colour="green"):
            log.append(f"  <h2>{ext}</h2>\n  <hr>\n  <table>")
            for file in files:
                log.append(f"    <tr>\n      <td>{file[0]}</td>")
                log.append(f'      <td class="copy-cell">{slash(file[1])}</td>\n    </tr>')
            log.append("  </table>\n  <br>")

        with open(f"!Search Results.html", 'w', encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Результаты поиска</title>
    <link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2024%22%3E%3Ctext%20x%3D%222%22%20y%3D%2218%22%20font-size%3D%2220%22%3E%F0%9F%94%8E%3C%2Ftext%3E%3C%2Fsvg%3E" type="image/svg+xml">
</head>
<body>
    {"\n".join(log)}
<style>
    body {{
        max-width: 95%;
        margin-left: auto;
        margin-right: auto;
        background-attachment: fixed;
        background: linear-gradient(to right, #0f5353, #11253f, #113928);
        color: rgb(255, 255, 255);
        font-family: system-ui, monospace;
    }}
    h2 {{
        text-align: center;
    }}
    .copy-cell {{
        padding-left: 50px;
        color: rgb(130, 159, 255);
    }}
    .slash {{
        color: rgb(18, 159, 20);
        font-weight: bold;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
    	padding: 10px;
    }}
    tr {{
        max-width: 100%;
        display: grid;
        margin: 10px 0;
        padding: 8px;
        background-color: #2b4b4b;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    table td:nth-child(1) {{
        word-break: break-all;
    }}
    table td:nth-child(2) {{
        word-break: break-all;
    }}
    hr {{
        border-color: #ffd900;
    }}
    b {{
        color: rgb(207, 147, 36);
    }}
</style>
</body>
</html>""")

def search(targets, path=getcwd()):
    global founds
    for root, dirs, files in tqdm(walk(path), desc="Search", unit="files", colour="green"):
        for name in dirs:
            for target in targets:
                if target in name.lower():
                    founds['Папки'].append((bold(name, target), root))
        for name in files:
            for target in targets:
                if target in name.lower():
                    ext = name[name.rfind('.')+1:]
                    if ext in founds:
                        founds[ext].append((bold(name, target), root))
                    else:
                        founds[ext] = [(bold(name, target), root)]

target = input('Что здесь найти? \n').lower().strip()
if "cheat" in target or "чит" in target:
	targets = [
        '.akr', '.wex', 'akrien', 'akrienantileek', 'archware', 'autochest', 'betterclicker', 'boberware',
        'celestial', 'cheststealer', 'deadcode', 'destroy', 'editme', 'eternity', 'exloader', 'flauncher',
        'freecam', 'future', 'gishcode', 'impact', 'inertia', 'jigsaw', 'konas', 'matix', 'mousetweaks',
        'nightmare', 'norender', 'norules', 'nursultan', 'pyro', 'r3d', 'rich', 'richpremium', 'rusherhack',
        'sigma', 'vape', 'wexside', 'wild', 'wintware', 'wurst', 'zamorozka', 'ares', 'aristois', 'baritone',
        'bleachhack', 'cabaletta', 'celka', 'xray', 'cortex', 'dauntiblyat', 'doomsday', 'hitbox', 'hits',
        'itemscroller', 'liquidbounce', 'mc100', 'meteor', 'nuric', 'pivo', 'rename_me_please','troxil', 'x-ray'
    ]
else:
	targets = set(target.strip().split())

print(f"\nОтлично, ищу {target} в {getcwd()}")

search(targets)
Result()

print("\nРезультаты поиска записаны как \033[1m!Search Results.html\033[0m")
print("Открыть получившийся файл можно в \033[1mлюбом браузере\033[0m\n")
startfile("!Search Results.html")
