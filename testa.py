import importlib
import inspect
import itertools
import sys
from collections import defaultdict
from pathlib import Path
from pprint import pprint

arquivos = Path('./testes').glob('teste_*.py')
print(list(arquivos))
resultados = defaultdict(list)

for arquivo in arquivos:
    modulo = importlib.import_module(
            str(arquivo).rstrip('.py').replace('/', '.')
    )
    pprint(f"-> {modulo.__name__}")
    testes = [
        objeto for nome, objeto in inspect.getmembers(modulo)
        if nome.startswith('teste_') and callable(objeto)
    ]
    for função in testes:
        try:
            função()
        except AssertionError as e:
            resultados['falhas'].append((função, e))
            pprint(f" \-> {função.__name__} - falhou - {e} ")
        except Exception as e:
            resultados['erros'].append((função, e))
            pprint(f" \-> {função.__name__} - deu erro - {e} ")
        else:
            resultados['sucessos'].append((função, None))
            pprint(f" \-> {função.__name__} - passou ")

print('_' * 20)
print(f"Coletados: {len(list(itertools.chain(*resultados.values())))}")
for categoria, resultado in resultados.items():
    print(f"{categoria.title()} - {len(resultado)}")

sys.exit(len(resultados['falhas'] + resultados['erros']) > 0)

