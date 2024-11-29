import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 数据
data = {
    '成分名称': ['kielcorin', 'osmundacetone', 'hispidin', 'sterubin', '(E)-4-(4-hydroxyphenyl)-3-buten-2-one', 'davallialactone', 'citrinin'],
    'TP53_1AIE': [-7.6, -5.3, -6.2, -6.5, -5.2, -7.5, -5.8],
    'PTEN_5BZZ': [-9.1, -6.6, -7.7, -8.2, -6.2, -9.3, -6.6],
    'MYC_1NKP': [-8.5, -6.5, -7.6, -8.4, -6.5, -10.5, -7],
    'STAT3_6NJS': [-7.4, -5.9, -7.1, -5.5, -5.3, -7, -4.6],
    'CTNNB1_7AFW': [-7, -5.3, -6.1, -6.7, -5.3, -7.5, -6.2],
    'PARP_6NRG': [-8.2, -7.2, -7.1, -8.8, -6.5, -9.4, -6.4],
    'CASP3_4QU9': [-7.3, -6.4, -6.8, -7.9, -6, -8.4, -6.3]
}

# 转换为DataFrame格式
df = pd.DataFrame(data)

# 设置成分名称为索引
df.set_index('成分名称', inplace=True)

# 创建热力图
plt.figure(figsize=(10, 8))
sns.heatmap(df, cmap='coolwarm', annot=True, fmt=".1f", linewidths=0.5)
plt.title('Heatmap of Active Components and Targets')
plt.xlabel('Targets')
plt.ylabel('Active Components')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.savefig('heatmap.png', bbox_inches='tight')
plt.show()

