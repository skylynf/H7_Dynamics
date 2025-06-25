import os
import re
import codecs

pattern = re.compile(r'[\u4e00-\u9fff]')
exts = ('.R', '.r', '.py')
total_cleaned = 0

for root, _, files in os.walk('.'):
    for fname in files:
        if not fname.lower().endswith(tuple(e.lower() for e in exts)):
            continue
        path = os.path.join(root, fname)
        print('检查文件:', path)
        try:
            with codecs.open(path, 'r', 'utf-8', errors='ignore') as fr:
                lines = fr.readlines()
        except Exception as e:
            print(f"无法处理文件: {path}，原因: {e}")
            continue

        changed = False
        new_lines = []
        for line in lines:
            if '#' in line:
                code_part, comment_part = line.split('#', 1)
                if pattern.search(comment_part):
                    if code_part.strip():
                        new_lines.append(code_part.rstrip() + '\n')
                    changed = True
                    total_cleaned += 1
                    continue
            new_lines.append(line)

        if changed:
            try:
                with codecs.open(path, 'w', 'utf-8') as fw:
                    fw.writelines(new_lines)
                print('cleaned', path)
            except Exception as e:
                print(f"无法写入文件: {path}，原因: {e}")

print(f'共清理了 {total_cleaned} 行含中文注释。')
