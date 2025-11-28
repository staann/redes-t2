"""
Script de Validação - Verifica se todos os componentes estão funcionando
"""

import sys
import os


def print_header(text):
    print("\n" + "="*80)
    print(f" {text}")
    print("="*80)


def check_python_version():
    """Verifica a versão do Python"""
    print_header("VERIFICANDO VERSÃO DO PYTHON")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✓ Versão do Python adequada (>= 3.7)")
        return True
    else:
        print("✗ Versão do Python inadequada. Necessário Python 3.7+")
        return False


def check_files():
    """Verifica se todos os arquivos necessários existem"""
    print_header("VERIFICANDO ARQUIVOS DO PROJETO")
    
    required_files = [
        'network_simulator.py',
        'test_network.py',
        'generate_diagram.py',
        'README.md',
        'INSTALACAO.md',
        'RESUMO_RELATORIO.md',
        'enderecamento.txt',
        'requirements.txt'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - AUSENTE")
            all_ok = False
    
    return all_ok


def check_imports():
    """Verifica se as importações funcionam"""
    print_header("VERIFICANDO IMPORTAÇÕES")
    
    all_ok = True
    
    # Testa importações básicas
    try:
        import ipaddress
        print("✓ ipaddress")
    except ImportError:
        print("✗ ipaddress - ERRO")
        all_ok = False
    
    try:
        import random
        print("✓ random")
    except ImportError:
        print("✗ random - ERRO")
        all_ok = False
    
    try:
        import time
        print("✓ time")
    except ImportError:
        print("✗ time - ERRO")
        all_ok = False
    
    # Testa matplotlib (opcional)
    try:
        import matplotlib
        print("✓ matplotlib (OPCIONAL - disponível para diagramas gráficos)")
    except ImportError:
        print("⚠ matplotlib não instalado (OPCIONAL - diagramas serão apenas em texto)")
    
    return all_ok


def test_network_simulator():
    """Testa se o simulador pode ser importado"""
    print_header("TESTANDO SIMULADOR DE REDE")
    
    try:
        from network_simulator import NetworkSimulator
        print("✓ NetworkSimulator pode ser importado")
        
        # Tenta criar uma instância
        simulator = NetworkSimulator()
        print("✓ Instância do simulador criada com sucesso")
        
        # Verifica quantidade de dispositivos
        num_devices = len(simulator.topology.devices)
        print(f"✓ Topologia criada com {num_devices} dispositivos")
        
        if num_devices == 15:  # 1 core + 2 agg + 4 edge + 8 hosts
            print("✓ Número correto de dispositivos (15)")
        else:
            print(f"⚠ Número inesperado de dispositivos (esperado: 15, obtido: {num_devices})")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro ao testar simulador: {str(e)}")
        return False


def test_xprobe():
    """Testa a funcionalidade XProbe"""
    print_header("TESTANDO COMANDO XPROBE")
    
    try:
        from network_simulator import NetworkSimulator
        
        simulator = NetworkSimulator()
        
        # Teste 1: h1 para h2 (mesma subrede)
        print("\nTeste 1: h1 → h2 (mesma subrede)")
        source = '192.168.1.2'
        dest = '192.168.1.3'
        
        path = simulator.topology.trace_route(source, dest)
        if len(path) > 0:
            print(f"✓ Rota traçada: {len(path)} dispositivos no caminho")
        else:
            print("✗ Falha ao traçar rota")
            return False
        
        is_active, samples, avg_rtt = simulator.topology.calculate_rtt(source, dest)
        if is_active and len(samples) == 3:
            print(f"✓ RTT calculado: {avg_rtt} ms (3 amostras)")
        else:
            print("✗ Falha ao calcular RTT")
            return False
        
        # Teste 2: h1 para h8 (caminho completo)
        print("\nTeste 2: h1 → h8 (caminho completo)")
        source = '192.168.1.2'
        dest = '192.168.4.3'
        
        path = simulator.topology.trace_route(source, dest)
        if len(path) > 0:
            print(f"✓ Rota traçada: {len(path)} dispositivos no caminho")
        else:
            print("✗ Falha ao traçar rota")
            return False
        
        is_active, samples, avg_rtt = simulator.topology.calculate_rtt(source, dest)
        if is_active and len(samples) == 3:
            print(f"✓ RTT calculado: {avg_rtt} ms (3 amostras)")
        else:
            print("✗ Falha ao calcular RTT")
            return False
        
        print("\n✓ Todos os testes de XProbe passaram!")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao testar XProbe: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_routing_tables():
    """Verifica as tabelas de roteamento"""
    print_header("VERIFICANDO TABELAS DE ROTEAMENTO")
    
    try:
        from network_simulator import NetworkSimulator
        
        simulator = NetworkSimulator()
        
        routers = ['c1', 'a1', 'a2', 'e1', 'e2', 'e3', 'e4']
        
        for router_name in routers:
            device = simulator.topology.devices.get(router_name)
            if device:
                num_routes = len(device.routing_table)
                print(f"✓ {router_name}: {num_routes} rotas configuradas")
            else:
                print(f"✗ {router_name}: não encontrado")
                return False
        
        print("\n✓ Todas as tabelas de roteamento estão configuradas!")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao verificar tabelas: {str(e)}")
        return False


def main():
    """Executa todos os testes de validação"""
    
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "VALIDAÇÃO DO PROJETO" + " "*38 + "║")
    print("║" + " "*15 + "Simulador de Rede Hierárquica" + " "*34 + "║")
    print("╚" + "="*78 + "╝")
    
    results = []
    
    # Executa todos os testes
    results.append(("Versão do Python", check_python_version()))
    results.append(("Arquivos do Projeto", check_files()))
    results.append(("Importações", check_imports()))
    results.append(("Simulador de Rede", test_network_simulator()))
    results.append(("Comando XProbe", test_xprobe()))
    results.append(("Tabelas de Roteamento", test_routing_tables()))
    
    # Resumo
    print_header("RESUMO DA VALIDAÇÃO")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{test_name:.<40} {status}")
    
    print("\n" + "-"*80)
    print(f"Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! O PROJETO ESTÁ PRONTO!")
        print("\n📌 Próximos passos:")
        print("   1. Execute: python network_simulator.py")
        print("   2. Teste o comando XProbe com diferentes hosts")
        print("   3. Prepare o vídeo de demonstração")
        print("   4. Complete o relatório usando RESUMO_RELATORIO.md")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM. Verifique os erros acima.")
        return 1
    
    print("\n" + "="*80)
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Validação interrompida pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
