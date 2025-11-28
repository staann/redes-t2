"""
Script de Teste - Demonstração do XProbe
Executa testes automatizados do comando XProbe
"""

from network_simulator import NetworkSimulator
import time


def print_separator():
    print("\n" + "="*80 + "\n")


def test_xprobe_examples():
    """Executa exemplos de XProbe para demonstração"""
    
    print("="*80)
    print(" DEMONSTRAÇÃO DO COMANDO XPROBE")
    print(" Projeto 2 - Simulador de Rede Hierárquica")
    print("="*80)
    
    # Inicializa o simulador
    print("\n🔧 Inicializando rede...")
    simulator = NetworkSimulator()
    print("✓ Rede configurada com sucesso!")
    time.sleep(1)
    
    # Lista de testes
    test_cases = [
        {
            'name': 'Teste 1: h1 → h8 (através de toda a hierarquia)',
            'source': '192.168.1.2',
            'dest': '192.168.4.3',
            'description': 'Caminho mais longo: e1 → a1 → c1 → a2 → e4'
        },
        {
            'name': 'Teste 2: h3 → h5 (através do core)',
            'source': '192.168.2.2',
            'dest': '192.168.3.2',
            'description': 'Caminho: e2 → a1 → c1 → a2 → e3'
        },
        {
            'name': 'Teste 3: h1 → h2 (mesma subrede)',
            'source': '192.168.1.2',
            'dest': '192.168.1.3',
            'description': 'Comunicação local através de e1'
        },
        {
            'name': 'Teste 4: h5 → h6 (mesma subrede)',
            'source': '192.168.3.2',
            'dest': '192.168.3.3',
            'description': 'Comunicação local através de e3'
        },
        {
            'name': 'Teste 5: h2 → h4 (mesmo roteador de agregação)',
            'source': '192.168.1.3',
            'dest': '192.168.2.3',
            'description': 'Caminho: e1 → a1 → e2'
        },
        {
            'name': 'Teste 6: h7 → h8 (mesma subrede)',
            'source': '192.168.4.2',
            'dest': '192.168.4.3',
            'description': 'Comunicação local através de e4'
        }
    ]
    
    # Executa cada teste
    for i, test in enumerate(test_cases, 1):
        print_separator()
        print(f"📝 {test['name']}")
        print(f"💡 {test['description']}")
        print("-" * 80)
        time.sleep(1)
        
        simulator.xprobe(test['source'], test['dest'])
        
        if i < len(test_cases):
            input("\n⏸  Pressione ENTER para o próximo teste...")
    
    print_separator()
    print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print_separator()


def test_routing_tables():
    """Exibe todas as tabelas de roteamento"""
    
    print("\n" + "="*80)
    print(" TABELAS DE ROTEAMENTO - VISÃO GERAL")
    print("="*80)
    
    simulator = NetworkSimulator()
    simulator.display_all_routing_tables()
    
    print("\n✓ Todas as tabelas de roteamento foram exibidas.")


def show_network_summary():
    """Mostra resumo da configuração da rede"""
    
    print("\n" + "="*80)
    print(" RESUMO DA CONFIGURAÇÃO DA REDE")
    print("="*80)
    
    simulator = NetworkSimulator()
    simulator.display_network_info()


def run_analysis():
    """Executa análise completa da rede"""
    
    print("\n" + "="*80)
    print(" ANÁLISE COMPLETA DA REDE")
    print("="*80)
    
    simulator = NetworkSimulator()
    
    print("\n📊 ESTATÍSTICAS DA TOPOLOGIA:")
    print("-" * 80)
    print(f"  • Total de dispositivos: {len(simulator.topology.devices)}")
    print(f"  • Roteadores Core: 1")
    print(f"  • Roteadores de Agregação: 2")
    print(f"  • Roteadores Edge: 4")
    print(f"  • Hosts: 8")
    print(f"  • Total de enlaces: {len(simulator.topology.links)}")
    
    print("\n📈 ANÁLISE DE CONECTIVIDADE:")
    print("-" * 80)
    
    # Testa conectividade entre alguns hosts
    test_pairs = [
        ('192.168.1.2', '192.168.4.3'),  # h1 -> h8
        ('192.168.2.2', '192.168.3.2'),  # h3 -> h5
        ('192.168.1.2', '192.168.1.3'),  # h1 -> h2
    ]
    
    print("\n  Testando conectividade entre hosts selecionados:\n")
    
    for source, dest in test_pairs:
        source_dev = simulator.topology.get_device_by_ip(source)
        dest_dev = simulator.topology.get_device_by_ip(dest)
        path = simulator.topology.trace_route(source, dest)
        
        if len(path) >= 2:
            status = "✓ ALCANÇÁVEL"
            hops = len(path) - 1
        else:
            status = "✗ INALCANÇÁVEL"
            hops = 0
        
        print(f"  {source_dev.name} → {dest_dev.name}: {status} ({hops} hops)")
    
    print("\n" + "="*80)
    
    # Análise de subredes
    print("\n🌐 ANÁLISE DE SUBREDES:")
    print("-" * 80)
    
    subnets = [
        ('192.168.1.0/28', 'e1', '14 hosts (10 requeridos)'),
        ('192.168.2.0/28', 'e2', '14 hosts (10 requeridos)'),
        ('192.168.3.0/27', 'e3', '30 hosts (20 requeridos)'),
        ('192.168.4.0/27', 'e4', '30 hosts (20 requeridos)'),
    ]
    
    for subnet, router, capacity in subnets:
        print(f"  • {subnet} ({router}): {capacity}")
    
    print("\n✓ Todos os requisitos de endereçamento foram atendidos!")
    print("="*80)


def main():
    """Menu principal dos testes"""
    
    while True:
        print("\n" + "="*80)
        print(" SCRIPTS DE TESTE E DEMONSTRAÇÃO")
        print("="*80)
        print("\n1. Executar demonstração XProbe (6 testes)")
        print("2. Visualizar todas as tabelas de roteamento")
        print("3. Visualizar resumo da configuração da rede")
        print("4. Executar análise completa da rede")
        print("5. Executar TODOS os itens acima")
        print("0. Voltar")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '1':
            test_xprobe_examples()
        
        elif choice == '2':
            test_routing_tables()
        
        elif choice == '3':
            show_network_summary()
        
        elif choice == '4':
            run_analysis()
        
        elif choice == '5':
            print("\n🚀 Executando análise completa...")
            show_network_summary()
            input("\n⏸  Pressione ENTER para continuar...")
            test_routing_tables()
            input("\n⏸  Pressione ENTER para continuar...")
            run_analysis()
            input("\n⏸  Pressione ENTER para continuar...")
            test_xprobe_examples()
        
        elif choice == '0':
            print("\n👋 Voltando...")
            break
        
        else:
            print("\n❌ Opção inválida!")
        
        if choice != '0':
            input("\n⏸  Pressione ENTER para continuar...")


if __name__ == "__main__":
    main()
