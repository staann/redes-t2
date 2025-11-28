"""
Simulador de Rede Hierárquica - Projeto 2
Topologia em Árvore com Core, Agregação e Edge
"""

import time
import random
from typing import Dict, List, Tuple, Optional
import ipaddress


class NetworkInterface:
    """Representa uma interface de rede com endereço IP"""
    
    def __init__(self, ip: str, mask: str):
        self.ip = ip
        self.mask = mask
        self.network = ipaddress.ip_network(f"{ip}/{mask}", strict=False)
    
    def __str__(self):
        return f"{self.ip}/{self.mask}"


class NetworkDevice:
    """Classe base para dispositivos de rede"""
    
    def __init__(self, name: str, device_type: str):
        self.name = name
        self.device_type = device_type
        self.interfaces: Dict[str, NetworkInterface] = {}
        self.routing_table: List[Dict] = []
        self.connections: Dict[str, 'NetworkDevice'] = {}
    
    def add_interface(self, interface_name: str, ip: str, mask: str):
        """Adiciona uma interface ao dispositivo"""
        self.interfaces[interface_name] = NetworkInterface(ip, mask)
    
    def add_connection(self, interface_name: str, device: 'NetworkDevice'):
        """Adiciona uma conexão com outro dispositivo"""
        self.connections[interface_name] = device
    
    def add_route(self, destination: str, mask: str, next_hop: str, interface: str):
        """Adiciona uma rota à tabela de roteamento"""
        self.routing_table.append({
            'destination': destination,
            'mask': mask,
            'next_hop': next_hop,
            'interface': interface
        })
    
    def get_route(self, destination_ip: str) -> Optional[Dict]:
        """Encontra a rota para um IP de destino"""
        dest_ip = ipaddress.ip_address(destination_ip)
        
        # Verifica se é uma rede diretamente conectada
        for iface_name, iface in self.interfaces.items():
            if dest_ip in iface.network:
                return {
                    'destination': str(iface.network.network_address),
                    'mask': str(iface.network.prefixlen),
                    'next_hop': 'directly connected',
                    'interface': iface_name
                }
        
        # Busca na tabela de roteamento
        best_match = None
        best_prefix_len = -1
        
        for route in self.routing_table:
            network = ipaddress.ip_network(f"{route['destination']}/{route['mask']}")
            if dest_ip in network:
                prefix_len = network.prefixlen
                if prefix_len > best_prefix_len:
                    best_match = route
                    best_prefix_len = prefix_len
        
        return best_match
    
    def __str__(self):
        return f"{self.device_type} {self.name}"


class Host(NetworkDevice):
    """Representa um host na rede"""
    
    def __init__(self, name: str, ip: str, mask: str, gateway: str):
        super().__init__(name, "Host")
        self.add_interface("eth0", ip, mask)
        self.gateway = gateway
        self.active = True
    
    def get_ip(self):
        return self.interfaces["eth0"].ip


class Router(NetworkDevice):
    """Representa um roteador na rede"""
    
    def __init__(self, name: str, router_type: str):
        super().__init__(name, f"Router-{router_type}")
        self.router_type = router_type


