import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.patches import Ellipse

def load_kegg_data(file_path):
    """
    读取 KEGG 富集分析数据并打印数据列名及前几行
    :param file_path: KEGG 富集分析结果文件路径
    :return: KEGG 数据 DataFrame
    """
    try:
        # 读取 KEGG 富集分析数据
        KEGG_df = pd.read_excel(file_path)

        # 打印 KEGG 数据的列名和前几行数据
        print("KEGG 数据列名：")
        print(KEGG_df.columns)

        print("\nKEGG 数据前几行：")
        print(KEGG_df.head())

        return KEGG_df
    except Exception as e:
        print(f"读取 KEGG 数据时出错: {e}")
        return None


def clean_kegg_data(KEGG_df):
    """
    清理 KEGG 数据，去掉空值并标准化列名
    :param KEGG_df: 原始 KEGG 数据
    :return: 清理后的 KEGG 数据
    """
    if KEGG_df is not None:
        # 去掉含有空值的行
        KEGG_df.dropna(inplace=True)

        # 列名标准化
        KEGG_df.columns = ['Category', 'Term', 'Count', '%', 'PValue', 'Genes',
                           'List Total', 'Pop Hits', 'Pop Total', 'Fold Enrichment',
                           'Bonferroni', 'Benjamini', 'FDR']

        # 去掉 KEGG Term 的前缀
        KEGG_df['Term'] = KEGG_df['Term'].str.replace(r'^hsa\d+:', '', regex=True)

        return KEGG_df
    else:
        print("KEGG 数据为空，无法进行清理。")
        return None


def filter_significant_kegg(KEGG_df, p_value_threshold=0.05, top_n=20):
    """
    选择显著的 KEGG 富集条目（PValue < 0.05），并选择前 N 个
    :param KEGG_df: 清理后的 KEGG 数据
    :param p_value_threshold: PValue 的显著性阈值
    :param top_n: 选择前 N 个条目
    :return: 显著的 KEGG 数据
    """
    if KEGG_df is not None:
        KEGG_df_sig = KEGG_df[KEGG_df['PValue'] < p_value_threshold].head(top_n)
        return KEGG_df_sig
    else:
        print("KEGG 数据为空，无法进行筛选。")
        return None


def plot_kegg_bubble_chart(KEGG_df, top_n=20):
    """
    绘制 KEGG 富集分析的气泡图
    :param KEGG_df: 需要绘制的 KEGG 数据
    :param top_n: 显示的 top N 条目
    """
    # 获取前 top_n 个 KEGG 富集数据
    KEGG_df_top = KEGG_df.head(top_n)

    # 创建一个图形并放置两个子图：一个用于颜色标尺，一个用于气泡大小标尺
    fig, ax = plt.subplots(figsize=(12, 8))

    # 使用气泡图
    scatter = sns.scatterplot(
        x='Count',  # X轴为 'Count'
        y='Term',  # Y轴为 'Term'
        size='Count',  # 气泡大小根据 'Count' 来设置
        hue=np.random.rand(top_n),  # 使用随机色彩
        data=KEGG_df_top,  # 使用的前 top_n 数据
        palette='rainbow',  # 彩虹色调的调色板
        sizes=(100, 500),  # 设置气泡大小范围（确保较大的气泡）
        legend=None  # 去掉图例
    )

    # 设置标题和标签
    ax.set_title('Top KEGG Enrichment Bubble Plot', fontsize=14)
    ax.set_xlabel('Count', fontsize=12)
    ax.set_ylabel('KEGG Term', fontsize=12)

    # 调整Y轴标签显示
    plt.xticks(rotation=45)
    plt.tight_layout()  # 自动调整布局避免标签重叠

    # 设置灰色方格背景（主要修改此部分）
    ax.set_facecolor('lightgray')  # 绘图区域背景为灰色
    ax.grid(True, which='both', axis='both', color='white', linestyle='-', linewidth=0.2)  # 白色网格线

    # 添加颜色条（Color Bar）
    norm = Normalize(vmin=0, vmax=25)  # 设置颜色条的范围为 [0, 25]
    sm = plt.cm.ScalarMappable(cmap="rainbow", norm=norm)
    sm.set_array([])  # 空数组用于颜色条的映射
    cbar = plt.colorbar(sm, ax=ax, shrink=0.3)  # 调整颜色条的长度
    cbar.set_label('-log10(PValue)', fontsize=12)
    cbar.ax.tick_params(labelsize=10)

    # 创建气泡大小图例
    legend_size = [15, 20, 25, 30]  # 气泡大小的四个示例
    legend_labels = [f'{s}' for s in legend_size]

    # 在右侧空白处添加气泡大小图例
    for i, size in enumerate(legend_size):
        ax.plot([], [], marker='o', markerfacecolor='black', markersize=np.sqrt(size), label=legend_labels[i],
                color='white')

    ax.legend(title='Bubble Size', loc='center left', bbox_to_anchor=(1, 0.2), fontsize=12)

    # 显示图形
    plt.show()

