# DeltaCoin

- Automação para extrair a cotação atual do Dollar e Euro

## Fluxo da automação

- A automação retira os dados do site - https://www.bcb.gov.br através de dois métodos, RPA e API.
  - Prefiro usar sempre API pois é o método feito para transferência /transmissão de informações, ou seja, para captura de dados também servirá melhor que um site dês de que não quebre nenhuma regra de uso ou negócio
- No arquivo main é possível chamar ambos a partir da classe App.
- O método RPA chama a propriedade RPA da classe DeltaCoin, onde todo o fluxo de; acessar o site, localizar as tabelas de cotação, localizar os itens dentro dessas tabelas e retornar as informações coletadas em um dicionário
- O dicionário retornado pela propriedade RPA é inserida no método _to_pdf_, que salva diretamente no _path_ definido ao instanciar o _DeltaCoin_
- E finalmente, no método _mail_ de _DeltaCoin_ envia o pdf por email

---

- Toda a aplicação registra log do que está sendo feito, o arquivo do log vai para o diretório _docs_generated_, na raíz do projeto

## Melhorias que gostaria de ter colocado

- Banco de dados, torna possível integração com programas como PowerBi, onde essa informação teria mais usos além de ir para um arquivo. _Desconsiderando a natureza do projeto de ser apenas um teste técnico_

## Instalação

- Após baixar e extrair a automação, será necessário criar um venv para instalar as dependências do projeto

  - Criar
    `python -m venv venv`

  - Ativar

    - Windows
      `source venv/scripts/activate`
    - Linux
      `source venv/bin/activate`

  - Instalar dependências
    `pip install -r requirements.txt`

## Inicialização

- Ativar o venv
- Rodar a main com algum dos modos ativados, os dois também funcionam normalmente caso sejam usados juntos
