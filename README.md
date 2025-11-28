# Projeto 2 - Simulador de Rede Hierárquica

## Descrição do Projeto

Este projeto implementa uma topologia de rede hierárquica em árvore, comumente utilizada em data centers, com três camadas: Core, Agregação e Edge.

## Estrutura da Rede

### Topologia
```
                        c1 (Core)
                       /         \
                      /           \
                 a1 (Agg)      a2 (Agg)
                /    \          /    \
               /      \        /      \
           e1(Edge) e2(Edge) e3(Edge) e4(Edge)
           /  \      /  \      /  \      /  \
          h1  h2    h3  h4    h5  h6    h7  h8
```

### Dispositivos

#### Camada Core
- **c1**: Roteador Core
  - eth0: 192.168.21.1/30 (link com a1)
  - eth1: 192.168.22.1/30 (link com a2)

#### Camada Aggregation
- **a1**: Roteador de Agregação 1
  - eth0: 192.168.11.1/30 (link com e1)
  - eth1: 192.168.12.1/30 (link com e2)
  - eth2: 192.168.21.2/30 (link com c1)

- **a2**: Roteador de Agregação 2
  - eth0: 192.168.13.1/30 (link com e3)
  - eth1: 192.168.14.1/30 (link com e4)
  - eth2: 192.168.22.2/30 (link com c1)

#### Camada Edge
- **e1**: Roteador Edge 1
  - eth0: 192.168.1.1/28 (rede de hosts)
  - eth1: 192.168.11.2/30 (link com a1)

- **e2**: Roteador Edge 2
  - eth0: 192.168.2.1/28 (rede de hosts)
  - eth1: 192.168.12.2/30 (link com a1)

- **e3**: Roteador Edge 3
  - eth0: 192.168.3.1/27 (rede de hosts)
  - eth1: 192.168.13.2/30 (link com a2)

- **e4**: Roteador Edge 4
  - eth0: 192.168.4.1/27 (rede de hosts)
  - eth1: 192.168.14.2/30 (link com a2)

#### Camada Host
- **h1**: 192.168.1.2/28 (gateway: 192.168.1.1)
- **h2**: 192.168.1.3/28 (gateway: 192.168.1.1)
- **h3**: 192.168.2.2/28 (gateway: 192.168.2.1)
- **h4**: 192.168.2.3/28 (gateway: 192.168.2.1)
- **h5**: 192.168.3.2/27 (gateway: 192.168.3.1)
- **h6**: 192.168.3.3/27 (gateway: 192.168.3.1)
- **h7**: 192.168.4.2/27 (gateway: 192.168.4.1)
- **h8**: 192.168.4.3/27 (gateway: 192.168.4.1)

## Planejamento de Endereçamento IP

### Requisitos Atendidos
- **e1 e e2**: Suporte para 10 hosts → /28 (14 hosts utilizáveis)
- **e3 e e4**: Suporte para 20 hosts → /27 (30 hosts utilizáveis)
- **a1 e a2**: Suporte para 4 subredes → Configurado com 3 interfaces + roteamento

### Subredes Definidas

| Subrede | Rede | Máscara | Range | Uso |
|---------|------|---------|-------|-----|
| e1 | 192.168.1.0/28 | /28 | 192.168.1.1-14 | Hosts h1, h2 |
| e2 | 192.168.2.0/28 | /28 | 192.168.2.1-14 | Hosts h3, h4 |
| e3 | 192.168.3.0/27 | /27 | 192.168.3.1-30 | Hosts h5, h6 |
| e4 | 192.168.4.0/27 | /27 | 192.168.4.1-30 | Hosts h7, h8 |
| Link a1-e1 | 192.168.11.0/30 | /30 | 192.168.11.1-2 | Ponto-a-ponto |
| Link a1-e2 | 192.168.12.0/30 | /30 | 192.168.12.1-2 | Ponto-a-ponto |
| Link a2-e3 | 192.168.13.0/30 | /30 | 192.168.13.1-2 | Ponto-a-ponto |
| Link a2-e4 | 192.168.14.0/30 | /30 | 192.168.14.1-2 | Ponto-a-ponto |
| Link c1-a1 | 192.168.21.0/30 | /30 | 192.168.21.1-2 | Ponto-a-ponto |
| Link c1-a2 | 192.168.22.0/30 | /30 | 192.168.22.1-2 | Ponto-a-ponto |

## Tipos de Enlaces

| Conexão | Tipo de Enlace | Capacidade | Justificativa |
|---------|----------------|------------|---------------|
| Core ↔ Aggregation | Fibra Óptica | 10 Gbps | Alta capacidade para agregação de tráfego de múltiplas subredes |
| Aggregation ↔ Edge | Par Trançado Cat6 | 1 Gbps | Boa relação custo-benefício para tráfego agregado |
| Edge ↔ Hosts | Par Trançado Cat5e | 100 Mbps | Suficiente para conexões de servidores individuais |

