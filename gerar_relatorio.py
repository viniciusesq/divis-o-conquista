"""Recria o PDF usando apenas os resultados da execução atual."""
import csv
import json
import statistics
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from matplotlib.font_manager import findfont, FontProperties


def gerar():
    ambiente = json.loads(Path('resultados/ambiente.json').read_text())
    autores = json.loads(Path('autores.json').read_text(encoding='utf-8'))
    resumo = list(csv.DictReader(open('resultados/resumo.csv', encoding='utf-8')))
    limiares = list(csv.DictReader(open('resultados/limiares.csv', encoding='utf-8')))
    teste = Path('resultado_testes.txt').read_text(encoding='utf-8').strip()
    pdfmetrics.registerFont(TTFont('DejaVu', findfont(FontProperties(family='DejaVu Sans'))))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', findfont(FontProperties(family='DejaVu Sans', weight='bold'))))
    pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVu-Bold', italic='DejaVu', boldItalic='DejaVu-Bold')
    styles = getSampleStyleSheet()
    for style in styles.byName.values():
        style.fontName = 'DejaVu-Bold' if style.name.startswith('Heading') or style.name == 'Title' else 'DejaVu'
    styles.add(ParagraphStyle(name='Texto', fontName='DejaVu', fontSize=10.5, leading=15, spaceAfter=9))
    styles.add(ParagraphStyle(name='Pequeno', fontName='DejaVu', fontSize=8.5, leading=12, spaceAfter=6))
    styles['Title'].textColor = colors.HexColor('#15314c')
    styles['Heading1'].textColor = colors.HexColor('#15314c')
    story = []
    def p(t): story.append(Paragraph(t, styles['Texto']))
    def h(t): story.append(Paragraph(t, styles['Heading1']))
    def page(): story.append(PageBreak())
    def table(rows, widths=None):
        data = [[Paragraph(escape(str(c)), styles['Pequeno']) for c in row] for row in rows]
        t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e2edf5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#15314c')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f7f9')]),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story.append(t); story.append(Spacer(1,10))
    def media(alg,n):
        return float(next(r['media_ms'] for r in resumo if r['algoritmo']==alg and int(r['n'])==n))
    def f(x): return f'{x:.4f}'.replace('.', ',')
    story.append(Paragraph('Divisão e Conquista', styles['Title']))
    p('<b>Trabalho prático de Análise de Algoritmos</b><br/>Universidade de Fortaleza - Ciências da Computação')
    p('<br/>'.join(escape(a) for a in autores))
    h('1. Objetivo e organização')
    p('Implementar e comparar força bruta e divisão e conquista em dois problemas: subarranjo de soma máxima e par de pontos mais próximos. A comparação considera correção, complexidade e tempos medidos. Foi acrescentado Kadane, linear, como complemento à menção de um desafio O(n) nos critérios do enunciado.')
    p('A implementação foi feita em Python. Os algoritmos ficam separados da interface de entrada, dos testes e dos experimentos. O notebook permite reproduzir a execução no Google Colab; os arquivos .py também podem ser executados localmente.')
    h('Convenções e interpretações')
    p('Os índices começam em zero. O subarranjo é não vazio e seus extremos são inclusivos. Em empate de soma, escolhe-se o menor índice inicial e, depois, o menor final. Para pontos, aceita-se qualquer par ótimo, identificado pelos índices originais; as distâncias são euclidianas.')
    p('O enunciado não fornece o formato exato de um avaliador automático. A interface adotada está documentada no README. A palavra “dígitos” da Etapa 2 foi interpretada como número de pontos; o limiar foi interpretado como tamanho do caso-base recursivo.')
    p('<b>Proveniência:</b> os resultados deste PDF foram medidos em ambiente remoto, identificado na seção experimental. Não representam medições no computador pessoal dos integrantes. O script gerar_relatorio.py permite atualizar o documento após uma nova execução.')
    page()
    h('2. Subarranjo de soma máxima')
    p('<b>Força bruta:</b> para cada início i, percorrem-se os finais j e atualiza-se uma soma acumulada. São examinados n(n+1)/2 intervalos. A soma não é recalculada do zero, evitando uma terceira repetição.')
    p('Uma recorrência equivalente para a contagem do trabalho é B(n) = B(n-1) + Θ(n), com B(1) = Θ(1). Expandindo: B(n) = Θ(1 + 2 + ... + n) = Θ(n²). O espaço auxiliar é Θ(1), desconsiderando a entrada.')
    p('<b>Divisão e conquista:</b> divide-se o intervalo em duas metades. A solução está inteiramente à esquerda, inteiramente à direita ou cruza o meio. O terceiro caso é a soma do melhor sufixo da metade esquerda com o melhor prefixo da direita. A combinação custa Θ(n).')
    p('A recorrência é D(n) = D(⌊n/2⌋) + D(⌈n/2⌉) + Θ(n), com D(1) = Θ(1). Para potências de dois: D(n) = 2D(n/2) + Θ(n). Existem Θ(log n) níveis, cada um com trabalho total Θ(n); logo D(n) = Θ(n log n). A pilha recursiva ocupa Θ(log n).')
    p('<b>Correção:</b> os três casos cobrem todos os intervalos não vazios. Por indução, cada chamada fornece a solução ótima da sua metade. O melhor intervalo cruzado combina independentemente o maior sufixo e o maior prefixo. Escolher o melhor dos três preserva a otimalidade. O comparador também aplica a regra de desempate.')
    h('Complemento: Kadane')
    p('Mantém-se a melhor soma terminando na posição atual. Se a soma anterior é negativa, inicia-se um novo intervalo; caso contrário, estende-se o existente. Quando a soma anterior é zero, estender preserva o menor início no desempate. A resposta global é atualizada a cada elemento.')
    p('K(n) = K(n-1) + Θ(1), portanto K(n) = Θ(n), com espaço Θ(1). O estado inicial utiliza o primeiro elemento, não zero; assim, vetores inteiramente negativos retornam o maior elemento, e não um intervalo vazio.')
    p('Exemplo: para [-2, 3, -1, 4, -5], as três versões retornam soma 6, início 1 e fim 3. Para [-8, -3, -6], retornam soma -3 e extremos 1 e 1.')
    page()
    h('3. Par de pontos mais próximos')
    p('<b>Força bruta:</b> são comparados todos os n(n-1)/2 pares. A recorrência de contagem é B(n) = B(n-1) + Θ(n), com B(2) = Θ(1), resultando em Θ(n²). O espaço auxiliar é Θ(1). Usa-se hypot para calcular a distância euclidiana.')
    p('<b>Divisão e conquista:</b> os pontos são inicialmente ordenados por x, com y e identificador como desempate. A lista é dividida por posição, garantindo metades equilibradas mesmo quando vários pontos têm o mesmo x. Cada chamada retorna também seus pontos ordenados por y; as duas listas são intercaladas em tempo linear.')
    p('Seja δ a menor distância dos dois lados. Um par entre metades que melhore δ deve estar na faixa de largura 2δ em torno da divisão. A faixa é construída a partir da lista já ordenada por y. Cada ponto é comparado com no máximo os sete seguintes, interrompendo quando a diferença em y já é pelo menos a melhor distância.')
    h('Por que bastam sete vizinhos?')
    p('Para um ponto p, só interessam sucessores na faixa com diferença vertical menor que δ. Eles ficam num retângulo de largura 2δ e altura δ. Separando pelas duas metades recursivas, cada lado cabe num retângulo δ por δ, dividido em quatro células de lado δ/2. Dois pontos do mesmo lado na mesma célula teriam distância no máximo δ/√2, menor que δ, contradizendo a distância mínima daquele lado.')
    p('Há, portanto, no máximo oito pontos nesse retângulo, contando p: no máximo sete sucessores precisam ser examinados. Pontos com x igual ao corte continuam associados à sua metade recursiva. Fronteiras podem ser atribuídas de modo consistente às células; a busca exige melhora estrita, pois qualquer par empatado é aceito.')
    p('<b>Complexidade:</b> com limiar constante L, C(n) = 2C(n/2) + Θ(n) para n &gt; L, e C(n) = Θ(n²) para n ≤ L. Como L não cresce com n, o caso-base é limitado por uma constante. A ordenação inicial custa Θ(n log n) e a recorrência também; o total é Θ(n log n), com espaço auxiliar de pico O(n).')
    p('<b>Correção e duplicatas:</b> a melhor resposta ou está em uma metade ou aparece na faixa. A indução e a propriedade dos sete vizinhos cobrem ambos os casos. Coordenadas repetidas são detectadas após a ordenação inicial e retornam distância zero, que é ótima. Essa entrada pode terminar mais cedo; Θ(n log n) descreve o pior caso.')
    page()
    h('4. Testes e metodologia experimental')
    p('<b>Resultado da bateria:</b> ' + escape(teste))
    table([['Grupo','Cobertura e justificativa'],['9 casos fixos de soma','Negativos, unitários, zeros, empates, cruzamento, positivos e inteiros grandes.'],['8 casos fixos de pontos','Dois pontos, duplicatas, colinearidade, x iguais, negativos, frações, empates e par entre metades.'],['1.092 vetores exaustivos','Todos os vetores de tamanho 1 a 6 sobre {-1, 0, 1}. Oráculo independente enumera intervalos com soma direta.'],['300 conjuntos aleatórios','2 a 100 pontos; comparação com força bruta em limiares 2, 3, 8, 16 e 32. Validação dos IDs e da distância do par retornado.'],['Entradas inválidas','Vetor vazio, menos de dois pontos e coordenada não finita devem gerar ValueError.']], [125,365])
    p('As verificações fixas incluem saídas esperadas em casos_teste.json. Pontos usam tolerância de 10⁻¹⁰ nos testes. A validação automática reduz o risco de erro, mas não substitui a prova nem garante compatibilidade com um formato externo ainda desconhecido.')
    p('Foram usados n = 100, 200, 400, 800, 1.600, 3.200 e 6.400, com cinco execuções por tamanho e algoritmo. Os vetores usam inteiros uniformes de -100 a 100; os pontos usam coordenadas uniformes em [-10.000, 10.000]. Em cada repetição, os algoritmos do mesmo problema recebem a mesma entrada. Cada repetição usa uma semente diferente e reproduzível.')
    p('O cronômetro perf_counter_ns mede somente a chamada do algoritmo, incluindo a ordenação inicial na solução de pontos. Geração, impressão e validação ficam fora. Há aquecimento curto com até 32 elementos e ordem de execução embaralhada. Foram registradas 175 medições principais; o estudo de limiares acrescenta 30. O resumo contém média, desvio amostral, mínimo e máximo.')
    p('<b>Ambiente:</b> Python '+escape(ambiente['python'])+'; '+escape(ambiente['sistema'])+'. Processador visível: '+escape(ambiente['cpu'])+'. CPUs lógicas visíveis: '+str(ambiente['cpus_logicas_visiveis'])+'. '+escape(ambiente['memoria_host_visivel'])+'. Execução UTC: '+escape(ambiente['data_utc'])+'.')
    p('O ambiente é virtualizado e compartilhado; os recursos visíveis não garantem recursos exclusivos. Escalonamento, alocações e coleta de lixo podem influenciar os tempos. Não foi feito isolamento de CPU. Os experimentos principais não cobrem todas as distribuições de entrada.')
    page()
    h('5. Resultados: subarranjo de soma máxima')
    table([['n','Força bruta (ms)','Divisão (ms)','Kadane (ms)']]+[[n,f(media('soma_bruta',n)),f(media('soma_divisao',n)),f(media('soma_kadane',n))] for n in [100,200,400,800,1600,3200,6400]], [65,145,140,140])
    story.append(Image('resultados/grafico_soma.png',width=490,height=233))
    p('Figura 1. Médias de cinco execuções, em escalas logarítmicas nos dois eixos. O CSV permite consultar a dispersão; as linhas conectam apenas os tamanhos efetivamente medidos.')
    rb=media('soma_bruta',6400)/media('soma_bruta',3200)
    rd=media('soma_divisao',6400)/media('soma_divisao',3200)
    rk=media('soma_kadane',6400)/media('soma_kadane',3200)
    p(f'Ao dobrar n de 3.200 para 6.400, os fatores observados foram {rb:.2f} na força bruta, {rd:.2f} na divisão e {rk:.2f} em Kadane. Para n², n log₂ n e n, os fatores teóricos são 4, aproximadamente 2,17 e 2. Os fatores medidos não precisam coincidir exatamente com essas referências, devido às constantes e à variabilidade.')
    p(f'Em n = 6.400, a força bruta levou {media("soma_bruta",6400)/media("soma_divisao",6400):.1f} vezes o tempo da divisão. O crescimento observado é compatível com a vantagem assintótica de divisão e conquista; Kadane oferece a alternativa linear para este problema específico. Tempos finitos não constituem prova de complexidade.')
    page()
    h('6. Resultados: par de pontos mais próximos')
    table([['n','Força bruta (ms)','Divisão (ms)']]+[[n,f(media('par_bruto',n)),f(media('par_divisao',n))] for n in [100,200,400,800,1600,3200,6400]], [90,200,200])
    story.append(Image('resultados/grafico_pontos.png',width=490,height=233))
    p('Figura 2. Médias de cinco execuções. A ordenação inicial faz parte dos tempos de divisão e conquista. O limiar utilizado nas medições principais foi 16.')
    p(f'Entre 3.200 e 6.400 pontos, a força bruta cresceu por fator {media("par_bruto",6400)/media("par_bruto",3200):.2f}, enquanto a divisão cresceu por {media("par_divisao",6400)/media("par_divisao",3200):.2f}. As referências teóricas são 4 e aproximadamente 2,17, respectivamente. Em 6.400 pontos, a razão entre os tempos médios foi {media("par_bruto",6400)/media("par_divisao",6400):.1f} a favor da divisão.')
    vencedores=[n for n in [100,200,400,800,1600,3200,6400] if media('par_divisao',n)<media('par_bruto',n)]
    p('A divisão foi mais rápida nos seguintes tamanhos medidos: '+', '.join(map(str,vencedores))+'. Em entradas muito pequenas, a força bruta pode economizar ordenação, recursão e alocação de listas. Este ensaio começa em n = 100 e não determina o ponto exato de cruzamento nem comprova uma vitória da força bruta abaixo desse valor.')
    page()
    h('7. Limiar, limitações e conclusão')
    medias={l:statistics.mean(float(r['tempo_ns'])/1e6 for r in limiares if int(r['limiar'])==l) for l in [2,3,8,16,32,64]}
    table([['Limiar','Média em 3.200 pontos (ms)']]+[[l,f(medias[l])] for l in medias],[120,370])
    p('O limiar 16 foi definido antes dos experimentos principais como compromisso entre reduzir chamadas recursivas e manter pequenos os grupos quadráticos. Para avaliá-lo, foram feitas cinco execuções com cada candidato, reutilizando os mesmos cinco conjuntos de pontos e alternando a ordem dos candidatos. As sementes e os tempos estão em limiares.csv.')
    best=min(medias,key=medias.get)
    p(f'O menor tempo médio desta avaliação foi obtido com limiar {best}. O limiar 16 levou {medias[16]/medias[best]:.2f} vezes esse tempo. Portanto, 16 não é apresentado como o parâmetro ótimo universal. Foi mantido para preservar a decisão inicial e a consistência dos resultados principais. Uma otimização posterior pode adotar o vencedor e repetir todo o experimento; alterar L para outra constante não altera a ordem assintótica.')
    p('A força bruta é simples e útil como referência de correção e caso-base. A divisão reduz fortemente o crescimento do custo para entradas maiores. No subarranjo, Kadane melhora ainda mais a ordem, mostrando que a melhor técnica depende da estrutura do problema.')
    p('<b>Limitações:</b> apenas cinco repetições por tamanho, uma família aleatória principal por problema e ambiente compartilhado. Não há afirmação de significância estatística. A aritmética foi analisada sob custo unitário; inteiros Python têm precisão arbitrária e seu custo cresce com o número de bits. Para pontos, valores extremos podem sofrer limitações da representação de ponto flutuante.')
    h('Reprodutibilidade e referência')
    p('Executar, na pasta do projeto: python testes.py; python experimentos.py; python gerar_relatorio.py. Os arquivos de entrada, código, CSV, gráficos e identificação da máquina devem acompanhar o repositório. O histórico Git deve registrar o desenvolvimento real; este pacote não representa histórico prévio de semanas.')
    p('Fonte dos requisitos: enunciado fornecido na disciplina, “Trabalho Prático: Divisão e Conquista”, entrega indicada em 28/10/2026. As recorrências, demonstrações e análises acima foram desenvolvidas a partir das implementações e das medições deste projeto.')
    def rodape(canvas, doc):
        canvas.setFont('DejaVu',8); canvas.setFillColor(colors.HexColor('#506276'))
        canvas.drawString(48,28,'ANÁLISE DE ALGORITMOS  |  Divisão e Conquista')
        canvas.drawRightString(A4[0]-48,28,str(doc.page))
    SimpleDocTemplate('Relatorio_Divisao_Conquista.pdf',pagesize=A4,rightMargin=48,leftMargin=48,topMargin=42,bottomMargin=46,title='Divisão e Conquista - Análise experimental',author='; '.join(autores)).build(story,onFirstPage=rodape,onLaterPages=rodape)
    print('Relatorio_Divisao_Conquista.pdf gerado.')


if __name__ == '__main__':
    gerar()
