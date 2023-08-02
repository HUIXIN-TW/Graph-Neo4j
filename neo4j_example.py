from py2neo import Graph

def connect_to_graph(uri, username, password):
    return Graph(uri, auth=(username, password))

def create_nodes_and_relationship(graph):
    create_nodes_query = """
    CREATE (alice:Person {name: 'Alice', age: 30})
    CREATE (bob:Person {name: 'Bob', age: 40})
    """
    graph.run(create_nodes_query)

    create_relationship_query = """
    MATCH (alice:Person {name: 'Alice'})
    MATCH (bob:Person {name: 'Bob'})
    CREATE (alice)-[:FRIENDS_WITH]->(bob)
    """
    graph.run(create_relationship_query)

def print_relationships(graph):
    retrieve_query = """
    MATCH (a:Person)-[r:FRIENDS_WITH]->(b:Person)
    RETURN a.name AS person1, b.name AS person2
    """
    relationship_result = graph.run(retrieve_query).data()
    for record in relationship_result:
        print(f"{record['person1']} is friends with {record['person2']}")

def print_node_count(graph):
    count_result = graph.run("MATCH (n) RETURN COUNT(n) AS count").data()
    node_count = count_result[0]['count']
    print(f"Number of nodes in the database: {node_count}")

def delete_all_nodes_relationships(graph):
    # Query to delete all nodes and relationships
    delete_query = """
    MATCH (n)
    DETACH DELETE n
    """
    # Prompt the user for confirmation
    user_input = input("Do you want to delete ALL nodes and relationships? (yes/no): ")
    if user_input.lower() == 'yes':
        graph.run(delete_query)
        print("All nodes and relationships have been deleted.")
    else:
        print("Operation aborted. No nodes or relationships were deleted.")

def delete_bob(graph):
    check_relationships_query = """
    MATCH (bob:Person {name: 'Bob'})-[r]-()
    RETURN COUNT(r) AS relationship_count
    """
    relationship_count = graph.run(check_relationships_query).evaluate()

    if relationship_count > 0:
        print("Warning: The node representing 'Bob' has relationships with other nodes.")
        user_input = input("Do you want to delete this node and all its relationships? (yes/no): ")
        if user_input.lower() == 'yes':
            delete_bob_query = """
            MATCH (bob:Person {name: 'Bob'})
            DETACH DELETE bob
            """
            graph.run(delete_bob_query)
            print("Node representing 'Bob' and all its relationships have been deleted.")
        else:
            print("Operation aborted. The node was not deleted.")
    else:
        print("'Bob' does not have any relationships.")

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "your_password"  # Replace with your actual password

    graph = connect_to_graph(uri, username, password)
    create_nodes_and_relationship(graph)
    print_relationships(graph)
    print_node_count(graph)
    # delete_all_nodes_relationships(graph)
    # delete_bob(graph)
