import networkx as nx
import matplotlib.pyplot as plt
import heapq
import numpy as np
from collections import defaultdict

print("🛣️ ЗАВДАННЯ 3: АЛГОРИТМ ДЕЙКСТРИ")
print("=" * 50)

def create_weighted_city_graph():
    """Створює зважений граф транспортної мережі з часом проїзду"""
    G = nx.Graph()
    
    # Додаємо райони
    districts = [
        "Центр", "Вокзал", "Університет", "Лікарня", "Ринок", 
        "Парк", "Житловий_масив", "Промзона", "Аеропорт", 
        "Стадіон", "Торговий_центр", "Школа"
    ]
    
    G.add_nodes_from(districts)
    
    # Додаємо маршрути з вагами (час проїзду в хвилинах)
    weighted_routes = [
        # Основні маршрути через центр (швидкі)
        ("Центр", "Вокзал", 8),
        ("Центр", "Університет", 12), 
        ("Центр", "Ринок", 6),
        ("Центр", "Торговий_центр", 10),
        ("Центр", "Лікарня", 15),
        
        # Маршрути від вокзалу
        ("Вокзал", "Аеропорт", 25),  # Довгий маршрут
        ("Вокзал", "Промзона", 18),
        ("Вокзал", "Житловий_масив", 20),
        
        # Університетські маршрути
        ("Університет", "Школа", 14),
        ("Університет", "Лікарня", 10),
        ("Університет", "Парк", 8),
        
        # Торгові маршрути
        ("Ринок", "Торговий_центр", 5),  # Короткий маршрут
        ("Ринок", "Житловий_масив", 22),
        
        # Житлові райони
        ("Житловий_масив", "Школа", 12),
        ("Житловий_масив", "Лікарня", 16),
        ("Житловий_масив", "Стадіон", 9),
        
        # Розважальні маршрути
        ("Парк", "Стадіон", 7),
        ("Парк", "Торговий_центр", 13),
        
        # Промислові маршрути  
        ("Промзона", "Аеропорт", 15),
        
        # Додаткові з'єднання
        ("Лікарня", "Стадіон", 11),
        ("Школа", "Торговий_центр", 17),
        ("Стадіон", "Торговий_центр", 8)
    ]
    
    # Додаємо зважені ребра
    for source, target, weight in weighted_routes:
        G.add_edge(source, target, weight=weight)
    
    return G, weighted_routes

def dijkstra_manual(graph, start):
    """
    Ручна реалізація алгоритму Дейкстри
    
    Args:
        graph: NetworkX граф з вагами
        start: початкова вершина
    
    Returns:
        distances: словник відстаней до всіх вершин
        previous: словник попередніх вершин для відновлення шляху
    """
    # Ініціалізація
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start] = 0
    previous = {node: None for node in graph.nodes()}
    unvisited = set(graph.nodes())
    
    print(f"\\n🔄 АЛГОРИТМ ДЕЙКСТРИ: крок за кроком від {start}")
    print("-" * 60)
    step = 0
    
    while unvisited:
        step += 1
        
        # Знаходимо вершину з найменшою відстанню
        current = min(unvisited, key=lambda node: distances[node])
        
        # Якщо відстань нескінченна, припиняємо
        if distances[current] == float('infinity'):
            break
        
        print(f"\\nКрок {step}: Обробляємо {current} (відстань: {distances[current]} хв)")
        
        # Оновлюємо відстані до сусідів
        for neighbor in graph.neighbors(current):
            if neighbor in unvisited:
                weight = graph[current][neighbor]['weight']
                new_distance = distances[current] + weight
                
                if new_distance < distances[neighbor]:
                    old_distance = distances[neighbor] if distances[neighbor] != float('infinity') else "∞"
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    print(f"  Оновлено {neighbor}: {old_distance} → {new_distance} хв (через {current})")
                else:
                    print(f"  {neighbor}: {new_distance} ≥ {distances[neighbor]} хв (не оновлюємо)")
        
        # Видаляємо поточну вершину з непереглянутих
        unvisited.remove(current)
        
        # Показуємо поточний стан (тільки для перших кроків)
        if step <= 3:
            print("  Поточні відстані:", end="")
            for node in sorted(graph.nodes()):
                dist = distances[node] if distances[node] != float('infinity') else "∞"
                visited_mark = "✓" if node not in unvisited else ""
                print(f" {node}:{dist}{visited_mark}", end="")
            print()
    
    return distances, previous

def reconstruct_path(previous, start, end):
    """Відновлює шлях від початку до кінця"""
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = previous[current]
    
    path.reverse()
    
    # Перевіряємо, чи існує шлях
    if path[0] == start:
        return path
    else:
        return None

