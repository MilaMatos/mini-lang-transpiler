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

## CORE TEAM

<table>
  <tr>
    <td align="center"><b>Camila Vanessa de Matos Sousa</b></td>
    <td align="center"><b>Dalton Gomes Lobato</b></td>
    <td align="center"><b>Pedro Rafael Pereira de Oliveira</b></td>
    <td align="center"><b>Vinícius Inácio dos Santos</b></td>
  </tr>
</table>