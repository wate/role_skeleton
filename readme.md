ロールのスケルトン
=============================

Ansibleのロール作成時のスケルトンです。

設定方法
-----------------------------

以下の内容を `~/.ansible.cfg` に追記します。

```ini
[galaxy]
role_skeleton = </path/to/skeleton>/data
```

使い方
-----------------------------

ロールを作成するディレクトリに移動して、以下のコマンドを実行します。

```sh
ansible-galaxy role init <role_name>
```

※`<role_name>` にはロール名を指定します。
