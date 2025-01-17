# 光工学研究室　研究データの保存方法

- 発表済み学術論文・博士論文に使用したデータ
- 博士・修士・学士論文（学位論文）の執筆に利用したデータ

を以下に述べるように整理・保存するようお願いします。

なお、ここでの「データ」とは、文章ファイル（tex, pdf, doc など）および図表ファイル、それらを作成するときに用いた実験データや解析スクリプト、数値計算データやそれを生成したプログラムなどを指します。

これらのデータを毎年の年度末（３月３１日）までに、データサーバQNAP（10.249.254.51）にアップロードするようにしてください。

# 実験ノート

実験を行うときは、実験ノートを必ずつけるようにしてください。
卒業時に実験ノートを研究室に残して置いてもらう必要があります。

可能であれば、実験ノートを１冊使い終わるごと、また卒業時にノートをスキャンして電子ファイルとしても残してもらうようお願いします。

卒業時に学位論文の最終原稿と一緒に実験ノートを提出して下さい．
手元に残す必要がある部分はコピーを取って下さい．

# QNAPの運用ポリシーについて

IP アドレスは 10.249.254.51 です。
（2021年3月1日から、アクセスにユーザー名・パスワードが必要になります。別途アナウンスしますのでそれを用いてください）

QNAPにBACK_UPというフォルダを用意してあります。
そこに各自のフォルダを作成して、データの整理・バックアップに使ってください。

QNAPにarchivesというフォルダがあります。
このフォルダには過去の卒業生のデータが保存されています。
このフォルダは読み込み専用です。
みなさんの卒業後、BACK_UP内のデータをこのフォルダに移します。

# フォルダの命名規則

BACK_UPのフォルダ内には、各自の名前に対応するフォルダを作成してください。  

例：BACK_UP/fujii

この個人フォルダの中に、以下のような構造でサブフォルダを配置してください。
```
BACK_UP  
└fujii  
　├backup  
　├thesis(bachelor)  
　├thesis(master)  
　├thesis(PhD)  
　├presentation(西暦・学会名)  
　├paper(西暦・ジャーナル名)  
　├lab_presentations  
　└archive
```

## backup ディレクトリ
各自で自由に使ってください

## thesis ディレクトリ, paper ディレクトリ
論文であるpdfファイル、それを作成するために使った doc ファイルや tex ファイル一式を保存してください。
論文内で用いた図のファイル、その図を作成するために使ったスクリプト、元データを整理して保存してください。
論文内で用いた図が、このディレクトリ内のデータだけから再現できるような完全なものとしておいてください。

学位論文の場合は、審査会・公聴会で使ったプレゼンテーションもこのディレクトリの中に保存してください。

ジャーナル論文の場合は出版後、学位論文の場合は最終稿の提出から１週間以内に作成・アップロードするようにしてください。

## presentation ディレクトリ
発表の要旨、プレゼンテーションファイルを保存してください。

## lab_presentations ディレクトリ
研究室内での発表に使ったファイルを保存してください。

## archive ディレクトリ
研究に関して取得したその他のデータ（論文に使わなかったものなど）を保存してください
実験ノートのスキャン結果もこのディレクトリに置いてください。


# 注意事項
まとめて作業しようとすると大変なんで、定期的に整理するようこころがけておいてください。