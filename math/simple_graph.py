import matplotlib.pyplot as plt

server_a: list[int] = [20, 85, 18, 92, 25, 15, 28, 88, 21, 23]
server_b: list[int] = [45, 42, 48, 40, 46, 41, 49, 43, 47, 44]

def plot_graph():
    plt.figure(figsize=(10, 6))
    plt.plot(server_a, label="Server A", marker='o')
    plt.plot(server_b, label="Server B", marker='o')
    
    # Annotate Server A values
    for i, value in enumerate(server_a):
        plt.text(i, value + 2, str(value), ha='center', fontsize=9)
    
    # Annotate Server B values
    for i, value in enumerate(server_b):
        plt.text(i, value - 3, str(value), ha='center', fontsize=9)
    
    plt.title("Server Response Times")
    plt.xlabel("Ping Attempt")
    plt.ylabel("Response Time (ms)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_graph()