class NetworkTopology:
    """Gerencia a topologia completa da rede"""
    
    def __init__(self):
        self.devices: Dict[str, NetworkDevice] = {}
        self.links: List[Tuple] = []
        self._build_network()
    
    def _build_network(self):
        """Constrói a topologia da rede conforme especificação"""
        
        # ===== HOSTS =====
        self.devices['h1'] = Host('h1', '192.168.1.2', '28', '192.168.1.1')
        self.devices['h2'] = Host('h2', '192.168.1.3', '28', '192.168.1.1')
        self.devices['h3'] = Host('h3', '192.168.2.2', '28', '192.168.2.1')
        self.devices['h4'] = Host('h4', '192.168.2.3', '28', '192.168.2.1')
        self.devices['h5'] = Host('h5', '192.168.3.2', '27', '192.168.3.1')
        self.devices['h6'] = Host('h6', '192.168.3.3', '27', '192.168.3.1')
        self.devices['h7'] = Host('h7', '192.168.4.2', '27', '192.168.4.1')
        self.devices['h8'] = Host('h8', '192.168.4.3', '27', '192.168.4.1')
        
        # ===== EDGE ROUTERS =====
        self.devices['e1'] = Router('e1', 'Edge')
        self.devices['e1'].add_interface('eth0', '192.168.1.1', '28')  # Para hosts h1, h2
        self.devices['e1'].add_interface('eth1', '192.168.11.2', '30')  # Link com a1
        
        self.devices['e2'] = Router('e2', 'Edge')
        self.devices['e2'].add_interface('eth0', '192.168.2.1', '28')  # Para hosts h3, h4
        self.devices['e2'].add_interface('eth1', '192.168.12.2', '30')  # Link com a1
        
        self.devices['e3'] = Router('e3', 'Edge')
        self.devices['e3'].add_interface('eth0', '192.168.3.1', '27')  # Para hosts h5, h6
        self.devices['e3'].add_interface('eth1', '192.168.13.2', '30')  # Link com a2
        
        self.devices['e4'] = Router('e4', 'Edge')
        self.devices['e4'].add_interface('eth0', '192.168.4.1', '27')  # Para hosts h7, h8
        self.devices['e4'].add_interface('eth1', '192.168.14.2', '30')  # Link com a2
        
        # ===== AGGREGATION ROUTERS =====
        self.devices['a1'] = Router('a1', 'Aggregation')
        self.devices['a1'].add_interface('eth0', '192.168.11.1', '30')  # Link com e1
        self.devices['a1'].add_interface('eth1', '192.168.12.1', '30')  # Link com e2
        self.devices['a1'].add_interface('eth2', '192.168.21.2', '30')  # Link com c1
        
        self.devices['a2'] = Router('a2', 'Aggregation')
        self.devices['a2'].add_interface('eth0', '192.168.13.1', '30')  # Link com e3
        self.devices['a2'].add_interface('eth1', '192.168.14.1', '30')  # Link com e4
        self.devices['a2'].add_interface('eth2', '192.168.22.2', '30')  # Link com c1
        
        # ===== CORE ROUTER =====
        self.devices['c1'] = Router('c1', 'Core')
        self.devices['c1'].add_interface('eth0', '192.168.21.1', '30')  # Link com a1
        self.devices['c1'].add_interface('eth1', '192.168.22.1', '30')  # Link com a2
        
        # ===== CONFIGURAR CONEXÕES =====
        self._setup_connections()
        
        # ===== CONFIGURAR TABELAS DE ROTEAMENTO =====
        self._setup_routing_tables()
        
        # ===== CONFIGURAR LINKS =====
        self._setup_links()
    
    def _setup_connections(self):
        """Configura as conexões entre dispositivos"""
        # Core <-> Aggregation
        self.devices['c1'].add_connection('eth0', self.devices['a1'])
        self.devices['c1'].add_connection('eth1', self.devices['a2'])
        
        # Aggregation <-> Edge
        self.devices['a1'].add_connection('eth0', self.devices['e1'])
        self.devices['a1'].add_connection('eth1', self.devices['e2'])
        self.devices['a1'].add_connection('eth2', self.devices['c1'])
        
        self.devices['a2'].add_connection('eth0', self.devices['e3'])
        self.devices['a2'].add_connection('eth1', self.devices['e4'])
        self.devices['a2'].add_connection('eth2', self.devices['c1'])
        
        # Edge <-> Aggregation e Hosts
        self.devices['e1'].add_connection('eth1', self.devices['a1'])
        self.devices['e2'].add_connection('eth1', self.devices['a1'])
        self.devices['e3'].add_connection('eth1', self.devices['a2'])
        self.devices['e4'].add_connection('eth1', self.devices['a2'])
    
    def _setup_routing_tables(self):
        """Configura as tabelas de roteamento estáticas"""
        
        # ===== ROUTER e1 =====
        # Rota padrão via a1
        self.devices['e1'].add_route('0.0.0.0', '0', '192.168.11.1', 'eth1')
        
        # ===== ROUTER e2 =====
        self.devices['e2'].add_route('0.0.0.0', '0', '192.168.12.1', 'eth1')
        
        # ===== ROUTER e3 =====
        self.devices['e3'].add_route('0.0.0.0', '0', '192.168.13.1', 'eth1')
        
        # ===== ROUTER e4 =====
        self.devices['e4'].add_route('0.0.0.0', '0', '192.168.14.1', 'eth1')
        
        # ===== ROUTER a1 =====
        # Redes locais via edge routers
        self.devices['a1'].add_route('192.168.1.0', '28', '192.168.11.2', 'eth0')
        self.devices['a1'].add_route('192.168.2.0', '28', '192.168.12.2', 'eth1')
        # Redes do outro lado via core
        self.devices['a1'].add_route('192.168.3.0', '27', '192.168.21.1', 'eth2')
        self.devices['a1'].add_route('192.168.4.0', '27', '192.168.21.1', 'eth2')
        # Redes do a2
        self.devices['a1'].add_route('192.168.13.0', '30', '192.168.21.1', 'eth2')
        self.devices['a1'].add_route('192.168.14.0', '30', '192.168.21.1', 'eth2')
        self.devices['a1'].add_route('192.168.22.0', '30', '192.168.21.1', 'eth2')
        
        # ===== ROUTER a2 =====
        # Redes locais via edge routers
        self.devices['a2'].add_route('192.168.3.0', '27', '192.168.13.2', 'eth0')
        self.devices['a2'].add_route('192.168.4.0', '27', '192.168.14.2', 'eth1')
        # Redes do outro lado via core
        self.devices['a2'].add_route('192.168.1.0', '28', '192.168.22.1', 'eth2')
        self.devices['a2'].add_route('192.168.2.0', '28', '192.168.22.1', 'eth2')
        # Redes do a1
        self.devices['a2'].add_route('192.168.11.0', '30', '192.168.22.1', 'eth2')
        self.devices['a2'].add_route('192.168.12.0', '30', '192.168.22.1', 'eth2')
        self.devices['a2'].add_route('192.168.21.0', '30', '192.168.22.1', 'eth2')
        
        # ===== ROUTER c1 (CORE) =====
        # Redes via a1
        self.devices['c1'].add_route('192.168.1.0', '28', '192.168.21.2', 'eth0')
        self.devices['c1'].add_route('192.168.2.0', '28', '192.168.21.2', 'eth0')
        self.devices['c1'].add_route('192.168.11.0', '30', '192.168.21.2', 'eth0')
        self.devices['c1'].add_route('192.168.12.0', '30', '192.168.21.2', 'eth0')
        # Redes via a2
        self.devices['c1'].add_route('192.168.3.0', '27', '192.168.22.2', 'eth1')
        self.devices['c1'].add_route('192.168.4.0', '27', '192.168.22.2', 'eth1')
        self.devices['c1'].add_route('192.168.13.0', '30', '192.168.22.2', 'eth1')
        self.devices['c1'].add_route('192.168.14.0', '30', '192.168.22.2', 'eth1')
    
    def _setup_links(self):
        """Define os links da topologia com tipos de enlace"""
        self.links = [
            # Core <-> Aggregation (Fibra Óptica - alta capacidade)
            ('c1', 'a1', 'Fibra Óptica', '10 Gbps'),
            ('c1', 'a2', 'Fibra Óptica', '10 Gbps'),
            # Aggregation <-> Edge (Fibra Óptica ou Par Trançado Cat6)
            ('a1', 'e1', 'Par Trançado Cat6', '1 Gbps'),
            ('a1', 'e2', 'Par Trançado Cat6', '1 Gbps'),
            ('a2', 'e3', 'Par Trançado Cat6', '1 Gbps'),
            ('a2', 'e4', 'Par Trançado Cat6', '1 Gbps'),
            # Edge <-> Hosts (Par Trançado Cat5e)
            ('e1', 'h1', 'Par Trançado Cat5e', '100 Mbps'),
            ('e1', 'h2', 'Par Trançado Cat5e', '100 Mbps'),
            ('e2', 'h3', 'Par Trançado Cat5e', '100 Mbps'),
            ('e2', 'h4', 'Par Trançado Cat5e', '100 Mbps'),
            ('e3', 'h5', 'Par Trançado Cat5e', '100 Mbps'),
            ('e3', 'h6', 'Par Trançado Cat5e', '100 Mbps'),
            ('e4', 'h7', 'Par Trançado Cat5e', '100 Mbps'),
            ('e4', 'h8', 'Par Trançado Cat5e', '100 Mbps'),
        ]
    
    def get_device_by_ip(self, ip: str) -> Optional[NetworkDevice]:
        """Encontra um dispositivo pelo seu IP"""
        for device in self.devices.values():
            if isinstance(device, Host):
                if device.get_ip() == ip:
                    return device
            else:
                for iface in device.interfaces.values():
                    if iface.ip == ip:
                        return device
        return None
    
    def trace_route(self, source_ip: str, dest_ip: str) -> List[str]:
        """Traça a rota entre origem e destino"""
        path = []
        current_ip = source_ip
        visited = set()
        
        # Encontra o dispositivo de origem
        source_device = self.get_device_by_ip(source_ip)
        if not source_device:
            return []
        
        path.append(f"{source_device.name} ({source_ip})")
        
        # Se for um host, começa pelo gateway
        if isinstance(source_device, Host):
            current_ip = source_device.gateway
            gateway_device = self.get_device_by_ip(current_ip)
            if gateway_device:
                path.append(f"{gateway_device.name} ({current_ip})")
        
        # Traça a rota através dos roteadores
        while current_ip != dest_ip:
            if current_ip in visited:
                break
            visited.add(current_ip)
            
            current_device = self.get_device_by_ip(current_ip)
            if not current_device or isinstance(current_device, Host):
                break
            
            # Encontra a próxima hop
            route = current_device.get_route(dest_ip)
            if not route:
                break
            
            if route['next_hop'] == 'directly connected':
                # Chegou na rede de destino
                dest_device = self.get_device_by_ip(dest_ip)
                if dest_device:
                    path.append(f"{dest_device.name} ({dest_ip})")
                break
            else:
                current_ip = route['next_hop']
                next_device = self.get_device_by_ip(current_ip)
                if next_device:
                    path.append(f"{next_device.name} ({current_ip})")
        
        return path
    
    def calculate_rtt(self, source_ip: str, dest_ip: str, num_samples: int = 3) -> Tuple[bool, List[float], float]:
        """Calcula o RTT entre origem e destino"""
        source_device = self.get_device_by_ip(source_ip)
        dest_device = self.get_device_by_ip(dest_ip)
        
        if not source_device or not dest_device:
            return False, [], 0.0
        
        if isinstance(dest_device, Host) and not dest_device.active:
            return False, [], 0.0
        
        # Traça a rota para calcular o número de hops
        path = self.trace_route(source_ip, dest_ip)
        if len(path) < 2:
            return False, [], 0.0
        
        num_hops = len(path) - 1
        
        # Simula RTT com variação baseada no número de hops
        samples = []
        base_rtt = num_hops * random.uniform(0.5, 2.0)  # Base RTT por hop
        
        for _ in range(num_samples):
            # Adiciona variação (jitter)
            variation = random.uniform(-0.3, 0.3)
            sample_rtt = base_rtt + variation
            samples.append(round(sample_rtt, 2))
            time.sleep(0.1)  # Simula delay entre amostras
        
        avg_rtt = round(sum(samples) / len(samples), 2)
        
        return True, samples, avg_rtt


