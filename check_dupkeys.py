import ast, sys, collections
src=open('data.py').read()
tree=ast.parse(src)
dups=[]
for node in ast.walk(tree):
    if not isinstance(node, ast.Dict): continue
    keys=[k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value,str)]
    for k,n in collections.Counter(keys).items():
        if n>1: dups.append((node.lineno, k, n))
if dups:
    print('DUPLICATE KEYS (the last one silently wins):')
    for ln,k,n in dups: print(f'  data.py line {ln}: "{k}" x{n}')
    sys.exit(1)
print('no duplicate keys in any dict literal')
