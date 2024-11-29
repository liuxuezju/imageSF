# main.py
from kegg_analysis import load_kegg_data, clean_kegg_data, filter_significant_kegg, plot_kegg_bubble_chart
from go_analysis import load_go_data, clean_go_data, filter_significant_go, plot_go_enrichment

def analyze_kegg(file_path):
    # 加载 KEGG 数据
    KEGG_df = load_kegg_data(file_path)

    # 清理 KEGG 数据
    KEGG_df_cleaned = clean_kegg_data(KEGG_df)

    # 筛选显著 KEGG 数据
    KEGG_df_sig = filter_significant_kegg(KEGG_df_cleaned)

    # 打印筛选后的显著 KEGG 数据
    if KEGG_df_sig is not None:
        print("\n筛选后的显著 KEGG 富集分析结果：")
        print(KEGG_df_sig)

        # 绘制气泡图
        plot_kegg_bubble_chart(KEGG_df_sig)


def analyze_go(file_path, category):
    """
    根据 GO 文件路径和类别分析 GO 富集数据并绘制柱状图
    :param file_path: GO 富集分析文件路径
    :param category: GO 类别 (BP, MF, CC)
    """
    # 加载和处理 GO 数据
    go_df = load_go_data(file_path, category)
    go_df_cleaned = clean_go_data(go_df)
    go_df_sig = filter_significant_go(go_df_cleaned)

    # 绘制 GO 富集分析柱状图
    if go_df_sig is not None:
        plot_go_enrichment(go_df_sig, category)



def main():
    # KEGG 分析（可以选择运行 KEGG 分析）
    print("开始 KEGG 分析...")
    kegg_file_path = 'data/KEGG-分析.xlsx'  # KEGG 数据文件路径
    analyze_kegg(kegg_file_path)

    # GO 分析（可以选择运行 GO 分析）
    print("\n开始 GO 分析...")
    category = 'BP'   # 可替换为 'MF' 或 'CC
    go_file_path = f'data/GO-{category}分析.xlsx'
    analyze_go(go_file_path, category)


if __name__ == "__main__":
    main()