def compare_with_networkx(graph, start):
    """Порівнює власну реалізацію з NetworkX"""
    print(f"\\n🔍 ПОРІВНЯННЯ З NETWORKX:")
    print("-" * 40)
    
    # Власна реалізація
    manual_distances, manual_previous = dijkstra_manual(graph, start)
    
    # NetworkX реалізація
    nx_distances = nx.single_source_dijkstra_path_length(graph, start, weight='weight')
    nx_paths = nx.single_source_dijkstra_path(graph, start, weight='weight')
    
    print(f"\\nПорівняння відстаней:")
    print(f"{'Вершина':<20} {'Власний алгоритм':<15} {'NetworkX':<15} {'Статус':<10}")
    print("-" * 60)
    
    all_correct = True
    for node in sorted(graph.nodes()):
        manual_dist = manual_distances[node] if manual_distances[node] != float('infinity') else "∞"
        nx_dist = nx_distances.get(node, "∞")
        
        if manual_distances[node] == nx_distances.get(node, float('infinity')):
            status = "✅"
        else:
            status = "❌"
            all_correct = False
        
        print(f"{node:<20} {str(manual_dist):<15} {str(nx_dist):<15} {status:<10}")
    
    if all_correct:
        print(f"\\n🎉 Власна реалізація працює правильно!")
    else:
        print(f"\\n⚠️ Знайдені розбіжності в реалізації")
    
    return manual_distances, manual_previous, nx_distances, nx_paths

def analyze_shortest_paths(graph, distances, previous, nx_paths, start_node):
    """Аналізує найкоротші шляхи"""
    print(f"\\n📊 АНАЛІЗ НАЙКОРОТШИХ ШЛЯХІВ ВІД {start_node}:")
    print("=" * 60)
    
    # Сортуємо за відстанню
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    
    print(f"{'Пункт призначення':<20} {'Час (хв)':<10} {'Найкоротший шлях':<30}")
    print("-" * 70)
    
    for destination, distance in sorted_distances:
        if destination != start_node and distance != float('infinity'):
            # Відновлюємо шлях
            path = reconstruct_path(previous, start_node, destination)
            if path:
                path_str = " → ".join(path)
                print(f"{destination:<20} {distance:<10} {path_str:<30}")
    
    # Найближчі та найдальші пункти
    accessible_destinations = [(dest, dist) for dest, dist in distances.items() 
                              if dest != start_node and dist != float('infinity')]
    
    if accessible_destinations:
        closest = min(accessible_destinations, key=lambda x: x[1])
        farthest = max(accessible_destinations, key=lambda x: x[1])
        
        print(f"\\n🎯 СТАТИСТИКА:")
        print(f"Найближчий пункт: {closest[0]} ({closest[1]} хв)")
        print(f"Найдальший пункт: {farthest[0]} ({farthest[1]} хв)")
        print(f"Середній час поїздки: {np.mean([dist for _, dist in accessible_destinations]):.1f} хв")

def create_shortest_path_tree(graph, start, previous):
    """Створює дерево найкоротших шляхів"""
    tree_edges = []
    for node, prev_node in previous.items():
        if prev_node is not None:
            tree_edges.append((prev_node, node))
    
    tree = nx.Graph()
    tree.add_edges_from(tree_edges)
    
    # Додаємо ваги до дерева
    for edge in tree_edges:
        weight = graph[edge[0]][edge[1]]['weight']
        tree[edge[0]][edge[1]]['weight'] = weight
    
    return tree

