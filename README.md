<div align="center">
  <h1>MINI-LANG TRANSPILER</h1>
  <p><i>Source-to-Source Compiler Architecture</i></p>
  
  <img src="https://img.shields.io/badge/Language-Mini--Lang-4B0082?style=for-the-badge" alt="Mini-Lang">
  <img src="https://img.shields.io/badge/Target-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Build-Development-000000?style=for-the-badge" alt="Build">
</div>

<br>

## VISÃO GERAL

O objetivo deste projeto é o desenvolvimento prático de um **Transpilador (Compilador Fonte-para-Fonte)** para a linguagem Mini-Lang. O software realiza a leitura de códigos escritos em Mini-Lang e os traduz automaticamente para uma linguagem de alto nível, sendo a linguagem escolhida o **Python**.

---

## ARQUITETURA

O sistema segue o pipeline clássico de compilação, estruturado nas seguintes etapas obrigatórias:

> **1. Análise Léxica (Scanner)**
> Geração de tokens a partir do arquivo de entrada bruto.

> **2. Análise Sintática (Parser)**
> Verificação da gramática EBNF e criação da Árvore Sintática Abstrata (AST).

> **3. Análise Semântica**
> Validação de regras lógicas, como declarações de variáveis, checagem de tipos e escopos.

> **4. Geração de Código**
> Tradução da AST validada para a linguagem destino (Python).

---

## COMO EXECUTAR (TESTES ISOLADOS)

O compilador foi projetado de forma modular. É possível testar o funcionamento de cada fase da compilação de maneira independente.

### 1. Analisador Léxico (Scanner)

Responsável por ler o código-fonte caractere por caractere, ignorar espaços e comentários, e agrupar os caracteres em **Tokens**.

Para testar apenas o Scanner e visualizar a lista de tokens gerada, execute o comando abaixo no terminal:

```bash
python lexer.py <arquivo.mini>
```

**Saída esperada:** Uma lista estruturada contendo o tipo do token, seu valor literal e a linha onde foi encontrado. Exemplo: <INT, 'int'> (linha 1).

### 2. Analisador Sintático (Parser)

Responsável por receber a lista de tokens do Léxico e verificar se eles formam uma estrutura gramatical válida baseada na gramática BNF da Mini-Lang. Utiliza a abordagem Fail-Fast, interrompendo a compilação no primeiro erro estrutural encontrado e exibindo mensagens de erro formatadas.

Para testar apenas o Scanner e visualizar a lista de tokens gerada, execute o comando abaixo no terminal:

```bash
python parser.py <arquivo.mini>
```

**Saída esperada:** Se a sintaxe estiver 100% correta, exibirá a **Árvore Sintática Abstrata (AST)** completa no formato JSON, contendo os nós e seus respectivos filhos em ordem hierárquica. Em caso de falha, exibirá a linha exata e a comparação entre o token esperado e o encontrado.

## CORE TEAM

<table>
  <tr>
    <td align="center"><b>Camila Vanessa de Matos Sousa</b></td>
    <td align="center"><b>Dalton Gomes Lobato</b></td>
    <td align="center"><b>Pedro Rafael Pereira de Oliveira</b></td>
    <td align="center"><b>Vinícius Inácio dos Santos</b></td>
  </tr>
</table>

### 3. Análise Semântica

Responsável por validar a **consistência lógica do programa** após a construção da Árvore Sintática Abstrata (AST). Nesta etapa são verificadas regras que não podem ser detectadas apenas pela gramática, como **declarações de variáveis, compatibilidade de tipos, escopo e chamadas de função**.

O analisador semântico percorre a AST realizando uma **varredura estruturada** e utilizando uma **Tabela de Símbolos** para armazenar informações sobre variáveis e funções declaradas ao longo do código.

Entre as verificações realizadas estão:

- Uso de **variáveis não declaradas**
- **Declaração duplicada** de variáveis no mesmo escopo
- **Compatibilidade de tipos** em atribuições e expressões
- Validação de **operadores matemáticos, relacionais e lógicos**
- Verificação de **existência de funções**
- Checagem de **quantidade e tipo de argumentos** em chamadas de função

O sistema segue a abordagem **Fail-Fast**, interrompendo a compilação assim que um erro semântico é encontrado e exibindo uma mensagem contendo a linha e a descrição do problema.

Para executar a análise semântica de forma isolada, utilize:

```bash
python symtable.py <arquivo.mini>
```

**Saída esperada:** Caso o programa seja semanticamente válido, a AST será considerada correta e poderá seguir para a fase de Geração de Código. Caso contrário, o compilador exibirá uma mensagem de Erro Semântico indicando a linha e a inconsistência detectada.

### 4. Geração de Código

Responsável por realizar a tradução da Árvore Sintática Abstrata (AST) validada para a linguagem de destino, neste caso, o Python.

O gerador percorre a AST e converte cada nó em sua representação equivalente em Python, respeitando a estrutura e a semântica do programa original.

Entre as construções suportadas estão:

- Declaração e atribuição de variáveis
- Expressões aritméticas (+, -, \*, //)
- Expressões relacionais (==, !=, <, >, <=, >=)
- Expressões lógicas (and, or, not)
- Operadores unários (negação lógica e numérica)
- Estruturas de controle (if, else, while)
- Definição de funções (def)
- Retorno de funções (return)
- Chamadas de função
- Comando de saída (print)

Além disso, o gerador é responsável por manter a indentação correta do código Python, garantindo que o código gerado seja válido e executável.

O arquivo **compilador.py** integra todas as etapas do compilador:

- Análise Léxica
- Análise Sintática
- Análise Semântica
- Geração de Código

Para executar o compilador completo, utilize:

```bash
python compilador.py <arquivo.mini>
```

**Saída esperada:** Caso o programa seja válido em todas as etapas anteriores, a AST será considerada correta e seguirá para a geração de código. O sistema exibirá o código Python gerado e realizará sua execução no próprio terminal. Em caso de erro em qualquer etapa, a execução é interrompida e uma mensagem descritiva é apresentada.