## Tabelas de Roteamento

### Roteador c1 (Core)
| Destino | Máscara | Next Hop | Interface |
|---------|---------|----------|-----------|
| 192.168.1.0 | /28 | 192.168.21.2 | eth0 |
| 192.168.2.0 | /28 | 192.168.21.2 | eth0 |
| 192.168.11.0 | /30 | 192.168.21.2 | eth0 |
| 192.168.12.0 | /30 | 192.168.21.2 | eth0 |
| 192.168.3.0 | /27 | 192.168.22.2 | eth1 |
| 192.168.4.0 | /27 | 192.168.22.2 | eth1 |
| 192.168.13.0 | /30 | 192.168.22.2 | eth1 |
| 192.168.14.0 | /30 | 192.168.22.2 | eth1 |

### Roteador a1 (Aggregation)
| Destino | Máscara | Next Hop | Interface |
|---------|---------|----------|-----------|
| 192.168.1.0 | /28 | 192.168.11.2 | eth0 |
| 192.168.2.0 | /28 | 192.168.12.2 | eth1 |
| 192.168.3.0 | /27 | 192.168.21.1 | eth2 |
| 192.168.4.0 | /27 | 192.168.21.1 | eth2 |
| 192.168.13.0 | /30 | 192.168.21.1 | eth2 |
| 192.168.14.0 | /30 | 192.168.21.1 | eth2 |
| 192.168.22.0 | /30 | 192.168.21.1 | eth2 |

### Roteador a2 (Aggregation)
| Destino | Máscara | Next Hop | Interface |
|---------|---------|----------|-----------|
| 192.168.3.0 | /27 | 192.168.13.2 | eth0 |
| 192.168.4.0 | /27 | 192.168.14.2 | eth1 |
| 192.168.1.0 | /28 | 192.168.22.1 | eth2 |
| 192.168.2.0 | /28 | 192.168.22.1 | eth2 |
| 192.168.11.0 | /30 | 192.168.22.1 | eth2 |
| 192.168.12.0 | /30 | 192.168.22.1 | eth2 |
| 192.168.21.0 | /30 | 192.168.22.1 | eth2 |

### Roteadores Edge (e1, e2, e3, e4)
Todos os roteadores Edge usam rota padrão (0.0.0.0/0) apontando para seus respectivos roteadores de agregação.

## Como Executar

### Requisitos
- Python 3.7 ou superior

### Execução
```bash
python network_simulator.py
```

### Funcionalidades

1. **Visualizar configuração da rede**
   - Exibe todos os dispositivos organizados por camada
   - Mostra interfaces e endereços IP
   - Lista todos os enlaces com tipo e capacidade

2. **Visualizar tabela de roteamento**
   - Exibe a tabela de roteamento de um dispositivo específico
   - Mostra redes diretamente conectadas e rotas estáticas

3. **Visualizar todas as tabelas de roteamento**
   - Mostra as tabelas de todos os roteadores da rede

4. **Executar XProbe**
   - Verifica conectividade entre dois IPs
   - Traça a rota completa entre origem e destino
   - Calcula RTT médio com 3 amostras
   - Exibe estatísticas detalhadas

## Comando XProbe

O comando XProbe implementa a funcionalidade especificada no Quadro 1 do projeto:

1. Verifica se o destino está ativo
2. Traça a rota entre origem e destino
3. Realiza 3 medições de RTT
4. Calcula e exibe:
   - RTT mínimo, máximo e médio
   - Número de hops
   - Perda de pacotes
   - Caminho completo

### Exemplo de Uso

```
Origem: 192.168.1.2 (h1)
Destino: 192.168.4.3 (h8)

Rota:
1. h1 (192.168.1.2)
2. e1 (192.168.1.1)
3. a1 (192.168.11.1)
4. c1 (192.168.21.1)
5. a2 (192.168.22.2)
6. e4 (192.168.14.1)
7. h8 (192.168.4.3)

RTT Médio: 8.45 ms
```

## Estrutura do Código

- **NetworkInterface**: Representa uma interface de rede com IP e máscara
- **NetworkDevice**: Classe base para dispositivos (hosts e roteadores)
- **Host**: Representa um host com IP e gateway
- **Router**: Representa um roteador com múltiplas interfaces
- **NetworkTopology**: Gerencia toda a topologia da rede
- **NetworkSimulator**: Interface de usuário e controle da simulação

## Análise de Resultados

A implementação demonstra:

1. **Roteamento correto**: Pacotes seguem o caminho esperado na hierarquia
2. **Tabelas otimizadas**: Rotas estáticas minimizam o número de entradas
3. **Escalabilidade**: Estrutura permite expansão fácil com mais dispositivos
4. **RTT realista**: Varia conforme número de hops e simula jitter de rede

## Autor

Projeto desenvolvido para a disciplina de Redes de Computadores - 2025.2
