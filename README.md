## Sobre o Projeto

Mini Dungeon Game é um jogo simples de aventura e exploração em um labirinto gerado aleatoriamente, criado com Python utilizando a biblioteca Pygame Zero. O jogador controla um herói que precisa coletar todos os tesouros espalhados pelo mapa, evitando inimigos e obstáculos para vencer o jogo.

## Como Jogar

* Use as **setas do teclado** (← ↑ → ↓) para mover o herói pelo labirinto.
* O objetivo é coletar todos os tesouros (representados por itens amarelos animados) no mapa.
* Evite os inimigos, que patrulham rotas fixas — se um inimigo encostar no herói, o jogo termina.
* Existem paredes e barreiras que limitam os caminhos, então planeje seus movimentos para não ficar preso.
* Após coletar todos os tesouros, você vence o jogo.
* No menu, você pode ativar ou desativar o som e iniciar ou sair do jogo.

## Controles

* **Setas do teclado**: mover o herói para cima, baixo, esquerda e direita.
* **Espaço**: no estado de "Game Over" ou "Vitória", pressione para voltar ao menu principal.

## Estado do Jogo

* **Menu**: tela inicial com opções para iniciar o jogo, ativar/desativar som, ou sair.
* **Jogando**: controle o herói, coleta tesouros, evita inimigos.
* **Game Over**: exibido quando o herói é capturado por um inimigo.
* **Vitória**: exibido quando todos os tesouros são coletados.

## Requisitos

* Python 3.x
* Biblioteca Pygame Zero instalada (`pip install pgzero`)

## Como Executar

1. Salve o código do jogo em um arquivo `main.py`.
2. Execute o jogo com o comando:

   ```bash
   pgzrun game.py
   ```
3. Use as setas do teclado para jogar.