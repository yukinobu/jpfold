# jpfold

## 概要

日本語のテキストを、指定された幅にあわせて折りたたみます。[fold コマンド](http://linuxjm.osdn.jp/html/GNU_textutils/man1/fold.1.html)の日本語対応版を目指しています。

禁則処理、英文ワードラップ、インデント、引用行の無視に対応します。

### 入力例

```text
日本語の段落：
　味の先刻を、その個性が次第が破るまで、今日上に少し前一十五人の連れくらいの思い切りに、私かしです安心が進まあり当時ももうありせるの、ですば、できるだけこう秋刀魚をだるから、その事から足り方に「美味ま」すないしましない。

英語の段落：
For though result and talent add are parish valley. Songs in oh other avoid it hours woman style. In myself family as if be agreed. Gay collected son him knowledge delivered put. 

インデント（日）
  場合なありかし哲学に限らて、このご免は正直ない大変ないともつたのんは云っうらしい、なかろ百姓の後に承た間柄なするというてもらい「なら」のますませ。

インデント（英）
  Me of soon rank be most head time tore. Colonel or passage to ability.

箇条書き
  - また勢い今二三二人の気に入るだけもありだに対する横着です料簡をなるば、自分にその中そのために飛びて来なけれ方ます。
  1. Added would end ask sight and asked saw dried house. Property expenses yourself occasion endeavor two may judgment she.

引用行は無視
> 単にに金力に人ならです十一人結果が見えで、そこか潰すなくておりませにおいてはずにそうするたのだが、とうてい来るものを静粛だっと、けっして珍がしてついがいなくなけれ。
```

### 出力例（witdh=66）

```text
日本語の段落：
　味の先刻を、その個性が次第が破るまで、今日上に少し前一十五人の連
れくらいの思い切りに、私かしです安心が進まあり当時ももうありせるの、
ですば、できるだけこう秋刀魚をだるから、その事から足り方に「美味ま」
すないしましない。

英語の段落：
For though result and talent add are parish valley. Songs in oh 
other avoid it hours woman style. In myself family as if be agreed. 
Gay collected son him knowledge delivered put.

インデント（日）
  場合なありかし哲学に限らて、このご免は正直ない大変ないともつたの
  んは云っうらしい、なかろ百姓の後に承た間柄なするというてもらい
  「なら」のますませ。

インデント（英）
  Me of soon rank be most head time tore. Colonel or passage to 
  ability.

箇条書き
  - また勢い今二三二人の気に入るだけもありだに対する横着です料簡を
    なるば、自分にその中そのために飛びて来なけれ方ます。
  1. Added would end ask sight and asked saw dried house. Property 
     expenses yourself occasion endeavor two may judgment she.

引用行は無視
> 単にに金力に人ならです十一人結果が見えで、そこか潰すなくておりませにおいてはずにそうするたのだが、とうてい来るものを静粛だっと、けっして珍がしてついがいなくなけれ。
```

## 使い方

入出力は UTF-8 を使用します。

### テキストファイルを入出力に指定

```bash
python3 /path/to/jpfold.py -i in.txt -o out.txt
```

### クリップボード上のテキストを変換（on Cygwin）

```bash
cat /dev/clipboard | python3 /path/to/jpfold.py > /dev/clipboard
```

### クリップボード上のテキストを、行末の空白を除去しつつ変換（on Cygwin）

```bash
cat /dev/clipboard | python3 /path/to/jpfold.py | sed -E 's/[ 　\t]+\r/\r/g' > /dev/clipboard
```

### jpfold 自体をテスト

```ash
cd /path/to/jpfold && python3 -m unittest discover
```

## 動作環境

* Python 3.8 以上（3.8.6 にて動作を確認）

## 参考にしたもの

* [XTR](https://www.vector.co.jp/soft/dos/util/se004563.html) / [XTR for Win32](https://www.vector.co.jp/soft/win95/util/se025753.html)
* [fold コマンド](http://linuxjm.osdn.jp/html/GNU_textutils/man1/fold.1.html)
* [Becky! Internet Mail](https://www.rimarts.co.jp/becky-j.htm) のメールエディタ
* [reflow-japanese for Atom](https://atom.io/packages/reflow-japanese)
