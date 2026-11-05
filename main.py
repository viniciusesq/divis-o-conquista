"""CLI sem mensagens extras, apropriada para redirecionamento de entrada."""
import argparse
import sys
from algoritmos import soma_bruta, soma_divisao, soma_kadane, par_bruto, par_divisao


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('problema', choices=['soma', 'pontos'])
    parser.add_argument('metodo', choices=['bruta', 'divisao', 'kadane'])
    args = parser.parse_args()
    tokens = sys.stdin.read().split()
    if not tokens:
        parser.error('Entrada vazia.')
    n = int(tokens[0])
    if args.problema == 'soma':
        if n < 1 or len(tokens) != n + 1:
            parser.error('Informe n >= 1 e exatamente n inteiros.')
        func = {'bruta': soma_bruta, 'divisao': soma_divisao, 'kadane': soma_kadane}[args.metodo]
        print(*func(list(map(int, tokens[1:]))))
    else:
        if args.metodo == 'kadane':
            parser.error('Kadane se aplica somente ao problema soma.')
        if n < 2 or len(tokens) != 2 * n + 1:
            parser.error('Informe n >= 2 e exatamente n pares de coordenadas.')
        valores = list(map(float, tokens[1:]))
        pontos = list(zip(valores[::2], valores[1::2]))
        func = par_bruto if args.metodo == 'bruta' else par_divisao
        d, i, j = func(pontos)
        print(f'{d:.12g} {i} {j}')


if __name__ == '__main__':
    main()
