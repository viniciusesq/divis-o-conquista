"""Algoritmos puros. Índices base zero; intervalos não vazios e inclusivos."""
from math import hypot, isfinite


def melhor(a, b):
    """Maior soma; em empate, menor início e depois menor fim."""
    return min(a, b, key=lambda r: (-r[0], r[1], r[2]))


def soma_bruta(v):
    if not v:
        raise ValueError('O vetor deve ter pelo menos um elemento.')
    resposta = (v[0], 0, 0)
    for i in range(len(v)):
        soma = 0
        for j in range(i, len(v)):
            soma += v[j]
            # Evita criar uma tupla em cada iteração sem melhoria.
            if soma > resposta[0]:
                resposta = (soma, i, j)
    return resposta


def soma_divisao(v):
    if not v:
        raise ValueError('O vetor deve ter pelo menos um elemento.')

    def resolver(lo, hi):
        if lo == hi:
            return (v[lo], lo, hi)
        meio = (lo + hi) // 2
        resposta = melhor(resolver(lo, meio), resolver(meio + 1, hi))
        soma = 0
        esquerda = None
        for i in range(meio, lo - 1, -1):
            soma += v[i]
            if esquerda is None or soma >= esquerda[0]:
                esquerda = (soma, i)
        soma = 0
        direita = None
        for j in range(meio + 1, hi + 1):
            soma += v[j]
            if direita is None or soma > direita[0]:
                direita = (soma, j)
        return melhor(resposta, (esquerda[0] + direita[0], esquerda[1], direita[1]))
    return resolver(0, len(v) - 1)


def soma_kadane(v):
    """Complemento O(n), incluído por precaução devido ao desafio citado."""
    if not v:
        raise ValueError('O vetor deve ter pelo menos um elemento.')
    soma, inicio = v[0], 0
    resposta = (soma, 0, 0)
    for j in range(1, len(v)):
        if soma < 0:
            soma, inicio = v[j], j
        else:
            soma += v[j]
        resposta = melhor(resposta, (soma, inicio, j))
    return resposta


def validar_pontos(pontos):
    if len(pontos) < 2:
        raise ValueError('São necessários pelo menos dois pontos.')
    if any(len(p) != 2 or not all(isfinite(x) for x in p) for p in pontos):
        raise ValueError('Cada ponto deve conter duas coordenadas finitas.')


def par_bruto(pontos):
    validar_pontos(pontos)
    resposta = (float('inf'), 0, 1)
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            d = hypot(pontos[i][0] - pontos[j][0], pontos[i][1] - pontos[j][1])
            if d < resposta[0]:
                resposta = (d, i, j)
    return resposta


def par_divisao(pontos, limiar=16):
    """Retorna (distância, id1, id2). Empates aceitam qualquer par ótimo.
    Mantém ordenação por y por intercalação, sem reordenar cada faixa.
    """
    validar_pontos(pontos)
    if limiar < 2:
        raise ValueError('O limiar deve ser >= 2.')
    px = sorted((x, y, i) for i, (x, y) in enumerate(pontos))
    # Duplicatas tornam a distância mínima zero; evita faixa degenerada.
    for a, b in zip(px, px[1:]):
        if a[:2] == b[:2]:
            return (0.0, min(a[2], b[2]), max(a[2], b[2]))

    def candidato(a, b):
        return (hypot(a[0] - b[0], a[1] - b[1]), min(a[2], b[2]), max(a[2], b[2]))

    def resolver(xs):
        if len(xs) <= limiar:
            resposta = (float('inf'), -1, -1)
            for i in range(len(xs)):
                for j in range(i + 1, len(xs)):
                    c = candidato(xs[i], xs[j])
                    if c[0] < resposta[0]:
                        resposta = c
            return resposta, sorted(xs, key=lambda p: (p[1], p[0], p[2]))
        meio = len(xs) // 2
        corte = xs[meio][0]
        a, ys1 = resolver(xs[:meio])
        b, ys2 = resolver(xs[meio:])
        resposta = a if a[0] <= b[0] else b
        ys, i, j = [], 0, 0
        while i < len(ys1) and j < len(ys2):
            if ys1[i][1] <= ys2[j][1]:
                ys.append(ys1[i]); i += 1
            else:
                ys.append(ys2[j]); j += 1
        ys.extend(ys1[i:]); ys.extend(ys2[j:])
        faixa = [p for p in ys if abs(p[0] - corte) < resposta[0]]
        for i, p in enumerate(faixa):
            for j in range(i + 1, min(i + 8, len(faixa))):
                q = faixa[j]
                if q[1] - p[1] >= resposta[0]:
                    break
                c = candidato(p, q)
                if c[0] < resposta[0]:
                    resposta = c
        return resposta, ys
    return resolver(px)[0]