class NetworkSimulator:
    """Simulador principal com interface de usuário"""
    
    def __init__(self):
        self.topology = NetworkTopology()
    
    def display_network_info(self):
        """Exibe informações sobre a rede"""
        print("\n" + "="*80)
        print(" CONFIGURAÇÃO DA REDE - TOPOLOGIA HIERÁRQUICA")
        print("="*80)
        
        print("\n📊 DISPOSITIVOS DA REDE:")
        print("-" * 80)
        
        # Organiza por camadas
        layers = {
            'Core': [],
            'Aggregation': [],
            'Edge': [],
            'Host': []
        }
        
        for name, device in sorted(self.topology.devices.items()):
            if 'Core' in device.device_type:
                layers['Core'].append((name, device))
            elif 'Aggregation' in device.device_type:
                layers['Aggregation'].append((name, device))
            elif 'Edge' in device.device_type:
                layers['Edge'].append((name, device))
            elif device.device_type == 'Host':
                layers['Host'].append((name, device))
        
        for layer_name in ['Core', 'Aggregation', 'Edge', 'Host']:
            if layers[layer_name]:
                print(f"\n🔸 Camada {layer_name}:")
                for name, device in layers[layer_name]:
                    print(f"  └─ {device}")
                    for iface_name, iface in device.interfaces.items():
                        print(f"      ├─ {iface_name}: {iface}")
                    if isinstance(device, Host):
                        print(f"      └─ Gateway: {device.gateway}")
        
        print("\n" + "="*80)
        print("\n🔗 ENLACES DA REDE:")
        print("-" * 80)
        for src, dst, link_type, capacity in self.topology.links:
            print(f"  {src} <---> {dst}")
            print(f"    Tipo: {link_type} | Capacidade: {capacity}")
        
        print("\n" + "="*80)
    
    def display_routing_table(self, device_name: str):
        """Exibe a tabela de roteamento de um dispositivo"""
        device = self.topology.devices.get(device_name)
        if not device:
            print(f"\n❌ Dispositivo '{device_name}' não encontrado!")
            return
        
        print(f"\n📋 TABELA DE ROTEAMENTO: {device}")
        print("-" * 80)
        print(f"{'Destino':<20} {'Máscara':<10} {'Próximo Hop':<20} {'Interface':<15}")
        print("-" * 80)
        
        # Redes diretamente conectadas
        for iface_name, iface in device.interfaces.items():
            print(f"{str(iface.network.network_address):<20} "
                  f"/{iface.network.prefixlen:<9} "
                  f"{'Directly Connected':<20} {iface_name:<15}")
        
        # Rotas da tabela
        for route in device.routing_table:
            print(f"{route['destination']:<20} "
                  f"/{route['mask']:<9} "
                  f"{route['next_hop']:<20} {route['interface']:<15}")
        
        print("-" * 80)
    
    def display_all_routing_tables(self):
        """Exibe todas as tabelas de roteamento"""
        routers = ['c1', 'a1', 'a2', 'e1', 'e2', 'e3', 'e4']
        for router_name in routers:
            self.display_routing_table(router_name)
            print()
    
    def xprobe(self, source_ip: str, dest_ip: str):
        """Comando XProbe - verifica conectividade e RTT"""
        print("\n" + "="*80)
        print(" XPROBE - VERIFICAÇÃO DE CONECTIVIDADE E RTT")
        print("="*80)
        print(f"\n🔍 Origem: {source_ip}")
        print(f"🎯 Destino: {dest_ip}")
        
        # Verifica se os IPs existem
        source_device = self.topology.get_device_by_ip(source_ip)
        dest_device = self.topology.get_device_by_ip(dest_ip)
        
        if not source_device:
            print(f"\n❌ ERRO: IP de origem {source_ip} não encontrado na rede!")
            return
        
        if not dest_device:
            print(f"\n❌ ERRO: IP de destino {dest_ip} não encontrado na rede!")
            return
        
        print(f"\n📍 Dispositivo Origem: {source_device}")
        print(f"📍 Dispositivo Destino: {dest_device}")
        
        # Traça a rota
        print(f"\n🛣️  TRAÇANDO ROTA:")
        print("-" * 80)
        path = self.topology.trace_route(source_ip, dest_ip)
        for i, hop in enumerate(path, 1):
            print(f"  {i}. {hop}")
        
        # Calcula RTT
        print(f"\n⏱️  MEDINDO RTT (3 amostras)...")
        print("-" * 80)
        
        is_active, samples, avg_rtt = self.topology.calculate_rtt(source_ip, dest_ip)
        
        if not is_active:
            print(f"\n❌ Host {dest_ip} está INATIVO ou INACESSÍVEL!")
            return
        
        for i, sample in enumerate(samples, 1):
            print(f"  Amostra {i}: {sample} ms")
        
        print("\n📊 ESTATÍSTICAS DO XPROBE:")
        print("-" * 80)
        print(f"  ✓ Status: ATIVO")
        print(f"  ✓ Pacotes enviados: 3")
        print(f"  ✓ Pacotes recebidos: 3")
        print(f"  ✓ Perda de pacotes: 0%")
        print(f"  ✓ RTT Mínimo: {min(samples)} ms")
        print(f"  ✓ RTT Máximo: {max(samples)} ms")
        print(f"  ✓ RTT Médio: {avg_rtt} ms")
        print(f"  ✓ Número de Hops: {len(path) - 1}")
        print("="*80)
    
    def run(self):
        """Executa o simulador com menu interativo"""
        while True:
            print("\n" + "="*80)
            print(" SIMULADOR DE REDE HIERÁRQUICA - MENU PRINCIPAL")
            print("="*80)
            print("\n1. Visualizar configuração da rede")
            print("2. Visualizar tabela de roteamento (específica)")
            print("3. Visualizar todas as tabelas de roteamento")
            print("4. Executar XProbe (ping com RTT)")
            print("5. Exemplo: XProbe de h1 para h8")
            print("6. Exemplo: XProbe de h3 para h5")
            print("0. Sair")
            
            choice = input("\nEscolha uma opção: ").strip()
            
            if choice == '1':
                self.display_network_info()
            
            elif choice == '2':
                device_name = input("\nDigite o nome do dispositivo (ex: c1, a1, e1, h1): ").strip()
                self.display_routing_table(device_name)
            
            elif choice == '3':
                self.display_all_routing_tables()
            
            elif choice == '4':
                print("\nDispositivos disponíveis:")
                print("Hosts: h1 (192.168.1.2), h2 (192.168.1.3), h3 (192.168.2.2), h4 (192.168.2.3)")
                print("       h5 (192.168.3.2), h6 (192.168.3.3), h7 (192.168.4.2), h8 (192.168.4.3)")
                source_ip = input("\nDigite o IP de origem: ").strip()
                dest_ip = input("Digite o IP de destino: ").strip()
                self.xprobe(source_ip, dest_ip)
            
            elif choice == '5':
                self.xprobe('192.168.1.2', '192.168.4.3')
            
            elif choice == '6':
                self.xprobe('192.168.2.2', '192.168.3.2')
            
            elif choice == '0':
                print("\n👋 Encerrando simulador...")
                break
            
            else:
                print("\n❌ Opção inválida!")
            
            input("\nPressione ENTER para continuar...")


def main():
    """Função principal"""
    print("\n" + "="*80)
    print(" SIMULADOR DE REDE HIERÁRQUICA")
    print(" Projeto 2 - Redes de Computadores")
    print("="*80)
    print("\nInicializando rede...")
    
    simulator = NetworkSimulator()
    print("✓ Rede configurada com sucesso!")
    print("✓ Topologia: 1 Core, 2 Aggregation, 4 Edge, 8 Hosts")
    
    simulator.run()


if __name__ == "__main__":
    main()
