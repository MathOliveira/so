# Trabalho

## Descrição do Arquivo

O arquivo livros.txt contém os dados de uma aplicação de catálogo de livros. A estrutura do arquivo é a seguinte:

    código: identificador do livro
    titulo: título do livro
    autor: autor do livro
    edição: edição do livro
    ano: ano de publicação do livro

As informações da estrutura de dados são separadas por vírgula (,). O indicador de final de linha utilizado é o "\n".

## Objetivo

O software a ser desenvolvido envolve o problema de programação concorrente de sistemas operacionais usando threads e processos. A linguagem de programação C para o Sistema Operacional Linux deve ser utilizada com a bibliotecas pthreads.h e a linguagem de programação Java ou C# ou Python para desenvolver este trabalho.

Desenhe a solução construindo um grafo de execução de processos para obter pontos de concorrência para o uso de threads e processos separados. Use a exclusão mútua para a solução com pthreads e memória compartilhada com processos.

## Implementar as seguintes operações

- [OK] Criar uma ou mais estruturas de dados para armazenar os dados lidos.
- [OK] Gravar um novo arquivo texto chamado autor.txt com o nome dos autores (sem repetição) e a quantidade de livros - publicados para cada um. Um livro publicado deve levar em consideração somente uma edição publicada.
- [] Gravar um novo arquivo chamado livro.txt com o título do livro (sem repetição) e os anos em que foram publicados (mostrar somente uma vez o mesmo ano).
- [] Gravar um novo arquivo chamado edicao.txt com o ano e o número de edições publicadas naquele ano.
- [] Apresentar um resumo na tela contendo a quantidade total de livros publicados (item 1), a quantidade total de anos que houveram publicações (item 2) e, o ano em que houve mais livros publicados (item 3).

## Entregar

- código fonte para a solução usando Processos ou Threads (Java / C# / Python)
- código fonte para a solução usando Threads (pthreads)
- instruções para a execução do código fonte
- grafo de execução dos processos

---

# Minha Implementação

Trabalho implementado em Python, por isso o único requisito necessário para execução do trabalho é o Python 3.

Instrução para execução do trabalho:

```sh
python3 main.py data/books.txt 5
```

Onde:

- [main.py] - Arquivo main da minha implementação
- [data/books.txt] - Arquivo de entrada com os dados estruturados do trabalho
- [5] - Número de threads para execução do trabalho
