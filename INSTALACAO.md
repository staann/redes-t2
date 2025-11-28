# GUIA DE INSTALAÇÃO E EXECUÇÃO

## Requisitos do Sistema

- Python 3.7 ou superior
- Sistema Operacional: Windows, Linux ou macOS

## Instalação

### 1. Verificar Instalação do Python

Abra o terminal/PowerShell e execute:
```bash
python --version
```

Deve mostrar Python 3.7 ou superior.

### 2. (Opcional) Instalar Dependências para Diagramas Gráficos

Se desejar gerar diagramas gráficos com matplotlib:

```bash
pip install matplotlib
```

**Nota:** O simulador funciona perfeitamente sem matplotlib. Os diagramas serão gerados em formato texto ASCII.

## Como Executar

### Opção 1: Simulador Interativo Principal

Execute o simulador principal com menu interativo:

```bash
python network_simulator.py
```

**Funcionalidades disponíveis:**
- Visualizar configuração completa da rede
- Ver tabelas de roteamento individuais ou todas
- Executar comando XProbe entre quaisquer dois IPs
- Exemplos pré-configurados de XProbe

### Opção 2: Script de Testes e Demonstração

Execute testes automatizados e demonstrações:

```bash
python test_network.py
```

**Inclui:**
- 6 testes de XProbe pré-configurados
- Análise completa da topologia
- Visualização de todas as tabelas de roteamento
- Estatísticas da rede

### Opção 3: Gerar Diagramas da Rede

Para gerar diagramas visuais da topologia:

```bash
python generate_diagram.py
```

**Gera:**
- `diagrama_rede.txt` - Diagrama em ASCII (sempre)
- `diagrama_rede.png` - Diagrama gráfico (se matplotlib instalado)

## Estrutura dos Arquivos

```
redest2/
│
├── network_simulator.py      # Simulador principal (EXECUTAR ESTE)
├── test_network.py            # Scripts de teste e demonstração
├── generate_diagram.py        # Gerador de diagramas
│
├── README.md                  # Documentação completa do projeto
├── INSTALACAO.md              # Este arquivo
├── requirements.txt           # Dependências Python
├── enderecamento.txt          # Planejamento de IPs
│
├── diagrama_rede.txt          # Diagrama em texto (gerado)
└── diagrama_rede.png          # Diagrama gráfico (gerado, se matplotlib)
```

## Exemplos de Uso

### Exemplo 1: Executar XProbe entre h1 e h8

1. Execute: `python network_simulator.py`
2. Escolha opção `5` (Exemplo: XProbe de h1 para h8)
3. Observe a rota traçada e estatísticas de RTT

### Exemplo 2: Visualizar Tabela de Roteamento do Core

1. Execute: `python network_simulator.py`
2. Escolha opção `2` (Visualizar tabela específica)
3. Digite: `c1`
4. Veja todas as rotas configuradas no roteador core

### Exemplo 3: Teste Personalizado de XProbe

1. Execute: `python network_simulator.py`
2. Escolha opção `4` (Executar XProbe)
3. Digite IP origem: `192.168.1.2` (h1)
4. Digite IP destino: `192.168.3.2` (h5)
5. Veja a rota e estatísticas

## Endereços IP Disponíveis

### Hosts
- h1: 192.168.1.2
- h2: 192.168.1.3
- h3: 192.168.2.2
- h4: 192.168.2.3
- h5: 192.168.3.2
- h6: 192.168.3.3
- h7: 192.168.4.2
- h8: 192.168.4.3

### Roteadores Edge (interfaces voltadas para hosts)
- e1: 192.168.1.1
- e2: 192.168.2.1
- e3: 192.168.3.1
- e4: 192.168.4.1

## Solução de Problemas

### Problema: "python não é reconhecido"

**Solução:** Instale Python 3.7+ de python.org ou use `python3` ao invés de `python`.

### Problema: "ModuleNotFoundError: No module named 'matplotlib'"

**Solução:** Isso é normal se não instalou matplotlib. O programa funciona sem ele, apenas não gerará diagramas gráficos PNG. Para instalar:
```bash
pip install matplotlib
```

### Problema: Caracteres não aparecem corretamente no terminal

**Solução (Windows):** Execute no PowerShell:
```powershell
chcp 65001
```
Isso ativa UTF-8 no terminal.

### Problema: ImportError relacionado a ipaddress

**Solução:** O módulo `ipaddress` faz parte da biblioteca padrão do Python 3.3+. Atualize seu Python.

## Testes Rápidos

Para verificar que tudo está funcionando:

```bash
# Teste 1: Executar simulador
python network_simulator.py

# Teste 2: Gerar diagrama
python generate_diagram.py

# Teste 3: Executar testes automatizados
python test_network.py
```

## Informações Adicionais

Para documentação completa sobre a topologia, endereçamento e tabelas de roteamento, consulte `README.md`.

## Suporte

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Redes de Computadores.

**Componentes do Projeto:**
- Simulador de rede hierárquica
- Implementação de roteamento estático
- Comando XProbe com cálculo de RTT
- Visualização de topologia e rotas
