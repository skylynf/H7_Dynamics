import os
import re
import codecs

pattern = re.compile(r'[\u4e00-\u9fff]')
exts = ('.R', '.r', '.py')

for root, _, files in os.walk('.'):
    for fname in files:
        if not fname.lower().endswith(tuple(e.lower() for e in exts)):
            continue
        path = os.path.join(root, fname)
        try:
            with codecs.open(path, 'r', 'utf-8', errors='ignore') as fr:
                for idx, line in enumerate(fr, 1):
                    if pattern.search(line):
                        print(f"{path} 第{idx}行: {line.strip()}")
        except Exception as e:
            print(f"无法处理文件: {path}，原因: {e}")