def visualize_dijkstra_results(graph, start, distances, previous, nx_paths):
    """Візуалізує результати алгоритму Дейкстри"""
    print(f"\\n🎨 ВІЗУАЛІЗАЦІЯ РЕЗУЛЬТАТІВ:")
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    fig.suptitle(f'Алгоритм Дейкстри: найкоротші шляхи від {start}', fontsize=16, fontweight='bold')
    
    pos = nx.spring_layout(graph, seed=42, k=3, iterations=50)
    
    # График 1: Вихідний зважений граф
    nx.draw(graph, pos, ax=axes[0,0], with_labels=True, node_color='lightblue',
            node_size=1000, font_size=9, font_weight='bold', edge_color='gray')
    
    # Додаємо ваги ребер
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, ax=axes[0,0], font_size=8)
    
    # Виділяємо початкову вершину
    nx.draw_networkx_nodes(graph, pos, nodelist=[start], node_color='green', 
                          node_size=1200, ax=axes[0,0])
    
    axes[0,0].set_title('Вихідний граф з вагами\\n(числа = час у хвилинах)', fontweight='bold')
    
    # График 2: Дерево найкоротших шляхів
    tree = create_shortest_path_tree(graph, start, previous)
    
    nx.draw(graph, pos, ax=axes[0,1], with_labels=True, node_color='lightgray',
            node_size=800, font_size=9, font_weight='bold', edge_color='lightgray', alpha=0.3)
    
    nx.draw_networkx_nodes(tree, pos, node_color='orange', node_size=1000, ax=axes[0,1])
    nx.draw_networkx_edges(tree, pos, edge_color='red', width=3, ax=axes[0,1])
    nx.draw_networkx_nodes(graph, pos, nodelist=[start], node_color='green', 
                          node_size=1200, ax=axes[0,1])
    
    axes[0,1].set_title('Дерево найкоротших шляхів\\n(червоні ребра = оптимальні маршрути)', fontweight='bold')
    
    # График 3: Відстані як розміри вузлів
    # Нормалізуємо відстані для розмірів вузлів
    max_distance = max([d for d in distances.values() if d != float('infinity')])
    node_sizes = []
    node_colors = []
    
    for node in graph.nodes():
        if distances[node] == float('infinity'):
            size = 300
            color = 'gray'
        else:
            # Інвертуємо: чим ближче, тим більше
            normalized_dist = 1 - (distances[node] / max_distance)
            size = 300 + normalized_dist * 1200
            color = plt.cm.get_cmap('RdYlGn')(normalized_dist)
        
        node_sizes.append(size)
        node_colors.append(color)
    
    nx.draw(graph, pos, ax=axes[1,0], with_labels=True, node_color=node_colors,
            node_size=node_sizes, font_size=9, font_weight='bold', edge_color='lightgray')
    
    axes[1,0].set_title('Відстані від початкової точки\\n(більший та зеленіший = ближче)', fontweight='bold')
    
    # График 4: Конкретні найкоротші шляхи
    nx.draw(graph, pos, ax=axes[1,1], with_labels=True, node_color='lightgray',
            node_size=800, font_size=9, font_weight='bold', edge_color='lightgray', alpha=0.5)
    
    # Вибираємо кілька цікавих шляхів для показу
    interesting_destinations = ['Аеропорт', 'Школа', 'Промзона']
    colors = ['red', 'blue', 'purple']
    
    for i, dest in enumerate(interesting_destinations):
        if dest in graph.nodes() and dest in nx_paths:
            path = nx_paths[dest]
            path_edges = [(path[j], path[j+1]) for j in range(len(path)-1)]
            
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, 
                                 edge_color=colors[i], width=3, alpha=0.7, ax=axes[1,1])
            nx.draw_networkx_nodes(graph, pos, nodelist=path, 
                                 node_color=colors[i], node_size=1000, alpha=0.7, ax=axes[1,1])
    
    # Виділяємо початкову вершину
    nx.draw_networkx_nodes(graph, pos, nodelist=[start], node_color='green', 
                          node_size=1200, ax=axes[1,1])
    
    axes[1,1].set_title(f'Приклади найкоротших шляхів\\n(різні кольори = різні маршрути)', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def practical_applications():
    """Розповідає про практичні застосування"""
    print(f"\\n🌍 ПРАКТИЧНІ ЗАСТОСУВАННЯ АЛГОРИТМУ ДЕЙКСТРИ:")
    print("=" * 50)
    
    applications = [
        ("🚗 GPS навігація", "Знаходження найкоротшого маршруту з урахуванням пробок"),
        ("🌐 Мережева маршрутизація", "Оптимальний шлях пакетів в інтернеті"),
        ("✈️ Авіаперевезення", "Планування найдешевших авіамаршрутів"),
        ("🚇 Громадський транспорт", "Оптимізація маршрутів міського транспорту"),
        ("📱 Соціальні мережі", "Знаходження найкоротших зв'язків між людьми"),
        ("🎮 Ігри", "Пошук шляху для персонажів (AI патфайндинг)"),
        ("💰 Фінанси", "Оптимізація торгових операцій та арбітражу"),
        ("🏥 Медицина", "Планування найшвидшого маршруту швидкої допомоги")
    ]
    
    for app, description in applications:
        print(f"{app}: {description}")

# Основна програма
if __name__ == "__main__":
    # Створюємо зважений граф
    G, weighted_routes = create_weighted_city_graph()
    
    print(f"Створено зважений граф з {G.number_of_nodes()} районів та {G.number_of_edges()} маршрутів")
    print(f"Ваги представляють час проїзду в хвилинах")
    
    # Вибираємо початкову точку
    start_point = "Центр"
    
    # Реалізуємо алгоритм Дейкстри та порівнюємо з NetworkX
    distances, previous, nx_distances, nx_paths = compare_with_networkx(G, start_point)
    
    # Аналізуємо результати
    analyze_shortest_paths(G, distances, previous, nx_paths, start_point)
    
    # Візуалізуємо результати
    visualize_dijkstra_results(G, start_point, distances, previous, nx_paths)
    
    # Практичні застосування
    practical_applications()
    
    # Фінальна статистика
    accessible_count = sum(1 for d in distances.values() if d != float('infinity')) - 1
    print(f"\\n📈 ФІНАЛЬНА СТАТИСТИКА:")
    print(f"• Доступних районів з {start_point}: {accessible_count}")
    print(f"• Середній час поїздки: {np.mean([d for d in distances.values() if d != float('infinity') and d > 0]):.1f} хв")
    print(f"• Найдовший маршрут: {max([d for d in distances.values() if d != float('infinity')]):.0f} хв")