import pandas as pd
import numpy as np



df = pd.DataFrame({
    "id":np.random.randint(1001, 1020, 20),
    "age":np.random.randint(25, 55, 20), 
    "salary":np.random.randint(3000, 20000, 20)
    })

df1 = pd.DataFrame({
    "id":np.random.randint(1001, 1006, 10),
    "sales":np.random.randint(5000, 20000, 10), 
    "date":'Feb'
    })

df2 = pd.DataFrame({
    "id":np.random.randint(1001, 1006, 10),
    "sales":np.random.randint(10000, 100000, 10), 
    "date":'Mar'
    })

# 1. SELECT * FROM data;
print(df)
 
# 2. SELECT * FROM data LIMIT 10;
print(df.head(10))
 
# 3. SELECT id FROM data;  //id 是 data 表的特定一列
print(df['id'])
 
# 4. SELECT COUNT(id) FROM data;
print(df['id'].count())
 
# 5. SELECT * FROM data WHERE id<1000 AND age>30;
print(df[(df['id'] < 1000) & (df['age'] > 30)])
 
# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
print(df1.groupby('id').aggregate({'id': 'count', }))

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
print(pd.merge(df1, df2, on='id'))
 
# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
print(pd.concat([df1, df2]))

# 9. DELETE FROM table1 WHERE id=10;
print(df1[df1['id'] != 1002])

# 10. ALTER TABLE table1 DROP COLUMN column_name;
print(df1.rename(columns={'Feb': 'SAN'}, inplace=True))