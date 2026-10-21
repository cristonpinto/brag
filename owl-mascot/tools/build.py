"""Concatenate src/shapes.generated.js + src/owl.js into dist/owl-mascot.js (one file, no dependencies)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
out = '(function () {\n' + rd('src/shapes.generated.js') + '\n' + rd('src/owl.js') + '\n}).call(typeof window !== "undefined" ? window : globalThis);\n'
os.makedirs(os.path.join(ROOT, 'dist'), exist_ok=True)
open(os.path.join(ROOT, 'dist', 'owl-mascot.js'), 'w', encoding='utf-8').write(out)
print('dist/owl-mascot.js', len(out), 'bytes')
