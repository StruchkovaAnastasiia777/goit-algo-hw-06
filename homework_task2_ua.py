import networkx as nx
from collections import deque
import matplotlib.pyplot as plt

print("🔍 ЗАВДАННЯ 2: АЛГОРИТМИ DFS ТА BFS")
print("=" * 50)

# Використовуємо граф з першого завдання
def create_city_transport_graph():
    """Відтворює граф з завдання 1"""
    G = nx.Graph()
    
    districts = [
        "Центр", "Вокзал", "Університет", "Лікарня", "Ринок", 
        "Парк", "Житловий_масив", "Промзона", "Аеропорт", 
        "Стадіон", "Торговий_центр", "Школа"
    ]
    
    routes = [
        ("Центр", "Вокзал"), ("Центр", "Університет"), ("Центр", "Ринок"),
        ("Центр", "Торговий_центр"), ("Центр", "Лікарня"),
        ("Вокзал", "Аеропорт"), ("Вокзал", "Промзона"), ("Вокзал", "Житловий_масив"),
        ("Університет", "Школа"), ("Університет", "Лікарня"), ("Університет", "Парк"),
        ("Ринок", "Торговий_центр"), ("Ринок", "Житловий_масив"),
        ("Житловий_масив", "Школа"), ("Житловий_масив", "Лікарня"), ("Житловий_масив", "Стадіон"),
        ("Парк", "Стадіон"), ("Парк", "Торговий_центр"),
        ("Промзона", "Аеропорт"), ("Лікарня", "Стадіон"),
        ("Школа", "Торговий_центр"), ("Стадіон", "Торговий_центр")
    ]
    
    G.add_nodes_from(districts)
    G.add_edges_from(routes)
    
    return G

def dfs_paths(graph, start, goal, path=None):
    """
    Пошук у глибину (DFS) для знаходження всіх шляхів
    
    Args:
        graph: NetworkX граф
        start: початкова вершина  
        goal: цільова вершина
        path: поточний шлях (для рекурсії)
    
    Returns:
        Генератор всіх можливих шляхів від start до goal
    """
    if path is None:
        path = [start]
    
    if start == goal:
        yield path
    
    for neighbor in graph.neighbors(start):
        if neighbor not in path:  # Уникаємо циклів
            yield from dfs_paths(graph, neighbor, goal, path + [neighbor])

