import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

print("🚌 ЗАВДАННЯ 1: ТРАНСПОРТНА МЕРЕЖА МІСТА")
print("=" * 50)

def create_city_transport_graph():
    """Створює граф транспортної мережі міста (автобусні маршрути)"""
    G = nx.Graph()
    
    # Додаємо райони міста як вершини
    districts = [
        "Центр", "Вокзал", "Університет", "Лікарня", "Ринок", 
        "Парк", "Житловий_масив", "Промзона", "Аеропорт", 
        "Стадіон", "Торговий_центр", "Школа"
    ]
    
    G.add_nodes_from(districts)
    
    # Додаємо автобусні маршрути (ребра між районами)
    routes = [
        # Основні маршрути через центр
        ("Центр", "Вокзал"),
        ("Центр", "Університет"), 
        ("Центр", "Ринок"),
        ("Центр", "Торговий_центр"),
        ("Центр", "Лікарня"),
        
        # Маршрути від вокзалу
        ("Вокзал", "Аеропорт"),
        ("Вокзал", "Промзона"),
        ("Вокзал", "Житловий_масив"),
        
        # Університетські маршрути
        ("Університет", "Школа"),
        ("Університет", "Лікарня"),
        ("Університет", "Парк"),
        
        # Торгові маршрути
        ("Ринок", "Торговий_центр"),
        ("Ринок", "Житловий_масив"),
        
        # Житлові райони
        ("Житловий_масив", "Школа"),
        ("Житловий_масив", "Лікарня"),
        ("Житловий_масив", "Стадіон"),
        
        # Розважальні маршрути
        ("Парк", "Стадіон"),
        ("Парк", "Торговий_центр"),
        
        # Промислові маршрути  
        ("Промзона", "Аеропорт"),
        
        # Додаткові з'єднання
        ("Лікарня", "Стадіон"),
        ("Школа", "Торговий_центр"),
        ("Стадіон", "Торговий_центр")
    ]
    
    G.add_edges_from(routes)
    
    return G, districts, routes

def analyze_graph(G, districts, routes):
    """Аналізує основні характеристики графа"""
    print("\n📊 АНАЛІЗ ОСНОВНИХ ХАРАКТЕРИСТИК ГРАФА:")
    print("-" * 40)
    
    # Основні характеристики
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    print(f"Кількість вершин (районів): {num_nodes}")
    print(f"Кількість ребер (маршрутів): {num_edges}")
    print(f"Граф зв'язний: {'Так' if nx.is_connected(G) else 'Ні'}")
    
    # Ступені вершин
    degrees = dict(G.degree())
    print(f"\n🔢 СТУПЕНІ ВЕРШИН (кількість маршрутів):")
    for district, degree in sorted(degrees.items(), key=lambda x: x[1], reverse=True):
        print(f"  {district}: {degree} маршрутів")
    
    # Статистика ступенів
    degree_values = list(degrees.values())
    print(f"\n📈 СТАТИСТИКА СТУПЕНІВ:")
    print(f"  Середній ступінь: {np.mean(degree_values):.2f}")
    print(f"  Максимальний ступінь: {max(degree_values)}")
    print(f"  Мінімальний ступінь: {min(degree_values)}")
    
    # Щільність графа
    density = nx.density(G)
    print(f"\n🌐 ЩІЛЬНІСТЬ ГРАФА: {density:.3f}")
    print(f"  (Відношення існуючих ребер до максимально можливих)")
    
    # Діаметр та середня довжина шляху
    if nx.is_connected(G):
        diameter = nx.diameter(G)
        avg_path_length = nx.average_shortest_path_length(G)
        print(f"\n📏 ХАРАКТЕРИСТИКИ ВІДСТАНЕЙ:")
        print(f"  Діаметр графа: {diameter}")
        print(f"  Середня довжина шляху: {avg_path_length:.2f}")
    
    # Центральність
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    
    print(f"\n⭐ ТОП-3 НАЙВАЖЛИВІШІ РАЙОНИ:")
    
    print(f"\nЗа кількістю маршрутів (degree centrality):")
    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (district, centrality) in enumerate(top_degree, 1):
        print(f"  {i}. {district}: {centrality:.3f}")
    
    print(f"\nЗа центральністю (betweenness centrality):")
    top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (district, centrality) in enumerate(top_betweenness, 1):
        print(f"  {i}. {district}: {centrality:.3f}")
    
    print(f"\nЗа близькістю (closeness centrality):")
    top_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (district, centrality) in enumerate(top_closeness, 1):
        print(f"  {i}. {district}: {centrality:.3f}")
    
    return degrees, degree_centrality, betweenness_centrality

