import itertools
import json
import math
import random
from pathlib import Path
from algoritmos import *


def executar():
    casos = json.loads(Path('casos_teste.json').read_text(encoding='utf-8'))
    total = 0
    for c in casos['soma']:
        for func in [soma_bruta, soma_divisao, soma_kadane]:
            assert list(func(c['entrada'])) == c['esperado'], (func.__name__, c)
            total += 1
    for c in casos['pontos']:
        for func in [par_bruto, par_divisao]:
            d, i, j = func(c['entrada'])
            assert math.isclose(d, c['distancia_esperada'], rel_tol=1e-10, abs_tol=1e-10)
            assert [i, j] in c['pares_aceitos'], (func.__name__, c, i, j)
            total += 1
    # Oráculo independente: enumera intervalos e soma por slicing (O(n³)).
    for n in range(1, 7):
        for v in itertools.product([-1, 0, 1], repeat=n):
            esperado = min(((sum(v[i:j+1]), i, j) for i in range(n) for j in range(i, n)),
                           key=lambda r: (-r[0], r[1], r[2]))
            for func in [soma_bruta, soma_divisao, soma_kadane]:
                assert func(v) == esperado
                total += 1
    rng = random.Random(270)
    for k in range(300):
        n = rng.randint(2, 100)
        pontos = [(rng.randint(-30, 30), rng.randint(-30, 30)) for _ in range(n)]
        if k % 3 == 0:
            pontos = [(0, y) for _, y in pontos]
        esperado = par_bruto(pontos)[0]
        for limiar in [2, 3, 8, 16, 32]:
            d, i, j = par_divisao(pontos, limiar)
            assert i != j and 0 <= i < n and 0 <= j < n
            assert math.isclose(d, esperado, rel_tol=1e-10, abs_tol=1e-10)
            assert math.isclose(d, math.dist(pontos[i], pontos[j]), abs_tol=1e-10)
            total += 1
    for func, entrada in [(soma_bruta, []), (soma_divisao, []), (soma_kadane, []),
                          (par_bruto, []), (par_divisao, [(1, 2)]), (par_divisao, [(0, 0), (math.nan, 1)])]:
        try:
            func(entrada)
        except ValueError:
            total += 1
        else:
            raise AssertionError('Entrada inválida aceita')
    resultado = f'{total} verificações concluídas sem falhas.'
    print(resultado)
    Path('resultado_testes.txt').write_text(resultado + '\n', encoding='utf-8')
    return total


if __name__ == '__main__':
    executar()
