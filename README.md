# py2cytoscape_example
Google Search Console から取得した検索キーワードを py2cytoscape を使って Network図に描画するサンプルスクリプトです。    

------------------------------------------------------------------------------
## 前提   
以下、実行に必要なアプリケーションとpython パッケージと、動作確認した python の version について記載します。   

* **python の verison**   
```console
% python -V
Python 2.7.10
```

* **アプリケーション**    
Cytoscape、cyRESTのインストールが必要になります。       
[Cytoscape / cyRESTとpy2cytoscapeを用いたIPython Notebook上でのグラフ解析と可視化 Part 1 - Qiita](http://qiita.com/keiono/items/ed796643107bd03aff64#cytoscape%E5%81%B4%E3%81%AE%E6%BA%96%E5%82%99)  
が参考になりました。    
スクリプト実行時は、CytoscapeのAPIを呼び出すため、ローカル環境のCytoscapeを起動しておく必要があります。   

* **パッケージインストール**     
```console
% pip install networkx
% pip install sklearn
% pip install py2cytoscape
```

-----------------------------------------------------------------------------
## インストール、実行方法    

### インストール、実行
* **git clone**    
```console
% git clone https://github.com/kemsakurai/py2cytoscape_example.git
```

* **ディレクトリ移動**
```console
% cd py2cytoscape_example/
```

* **スクリプト実行**
```console
% python export_keyword_network.py    
plot start layout_algorithm [attribute-circle]...
plot end
plot start layout_algorithm [stacked-node-layout]...
plot end
plot start layout_algorithm [degree-circle]...
plot end
plot start layout_algorithm [circular]...
plot end
plot start layout_algorithm [attributes-layout]...
plot end
plot start layout_algorithm [kamada-kawai]...
plot end
plot start layout_algorithm [force-directed]...
plot end
plot start layout_algorithm [cose]...
plot end
plot start layout_algorithm [grid]...
plot end
plot start layout_algorithm [hierarchical]...
plot end
plot start layout_algorithm [fruchterman-rheingold]...
plot end
plot start layout_algorithm [isom]...
plot end
plot start layout_algorithm [force-directed-cl]...
plot end
```
出力には結構時間がかかります。   

* **HTMLの出力先**
スクリプトの実行が完了すると、htmlフォルダにhtmlが出力されます。   
```
% cd html
% ls -1
attribute-circle_export.html
attributes-layout_export.html
circular_export.html
cose_export.html
degree-circle_export.html
force-directed-cl_export.html
force-directed_export.html
fruchterman-rheingold_export.html
grid_export.html
hierarchical_export.html
isom_export.html
kamada-kawai_export.html
stacked-node-layout_export.html
```

--------------------------------------------------------------------
## キーワードを入れ替える   
Google Search Console 等の Webマスターツールから検索キーワードを取得し、スペース区切りでkeywords.txtにコピー&ペーストしてください。   
```console
% head keywords.txt
java uribuilder
django modelchoicefield
sonarqube 日本語化
bootstrap's javascript requires jquery version 1.9.1 or higher, but lower than version 3
sonarqube 日本語
@transactional ネスト
pycharm terminal
uribuilder java
django crontab
uncaught error: bootstrap's javascript requires jquery version 1.9.1 or higher, but lower than version 3
```
その後スクリプトを実行すると、対象キーワードの共起ネットワーク図が出力されます。    
