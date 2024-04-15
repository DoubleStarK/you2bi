# you2bi 自动爬取youtube视频发送到bilibili
> 自动爬取youtube视频发送到bilibili | 自动爬取机器人 | youtube | bilibili | 自动投稿
> - 通过向bilibili账号私信youtube链接,一键下载youtube视频并投稿到bilibili
> - 支持自动翻译标题,描述,tags

## TODO: 
  - [ ] 多平台支持
    - [x] macos
    - [ ] linux
    - [ ] windows
  - [ ] 消息模板自定义
  - [ ] 在聊天框中回复投稿状态
  - [ ] 可以选择使用Proxy
  - [ ] 视频防撞车(翻转,添加片头片尾)
  - [ ] 视频本地化(自动添加翻译字幕)
  - [ ] 自动爬取youtube前几条评论并发送到哔哩哔哩
  - [ ] 根据热词排行推荐视频

## Quick Start 使用方式
`python -V >= 3.9`

**macos**
- 第一步,确保有两个B站账号,并且可以相互发送私信,准备好这两个账号的uid

- 第二步,配置运行环境(暂时只支持macos)
```shell
git clone git@github.com:1130646208/you2bi.git && cd you2bi
python3 -m virtualenv .venv
source .venv/bin/activate
pip3 install requirements.txt
```

- 第三步,登录bilibili(需要根据自己平台指定可执行文件)
```shell
./biliup_macos_arm64 login
控制台出现二维码,用手机扫描二维码即可,出现cookie.json说明登录成功
```

- 第四步,运行自动爬取脚本
```shell
修改task_manager.py中最后的sender和receiver为第一步中的两个uid
python3 task_manager.py
```

- 最后一步,从youtube中复制视频链接,并从sender账号向receiver账号发送消息,具体格式(tid即[B站分区id](https://biliup.github.io/tid-ref.html)):
  - \$video_url\$ \<tid\>

## 致谢
- git@github.com:biliup/biliup-rs.git
- git@github.com:XiaoMiku01/biliup-go.git
- git@github.com:Quandong-Zhang/Violet.git
