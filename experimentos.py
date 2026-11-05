"""Medições reais; geração de entradas, validação e I/O fora do cronômetro."""
import csv
import json
import os
import platform
import random
import statistics
import time
from pathlib import Path
from algoritmos import *


def salvar_csv(path, linhas):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader(); w.writerows(linhas)


def executar():
    Path('resultados').mkdir(exist_ok=True)
    cpu = platform.processor()
    if Path('/proc/cpuinfo').exists():
        cpu = next((l.split(':', 1)[1].strip() for l in Path('/proc/cpuinfo').read_text().splitlines()
                    if l.startswith('model name')), cpu)
    memoria = next((l for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:')), '') if Path('/proc/meminfo').exists() else 'Não disponível'
    ambiente = {'python': platform.python_version(), 'sistema': platform.platform(), 'cpu': cpu,
                'cpus_logicas_visiveis': os.cpu_count(), 'memoria_host_visivel': memoria,
                'observacao': 'Ambiente remoto/virtualizado; recursos visíveis podem diferir da cota efetiva.',
                'data_utc': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
                'repeticoes': 5, 'semente_base': 20261026, 'limiar': 16}
    Path('resultados/ambiente.json').write_text(json.dumps(ambiente, indent=2, ensure_ascii=False), encoding='utf-8')
    linhas = []
    for n in [100, 200, 400, 800, 1600, 3200, 6400]:
        for rep in range(5):
            seed = 20261026 + n * 10 + rep
            rng = random.Random(seed)
            vetor = [rng.randint(-100, 100) for _ in range(n)]
            pontos = [(rng.uniform(-10000, 10000), rng.uniform(-10000, 10000)) for _ in range(n)]
            grupos = [('soma', vetor, [soma_bruta, soma_divisao, soma_kadane]),
                      ('pontos', pontos, [par_bruto, par_divisao])]
            for problema, dados, funcs in grupos:
                rng.shuffle(funcs)
                saidas = []
                for func in funcs:
                    func(dados[:min(32, n)])  # aquecimento curto, fora da medição
                    inicio = time.perf_counter_ns()
                    saida = func(dados)
                    duracao = time.perf_counter_ns() - inicio
                    linhas.append(dict(problema=problema, algoritmo=func.__name__, n=n,
                                       repeticao=rep+1, semente=seed, tempo_ns=duracao))
                    saidas.append(saida)
                if problema == 'soma':
                    assert all(s == saidas[0] for s in saidas)
                else:
                    assert abs(saidas[0][0] - saidas[1][0]) <= 1e-8
        print(f'n={n} concluído', flush=True)
    salvar_csv('resultados/medicoes_brutas.csv', linhas)
    resumo = []
    for problema, algoritmo, n in sorted({(r['problema'], r['algoritmo'], r['n']) for r in linhas}):
        tempos = [r['tempo_ns']/1e6 for r in linhas if (r['problema'], r['algoritmo'], r['n']) == (problema, algoritmo, n)]
        resumo.append(dict(problema=problema, algoritmo=algoritmo, n=n, media_ms=statistics.mean(tempos),
                           desvio_ms=statistics.stdev(tempos), minimo_ms=min(tempos), maximo_ms=max(tempos)))
    salvar_csv('resultados/resumo.csv', resumo)
    # Avaliação empírica do parâmetro em entradas independentes das principais.
    limiares = []
    for rep in range(5):
        rng = random.Random(8800 + rep)
        pontos = [(rng.random()*10000, rng.random()*10000) for _ in range(3200)]
        ordem = [2, 3, 8, 16, 32, 64]; rng.shuffle(ordem)
        for limiar in ordem:
            inicio = time.perf_counter_ns(); par_divisao(pontos, limiar)
            tempo = time.perf_counter_ns() - inicio
            limiares.append(dict(limiar=limiar, repeticao=rep+1, n=3200, semente=8800+rep, tempo_ns=tempo))
    salvar_csv('resultados/limiares.csv', limiares)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    for problema in ['soma', 'pontos']:
        fig, ax = plt.subplots(figsize=(8, 3.8))
        for algoritmo in sorted({r['algoritmo'] for r in resumo if r['problema'] == problema}):
            rs = sorted([r for r in resumo if r['algoritmo'] == algoritmo], key=lambda r: r['n'])
            ax.plot([r['n'] for r in rs], [r['media_ms'] for r in rs], 'o-', label=algoritmo)
        ax.set(xscale='log', yscale='log', xlabel='Tamanho da entrada (n)', ylabel='Tempo médio (ms)',
               title='Subarranjo de soma máxima' if problema == 'soma' else 'Par de pontos mais próximos')
        ax.grid(alpha=.25); ax.legend(); fig.tight_layout()
        fig.savefig(f'resultados/grafico_{problema}.png', dpi=170); plt.close(fig)
    return resumo


if __name__ == '__main__':
    executar()
