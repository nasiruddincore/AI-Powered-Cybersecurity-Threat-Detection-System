import pandas as pd
import random
import os

def generate_traffic(num_samples=5000):
    data = []
    for _ in range(num_samples):
        # 70% chance of Normal traffic
        if random.random() > 0.3:
            packet_size = random.randint(100, 1500)
            login_attempts = random.randint(1, 3)
            conn_duration = random.randint(1, 60)
            error_rate = round(random.uniform(0.0, 0.05), 3)
            label = 0 # 0 = Normal
        else:
            # 30% chance of Attack traffic
            attack_type = random.choice(['dos', 'brute_force'])
            if attack_type == 'dos':
                packet_size = random.randint(3000, 10000) # Massive packets
                login_attempts = random.randint(1, 2)
                conn_duration = random.randint(100, 500)  # Long connections
                error_rate = round(random.uniform(0.5, 0.9), 3)
            else: # brute_force
                packet_size = random.randint(50, 200)
                login_attempts = random.randint(20, 100)  # High login attempts
                conn_duration = random.randint(5, 20)
                error_rate = round(random.uniform(0.8, 1.0), 3)
            label = 1 # 1 = Attack
            
        data.append([packet_size, login_attempts, conn_duration, error_rate, label])
        
    df = pd.DataFrame(data, columns=['packet_size', 'login_attempts', 'connection_duration', 'error_rate', 'label'])
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/network_traffic.csv', index=False)
    print(f"Generated {num_samples} records of synthetic network traffic in data/network_traffic.csv")

if __name__ == "__main__":
    generate_traffic()