# go_analysis.py

import pandas as pd


def load_go_data(file_path, category):
    """
    读取 GO 富集分析数据并打印数据列名及前几行
    :param file_path: GO 富集分析结果文件路径
    :param category: GO 类别 (BP, MF, CC)
    :return: GO 数据 DataFrame
    """
    try:
        # 读取 GO 富集分析数据
        go_df = pd.read_excel(file_path)

        # 打印 GO 数据的列名和前几行数据
        print(f"{category} 数据列名：")
        print(go_df.columns)

        print(f"\n{category} 数据前几行：")
        print(go_df.head())

        return go_df
    except Exception as e:
        print(f"读取 {category} 数据时出错: {e}")
        return None


def clean_go_data(go_df):
    """
    清理 GO 数据，去掉空值并标准化列名
    :param go_df: 原始 GO 数据
    :return: 清理后的 GO 数据
    """
    if go_df is not None:
        # 去掉含有空值的行
        go_df.dropna(inplace=True)

        # 列名标准化
        go_df.columns = ['Category', 'Term', 'Count', '%', 'PValue', 'Genes',
                         'List Total', 'Pop Hits', 'Pop Total', 'Fold Enrichment',
                         'Bonferroni', 'Benjamini', 'FDR']

        # 去掉 GO Term 的前缀
        go_df['Term'] = go_df['Term'].str.replace(r'^GO:\d+~', '', regex=True)

        return go_df
    else:
        print("GO 数据为空，无法进行清理。")
        return None


def filter_significant_go(go_df, p_value_threshold=0.05, top_n=10):
    """
    选择显著的 GO 富集条目（PValue < 0.05），并选择前 N 个
    :param go_df: 清理后的 GO 数据
    :param p_value_threshold: PValue 的显著性阈值
    :param top_n: 选择前 N 个条目
    :return: 显著的 GO 数据
    """
    if go_df is not None:
        go_df_sig = go_df[go_df['PValue'] < p_value_threshold].head(top_n)
        return go_df_sig
    else:
        print("GO 数据为空，无法进行筛选。")
        return None


def plot_go_enrichment(go_df_sig, category):
    """
    绘制 GO 富集分析的柱状图
    :param go_df_sig: 筛选后的显著 GO 数据
    :param category: GO 类别 (BP, MF, CC)
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    # 按百分比排序
    go_df_sig = go_df_sig.sort_values('%', ascending=False)

    # 绘制柱状图
    plt.figure(figsize=(8, 6))
    sns.barplot(x='%', y='Term', data=go_df_sig, palette='viridis')
    plt.title(f'{category} GO Enrichment')
    plt.xlabel('Percent of Genes (%)')
    plt.ylabel('GO Term')

    # 设置 x 轴刻度范围和间隔
    plt.xlim(0, 100)  # 设置 x 轴范围从 0 到 100
    plt.xticks(range(0, 101, 20))  # 设置 x 轴刻度间隔为 20

    # 启用灰色方格背景
    plt.grid(True, linestyle='--', color='gray', alpha=0.5)  # 设置网格线为灰色虚线，透明度为 0.5

    # 设置背景色为灰色
    plt.gca().set_facecolor('lightgray')

    plt.tight_layout()
    plt.show()
