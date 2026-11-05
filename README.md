# Trabalho prático - Divisão e Conquista

Python 3.10 ou superior. Plataforma sugerida: Google Colab; alternativa: VS Code.

## Começar pelo Colab
1. Acesse https://colab.research.google.com/.
2. Arquivo > Fazer upload de notebook. Selecione Trabalho_Divisao_Conquista.ipynb.
3. Execute as células na ordem. O notebook recria todos os arquivos de código.
4. Edite AUTORES na célula de identificação para incluir o segundo integrante.
5. Execute testes, experimentos e relatório. Os novos tempos serão do ambiente Colab.
6. Baixe o ZIP pela última célula. Guarde o notebook e os resultados: o ambiente é temporário.

O PDF e o CSV fornecidos originalmente foram medidos no ambiente remoto identificado
em resultados/ambiente.json, e não no computador do estudante nem no Colab.
Não misture gráficos de uma execução com CSV ou relatório de outra execução.

## Executar localmente
Abra esta pasta no terminal:

    python -m pip install -r requirements.txt
    python testes.py
    python experimentos.py
    python gerar_relatorio.py

Configure nomes em autores.json antes de gerar o PDF. Os testes usam somente a biblioteca
padrão. Matplotlib cria os gráficos; ReportLab cria o relatório.

## Entrada e saída
Todos os índices começam em 0. Intervalos são inclusivos e não vazios.
Soma: primeira linha n, seguida de n inteiros separados por espaço ou linhas.
Saída: soma inicio fim. Empate: menor início e depois menor fim.

    python main.py soma bruta < exemplos/soma.txt
    python main.py soma divisao < exemplos/soma.txt
    python main.py soma kadane < exemplos/soma.txt

Pontos: n seguido de n pares x y. Saída: distancia id1 id2, IDs na ordem original.
Qualquer par de distância mínima é aceito. Compare distâncias com tolerância numérica,
não por igualdade textual. As coordenadas devem ser finitas, com magnitude moderada.

    python main.py pontos bruta < exemplos/pontos.txt
    python main.py pontos divisao < exemplos/pontos.txt

No PowerShell, use: Get-Content exemplos/soma.txt | python main.py soma divisao

## Arquivos
- algoritmos.py: quatro algoritmos obrigatórios e Kadane complementar.
- main.py: interface de entrada e saída sem menu.
- casos_teste.json: entradas, resultados esperados e pares aceitos.
- testes.py: casos fixos, oráculo exaustivo e testes aleatórios reproduzíveis.
- experimentos.py: cinco repetições por tamanho, CSV, ambiente e gráficos.
- gerar_relatorio.py: gera o relatório a partir dos CSV atuais.
- resultados/: medições brutas, resumo, avaliação do limiar e gráficos.
- Relatorio_Divisao_Conquista.pdf: relatório de sete páginas.

## Decisões a confirmar com o professor
O enunciado menciona um desafio O(n) sem descrevê-lo: foi incluído Kadane como complemento.
“Dígitos” foi interpretado como quantidade de pontos. “Limiar” foi interpretado como
quantidade máxima de pontos tratada por força bruta no caso-base (16).
O formato exato do avaliador automático não foi informado. Adapte main.py se necessário.

## Git e entrega
Crie um repositório no GitHub, extraia os arquivos deste projeto para a pasta dele e
registre commits reais conforme você revisar, executar e alterar o trabalho.
O ZIP não é um repositório remoto e não inclui histórico de semanas anteriores.
Não altere datas nem invente commits. O requisito de histórico deve ser tratado com o professor.
Envie o link do repositório e o PDF pelo canal solicitado na disciplina.
Antes da entrega: inclua o nome da dupla, execute o notebook, confira os resultados e
entenda as implementações para conseguir explicá-las.
