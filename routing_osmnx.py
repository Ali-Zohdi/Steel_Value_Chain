from geopy.geocoders import Nominatim
import geopy.distance
import osmnx as ox
import networkx as nx

# CALCULATES DISTANCE BETWEEN A LATITUDE&LONGITUDE COORDINATIOIN AND A GRAPH
def node_graph_distance(NODE, GRAPH):

    nearest_node = ox.distance.nearest_nodes(G=GRAPH, X=NODE[1], Y=NODE[0])
    GRAPH_X = GRAPH.nodes[nearest_node]['x']
    GRAPH_Y = GRAPH.nodes[nearest_node]['y']
    nearest_node = (GRAPH_Y, GRAPH_X)

    distance = geopy.distance.great_circle(NODE, nearest_node).km

    return distance, nearest_node

# JOINS TWO GRAPHS
def join_graphs(G1, G2):

    for node, data in G2.nodes(data=True):
        if G1.has_node(node):
            pass
        else:
            G1.add_node(node, **data)
    G1.add_edges_from(G2.edges.data())

    return G1

# CALCULATES DISTANCE BETWEEN TWO LATITUDE&LONGITUDE COORDINATIOINS
def routing_distance(coords_1, coords_2, radius = 0, threshold = 1):
    
    #calculating distance using geopy
    geodistance = geopy.distance.geodesic(coords_1, coords_2).km
    print(f"The distance between two coordinations using 'geopy' is {geodistance : .2f} kilometers.")

    #calculate radius
    if radius = 0:
        radius = round(geodistance)/4
    
    radius_km = radius*1000 

    #calculating the "Origin Graph" which is centered around coords_1
    graph = ox.graph_from_point(coords_1, dist=radius_km, network_type='drive')
    origin_node = ox.distance.nearest_nodes(G=graph, X=coords_1[1], Y=coords_1[0])

    #checking if the Origin Graph contains coords_2
    distance = node_graph_distance(coords_2, graph)[0]
    while distance > threshold: 
        #if the distance is less than 1 km (by default) then the graph contains coords_2
        #otherwise: 
        print(distance)
        nearest_node = node_graph_distance(coords_2, graph)[1] #nearest node to destination is calculated
        middle_graph = ox.graph_from_point(nearest_node, dist=radius_km, network_type='drive') #a middle graph is created
        graph = join_graphs(graph, middle_graph) #middle graph is added to the original graph
        distance = node_graph_distance(coords_2, graph)[0] #the distance is updated
        
        undirect_graph = graph.to_undirected()
        if not nx.is_connected(undirect_graph):
            print("Graph is not connected")
            for i in [1.2, 1.5, 1.7, 2]:
                middle_graph = ox.graph_from_point(nearest_node, dist= radius_km*i, network_type='drive')
                graph = join_graphs(graph, middle_graph)
                distance = node_graph_distance(coords_2, graph)[0]

                undirect_graph = graph.to_undirected()
                if nx.is_connected(undirect_graph):
                    break
        print("Graph is connected")
        

        #untill the distance is less than the threshold
    
    destination_node = ox.distance.nearest_nodes(G=graph, X=coords_2[1], Y=coords_2[0])
    
    route = nx.shortest_path(graph, origin_node, destination_node, 'length')
    route_length = nx.shortest_path_length(graph, origin_node, destination_node, 'length')

    print(f"The shortest path is about {route_length : .2f} meters")
    
    # routing = []
    # for node in route:
    #     routing.append(graph.nodes.data())
    
    return route, graph