def visualize_graph(G, degrees, degree_centrality, betweenness_centrality):
    """Візуалізує граф з різними характеристиками"""
    print("\n🎨 СТВОРЕННЯ ВІЗУАЛІЗАЦІЇ:")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Транспортна мережа міста: Аналіз та візуалізація', fontsize=16, fontweight='bold')
    
    # Позиціонування вершин
    pos = nx.spring_layout(G, seed=42, k=3, iterations=50)
    
    # График 1: Базовий граф
    nx.draw(G, pos, ax=axes[0,0], with_labels=True, node_color='lightblue',
            node_size=1000, font_size=9, font_weight='bold', edge_color='gray')
    axes[0,0].set_title('Схема транспортної мережі\n(вершини = райони, ребра = маршрути)', fontweight='bold')
    
    # График 2: Розміри вузлів за ступенем
    node_sizes = [degrees[node] * 200 for node in G.nodes()]
    nx.draw(G, pos, ax=axes[0,1], with_labels=True, node_color='orange',
            node_size=node_sizes, font_size=9, font_weight='bold', edge_color='gray')
    axes[0,1].set_title('Кількість маршрутів\n(більший вузол = більше маршрутів)', fontweight='bold')
    
    # График 3: Кольори за центральністю по ступеню
    node_colors = [degree_centrality[node] for node in G.nodes()]
    nx.draw(G, pos, ax=axes[1,0], with_labels=True, 
            node_color=node_colors, node_size=1000, font_size=9, 
            font_weight='bold', edge_color='gray', cmap='Reds')
    axes[1,0].set_title('Центральність по ступеню\n(червоніший = важливіший)', fontweight='bold')
    
    # График 4: Кольори за центральністю посередництва
    node_colors = [betweenness_centrality[node] for node in G.nodes()]
    nx.draw(G, pos, ax=axes[1,1], with_labels=True,
            node_color=node_colors, node_size=1000, font_size=9,
            font_weight='bold', edge_color='gray', cmap='Blues')
    axes[1,1].set_title('Центральність посередництва\n(синіший = більше з\'єднує)', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def create_route_analysis(G):
    """Аналіз конкретних маршрутів"""
    print("\n🗺️ АНАЛІЗ КОНКРЕТНИХ МАРШРУТІВ:")
    print("-" * 40)
    
    # Найкоротші шляхи між важливими точками
    important_routes = [
        ("Вокзал", "Аеропорт"),
        ("Центр", "Університет"), 
        ("Житловий_масив", "Лікарня"),
        ("Парк", "Торговий_центр")
    ]
    
    for start, end in important_routes:
        if nx.has_path(G, start, end):
            path = nx.shortest_path(G, start, end)
            length = len(path) - 1
            print(f"  {start} → {end}: {' → '.join(path)} (пересадок: {length})")
        else:
            print(f"  {start} → {end}: Шлях не існує")

# Основна програма
if __name__ == "__main__":
    # Створюємо граф
    G, districts, routes = create_city_transport_graph()
    
    # Аналізуємо граф
    degrees, degree_centrality, betweenness_centrality = analyze_graph(G, districts, routes)
    
    # Візуалізуємо граф
    visualize_graph(G, degrees, degree_centrality, betweenness_centrality)
    
    # Аналізуємо маршрути
    create_route_analysis(G)
    
    # Повертаємо граф для використання в інших завданнях
    globals()['city_graph'] = G