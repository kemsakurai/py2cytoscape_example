# -*- coding: utf-8 -
from __future__ import print_function
import networkx as nx
from sklearn.feature_extraction import text


def __create_keywords_data():
    keywords = []
    # txtからキーワードを取得
    for line in open('keywords.txt', 'r'):
        if line != "":
            keywords.append(line)
    return keywords


def __check_stop_word(word):
    """
    stop word のチェック
    2文字以下の文字列を除去と、英語のstopwords を除去を行う
    """
    if len(word) <= 2:
        return False
    return True


def __split_keyword(text):
    """
    キーワードを区切り、stopwordsを除外する
    """
    keywords = text.split(" ")
    return [keyword for keyword in keywords if __check_stop_word(keyword)]


def __get_co_occurrence_matrix_from(keywords):
    # -----------------------------------------------------
    # 以下、CountVectorizer で共起単語行列を作っている
    # ----------------------------------
    from sklearn.feature_extraction.text import CountVectorizer
    count_model = CountVectorizer(ngram_range=(
        1, 1), stop_words=text.ENGLISH_STOP_WORDS)  # default unigram model
    X = count_model.fit_transform(keywords)

    # normalized co-occurence matrix
    import scipy.sparse as sp
    Xc = (X.T * X)
    g = sp.diags(2. / Xc.diagonal())
    Xc_norm = g * Xc

    import collections
    splited_keywords = []
    for keyword in keywords:
        splited_keywords.extend(__split_keyword(keyword))
    counter = collections.Counter(splited_keywords)
    return Xc_norm, count_model.vocabulary_, counter

    # -----------------------------------------------------
    # 以下、TfidfVectorizer で共起単語行列を作っている
    # ----------------------------------
    # from sklearn.feature_extraction.text import TfidfVectorizer
    # tfidf_vectorizer = TfidfVectorizer(ngram_range=(
    #     1, 1), stop_words=text.ENGLISH_STOP_WORDS, max_df=0.5, min_df=1, max_features=3000, norm='l2')
    # X = tfidf_vectorizer.fit_transform(keywords)
    # # normalized co-occurence matrix
    # import scipy.sparse as sp
    # Xc = (X.T * X)
    # g = sp.diags(2. / Xc.diagonal())
    # Xc_norm = g * Xc

    # import collections
    # splited_keywords = []
    # for keyword in keywords:
    #     splited_keywords.extend(utils.split_keyword(keyword))
    # counter = collections.Counter(splited_keywords)
    # return Xc_norm, tfidf_vectorizer.vocabulary_, counter


def main():

    # -------------------------
    # 1. キーワード文字列を取得
    # -------------------------
    keywords = __create_keywords_data()

    # -------------------------
    # 2. 共起単語行列を作成する
    # -------------------------
    Xc_norm, vocabulary, counter = __get_co_occurrence_matrix_from(keywords)

    # -------------------------
    # 3. networkx 描画データを作成   
    # -------------------------
    # 3-1.初期化ノードの追加
    G = nx.from_scipy_sparse_matrix(
        Xc_norm, parallel_edges=True, create_using=nx.DiGraph(), edge_attribute='weight')

    # 3-2.nodeに、count にcount属性を設定
    value_key_dict = {}
    for key, value in vocabulary.items():
        count = counter.get(key, 0)
        nx.set_node_attributes(G, "score", {value: count})
        value_key_dict.update({value: key})

    # 3-3.エッジと、ノードの削除
    # 同一ノードに引かれたエッジと、出現回数の少ないエッジを削除
    for (u, v, d) in G.edges(data=True):
        if u == v:
            G.remove_edge(u, v)

        if d["weight"] <= 0.0:
            G.remove_edge(u, v)

    # 出現回数の少ないノードを除去
    for n, a in G.nodes(data=True):
        if a["score"] <= 10:
            G.remove_node(n)

    # 3-4 ラベルの張り替え、from_scipy_sparse_matrix 設定時はラベルとして1,2,3 等の数値が設定されている
    G = nx.relabel_nodes(G, value_key_dict)

    # ------------------------------------------------------
    # 4 描画のために調整と、HTMLへのExport
    # ------------------------------------
    # Cytoscape に送信して、描画する
    # http://localhost:1234/v1/apply/layouts でレイアウトアルゴリズムのリストを取得できる
    from py2cytoscape.data.cyrest_client import CyRestClient
    cy = CyRestClient(ip='127.0.0.1', port=1234)
    for layout_algorithm in ["attribute-circle", "stacked-node-layout", "degree-circle", "circular", "attributes-layout", "kamada-kawai", "force-directed", "cose", "grid", "hierarchical", "fruchterman-rheingold", "isom", "force-directed-cl"]:
        print("plot start layout_algorithm [" + layout_algorithm + "]...")
        g_cy = cy.network.create_from_networkx(G)
        cy.layout.apply(name=layout_algorithm, network=g_cy)
        directed = cy.style.create('Curved')
        cy.style.apply(directed, network=g_cy)
        # エッジを束ねて見やすくする
        cy.edgebundling.apply(g_cy)
        view = g_cy.get_first_view()
        import exporter as exporter
        exporter.exportHTML(
            view, "html/" + layout_algorithm + "_export.html", 'custermizedCurved', background='radial-gradient(#898989 15%, #DDDDDD 105%)')
        print("plot end")


if __name__ == '__main__':
    main()
