import pandas as pd
import numpy as np
from faker import Faker


dataset_size = 300000

fake = Faker()


data = {
    'Name': [fake.name() for _ in range(dataset_size)],
    'Age': np.random.randint(18, 91, size=dataset_size),
    'Family': np.random.randint(1, 7, size=dataset_size),
    'Income': (np.random.randint(10, 30001, size=dataset_size))//10*10
}

df = pd.DataFrame(data)


df['label'] = np.where(((df['Income'])//(df['Family']) < 90 ) | ((df['Income'])//(df['Family']) < 100 ),1, 0)
df.sort_values('label', inplace=True, ascending=False)
df.to_csv('random_data_with_label.csv', index=False)

print(df.head())