def dfs_path_single(graph, start, goal):
    """
    Пошук у глибину (DFS) для знаходження одного шляху
    
    Args:
        graph: NetworkX граф
        start: початкова вершина
        goal: цільова вершина
    
    Returns:
        Перший знайдений шлях або None
    """
    visited = set()
    stack = [(start, [start])]
    
    while stack:
        current, path = stack.pop()
        
        if current == goal:
            return path
            
        if current not in visited:
            visited.add(current)
            
            # Додаємо сусідів до стеку (в зворотному порядку для консистентності)
            neighbors = sorted(graph.neighbors(current), reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    
    return None

def bfs_path(graph, start, goal):
    """
    Пошук у ширину (BFS) для знаходження найкоротшого шляху
    
    Args:
        graph: NetworkX граф  
        start: початкова вершина
        goal: цільова вершина
    
    Returns:
        Найкоротший шлях або None
    """
    if start == goal:
        return [start]
    
    visited = set([start])
    queue = deque([(start, [start])])
    
    while queue:
        current, path = queue.popleft()
        
        # Сортуємо сусідів для консистентності результатів
        neighbors = sorted(graph.neighbors(current))
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                
                if neighbor == goal:
                    return new_path
                
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    
    return None

def compare_algorithms(graph, test_routes):
    """Порівнює результати DFS та BFS для різних маршрутів"""
    print("\n🆚 ПОРІВНЯННЯ АЛГОРИТМІВ DFS ТА BFS:")
    print("=" * 60)
    
    results = []
    
    for i, (start, goal) in enumerate(test_routes, 1):
        print(f"\n{i}. МАРШРУТ: {start} → {goal}")
        print("-" * 40)
        
        # DFS - знаходимо один шлях
        dfs_path = dfs_path_single(graph, start, goal)
        
        # BFS - знаходимо найкоротший шлях
        bfs_shortest = bfs_path(graph, start, goal)
        
        # DFS - знаходимо всі можливі шляхи (обмежуємо кількість)
        all_dfs_paths = list(dfs_paths(graph, start, goal))
        
        print(f"DFS (перший знайдений): {' → '.join(dfs_path) if dfs_path else 'Шлях не знайдено'}")
        if dfs_path:
            print(f"  Довжина: {len(dfs_path)} районів ({len(dfs_path)-1} пересадок)")
        
        print(f"\\nBFS (найкоротший): {' → '.join(bfs_shortest) if bfs_shortest else 'Шлях не знайдено'}")
        if bfs_shortest:
            print(f"  Довжина: {len(bfs_shortest)} районів ({len(bfs_shortest)-1} пересадок)")
        
        print(f"\\nВсього можливих шляхів (DFS): {len(all_dfs_paths)}")
        if len(all_dfs_paths) > 1:
            print("Альтернативні шляхи:")
            for j, path in enumerate(all_dfs_paths[:3], 1):  # Показуємо лише перші 3
                print(f"  {j}. {' → '.join(path)} ({len(path)-1} пересадок)")
            if len(all_dfs_paths) > 3:
                print(f"  ... та ще {len(all_dfs_paths)-3} шляхів")
        
        # Аналіз різниці
        if dfs_path and bfs_shortest:
            if len(dfs_path) == len(bfs_shortest):
                analysis = "✅ Однакова довжина - обидва алгоритми знайшли оптимальний шлях"
            elif len(dfs_path) > len(bfs_shortest):
                analysis = f"⚠️ DFS знайшов довший шлях (+{len(dfs_path)-len(bfs_shortest)} пересадок)"
            else:
                analysis = f"🔄 DFS випадково знайшов коротший шлях (-{len(bfs_shortest)-len(dfs_path)} пересадок)"
            
            print(f"\\n📊 Аналіз: {analysis}")
        
        results.append({
            'route': (start, goal),
            'dfs_path': dfs_path,
            'bfs_path': bfs_shortest,
            'all_paths_count': len(all_dfs_paths)
        })
    
    return results

def explain_differences():
    """Пояснює різницю між алгоритмами DFS та BFS"""
    print(f"\\n📚 ПОЯСНЕННЯ РІЗНИЦІ МІЖ DFS ТА BFS:")
    print("=" * 50)
    
    print(f"🔍 АЛГОРИТМ DFS (ПОШУК У ГЛИБИНУ):")
    print(f"• Стратегія: 'Іди якомога глибше, потім повертайся'")
    print(f"• Структура даних: СТЕК (останній увійшов - перший вийшов)")
    print(f"• Принцип роботи:")
    print(f"  1. Починає з початкової точки")
    print(f"  2. Йде по першому доступному маршруту до кінця")
    print(f"  3. Якщо зайшов у глухий кут - повертається назад")
    print(f"  4. Пробує інший маршрут")
    print(f"• Результат: Знаходить БУДЬ-ЯКИЙ шлях (не обов'язково найкоротший)")
    print(f"• Аналогія: Дослідження лабіринту методом 'правої руки'")
    
    print(f"\\n🌊 АЛГОРИТМ BFS (ПОШУК У ШИРИНУ):")
    print(f"• Стратегія: 'Перевір всіх сусідів, потім сусідів сусідів'")
    print(f"• Структура даних: ЧЕРГА (перший увійшов - перший вийшов)")
    print(f"• Принцип роботи:")
    print(f"  1. Починає з початкової точки")
    print(f"  2. Перевіряє всі сусідні райони")
    print(f"  3. Потім перевіряє сусідів цих районів")
    print(f"  4. Продовжує 'хвилями' до мети")
    print(f"• Результат: Завжди знаходить НАЙКОРОТШИЙ шлях")
    print(f"• Аналогія: Розповсюдження інформації або епідемії")
    
    print(f"\\n⚖️ ПОРІВНЯННЯ:")
    print(f"• Час виконання: Обидва O(V + E), але BFS зазвичай швидший для пошуку")
    print(f"• Пам'ять: DFS використовує менше пам'яті")
    print(f"• Гарантії: BFS завжди знаходить найкоротший шлях, DFS - ні")
    print(f"• Застосування:")
    print(f"  - DFS: Перевірка зв'язності, пошук циклів, топологічне сортування")
    print(f"  - BFS: Найкоротший шлях, рівневий обхід, пошук найближчого")

def visualize_paths(graph, results):
    """Візуалізує знайдені шляхи"""
    print(f"\\n🎨 ВІЗУАЛІЗАЦІЯ ЗНАЙДЕНИХ ШЛЯХІВ:")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Порівняння алгоритмів DFS та BFS: знайдені шляхи', fontsize=16, fontweight='bold')
    
    pos = nx.spring_layout(graph, seed=42, k=3, iterations=50)
    
    # Вибираємо два найцікавіші маршрути для візуалізації
    for idx, result in enumerate(results[:2]):
        start, goal = result['route']
        dfs_path = result['dfs_path']
        bfs_path = result['bfs_path']
        
        # DFS шлях
        ax_dfs = axes[idx, 0]
        nx.draw(graph, pos, ax=ax_dfs, with_labels=True, node_color='lightgray',
                node_size=800, font_size=8, font_weight='bold', edge_color='lightgray')
        
        if dfs_path:
            # Виділяємо шлях DFS
            path_edges = [(dfs_path[i], dfs_path[i+1]) for i in range(len(dfs_path)-1)]
            nx.draw_networkx_nodes(graph, pos, nodelist=dfs_path, node_color='red', 
                                 node_size=1000, ax=ax_dfs)
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', 
                                 width=3, ax=ax_dfs)
            # Виділяємо початок та кінець
            nx.draw_networkx_nodes(graph, pos, nodelist=[start], node_color='green', 
                                 node_size=1200, ax=ax_dfs)
            nx.draw_networkx_nodes(graph, pos, nodelist=[goal], node_color='orange', 
                                 node_size=1200, ax=ax_dfs)
        
        ax_dfs.set_title(f'DFS шлях: {start} → {goal}\\n{" → ".join(dfs_path) if dfs_path else "Шлях не знайдено"}', 
                        fontweight='bold')
        
        # BFS шлях
        ax_bfs = axes[idx, 1]
        nx.draw(graph, pos, ax=ax_bfs, with_labels=True, node_color='lightgray',
                node_size=800, font_size=8, font_weight='bold', edge_color='lightgray')
        
        if bfs_path:
            # Виділяємо шлях BFS
            path_edges = [(bfs_path[i], bfs_path[i+1]) for i in range(len(bfs_path)-1)]
            nx.draw_networkx_nodes(graph, pos, nodelist=bfs_path, node_color='blue', 
                                 node_size=1000, ax=ax_bfs)
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='blue', 
                                 width=3, ax=ax_bfs)
            # Виділяємо початок та кінець
            nx.draw_networkx_nodes(graph, pos, nodelist=[start], node_color='green', 
                                 node_size=1200, ax=ax_bfs)
            nx.draw_networkx_nodes(graph, pos, nodelist=[goal], node_color='orange', 
                                 node_size=1200, ax=ax_bfs)
        
        ax_bfs.set_title(f'BFS шлях: {start} → {goal}\\n{" → ".join(bfs_path) if bfs_path else "Шлях не знайдено"}', 
                        fontweight='bold')
    
    plt.tight_layout()
    plt.show()

# Основна програма
if __name__ == "__main__":
    # Створюємо граф
    G = create_city_transport_graph()
    
    print(f"Граф містить {G.number_of_nodes()} районів та {G.number_of_edges()} маршрутів")
    
    # Тестові маршрути для порівняння
    test_routes = [
        ("Вокзал", "Аеропорт"),
        ("Центр", "Школа"),  
        ("Парк", "Промзона"),
        ("Житловий_масив", "Університет")
    ]
    
    # Порівнюємо алгоритми
    results = compare_algorithms(G, test_routes)
    
    # Пояснюємо різницю
    explain_differences()
    
    # Візуалізуємо результати
    visualize_paths(G, results)
    
    # Збереження для завдання 3
    globals()['city_graph'] = G
    globals()['test_results'] = results