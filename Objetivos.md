# Objetivos

## Servidor Central

**Manter conexão com o servidor distribuído (TCP/IP);**

**Prover uma interface que mantenham atualizadas as seguintes informações:**

- [x] Estado das entradas (Sensores);  
- [x] Estado das Saídas (lâmpadas, aparelhos de ar, etc.);  
- [x] Valor da temperatura e umidade de cada sala a cada 2 segundos;  
- [x] Contador de Ocupação (Número de Pessoas) presentes no prédio como um todo e a ocupação individual de cada sala;  

**Prover mecanismo na interface para:**  

- [x] Acionar manualmente lâmpadas, aparelhos de ar-condicionado e projetores das salas;
- [x] Acionamento do sistema de alarme que, quando estiver ligado, deve tocar um som de alerta (acionar a sirene/buzzer) ao detectar presenças ou abertura de portas/janelas;  
- [x] Acionamento de alarme de incêncio que, ao detectar presença de fumaça a qualquer momento deve soar o alarme;  

**Manter log (em arqvuio CSV) dos comandos acionados pelos usuários e do acionamento dos alarmes com data e hora e cada evento;**

## Servidores Distribuídos

- [x] Manter os valores de temperatura e umidade atualizados a cada 2 segundos (Sendo requisitado pelo servidor central periodicamente ou enviado via mensagem push);
- [x] Acionar Lâmpadas, aparelhos de Ar-Condicionado e projetores (mantendo informação sobre seu estado) conforme comandos do Servidor Central e retornando uma mensagem de confirmação para o mesmo sobre o sucesso ou não do acionamento;
- [x] Manter o estado dos sensores de presença e abertura de portas/janelas informando ao servidor central imediatamente (mensagem push) quando detectar o acionamento de qualquer um deles;
- [x] Manter o estado dos sensores de fumaça informando ao servidor central imediatamente (mensagem push) quando detectar o acionamento de qualquer um deles;
- [x] Efetuar a contagem de pessoas entrando e saindo da sala para controle de ocupação;
- [x] Cada instância dos servidores distribuídos deve ser iniciada conforme o arquivo descrição JSON disponível neste repositório (Somente a porta local de cada servidor deve ser modificada no arquivo para cada aluno conforme a distribuição de portas disponibilizada para a turma).

Os sensores de presença nos corredores terão duas funções:
a. Caso o sistema de alarme esteja ligado, deverão acionar a sirene/buzzer;
b. Caso o sistema de alarme esteja desligado, deverão acender as duas lâmpadas da sala por 15 segundos e depois apagar;
