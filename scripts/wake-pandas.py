import pandas as pd

# Sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Displaying the DataFrame
print("Sample DataFrame:")
print(df)