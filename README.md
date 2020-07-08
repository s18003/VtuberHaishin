# VtuberHaishin

# これなに？
こいつは「推しVtuber配信予定表」

実はもともとVtuberの配信予定表サイトが存在するのだが、

ほぼ全てのVtuberが利用している為表示量が膨大。

これでは目が疲れる(当社比)ので、

自分が見たいVtuberの配信予定だけをとってこれるのが、この推しVtuber配信予定表です



# 使うための前準備
pythonの実行環境を整える(利用するためにpythonが必要なので)

ここ参照　https://www.sejuku.net/blog/33294

あとこいつらもインストール推奨

'''bash
pip3 install Flask
pip3 install beautifulsoup4
pip3 install sqlalchemy
'''


# 使い方
run.pyを実行

うまくいけばURLが出てくるのでそこにアクセスする(localhost:5000でいける)

アクセスすると真ん中にでかでかと好きなVtber入れてね～ってのがあるので、

そこに予定表をとってきたい人の名前を入れる

予定表の更新は真ん中の青いボタンによる手動

配信者、配信タイトルはそれぞれ外部リンクとなっており、

配信者は元の予定表にある個人ページ

配信タイトルは配信していればそのまま配信サイトへ、してなければ配信者と同じ個人ページにとぶ

その他機能は削除とかそのへん
