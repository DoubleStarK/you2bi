# you2bi 自动爬取youtube视频发送到bilibili
> 自动爬取youtube视频发送到bilibili | 自动爬取机器人 | youtube | bilibili | 自动投稿
> - 通过向bilibili账号私信youtube链接,一键下载youtube视频并投稿到bilibili
> - 支持自动翻译标题,描述,tags

## TODO: 
  - [ ] 多平台支持
    - [x] macos
    - [ ] linux
    - [x] windows
  - [x] 消息模板自定义
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
pip3 install -r requirements.txt
```

- 第三步,登录bilibili(暂时只支持macos,windows)
```shell
./setup.sh
控制台出现二维码,用手机扫描二维码即可,出现cookie.json说明登录成功
```

- 第四步,运行自动爬取脚本
```shell
修改task_manager.py中最后的sender和receiver为第一步中的两个uid
python3 task_manager.py
```

- 最后一步,从youtube中复制视频链接,并从sender账号向receiver账号发送消息,具体格式可在message_template.py->__get_keywords中自定义:
  - 默认模板：
```python
            r'<v:\s*(.*?)\s*>': 'video_url', # 这样定义，则消息中的<v:https://youtube.com/xxx>视频链接可被识别出来
            r'<vt:\s*(.*?)\s*>': 'video_type', # 这样定义，则消息中的<vt:1>视频类型（1自制，2转载）可被识别出；下面的以此类推
            r'<tid:\s*(.*?)\s*>': 'tid', # 投稿分区tid
            r'<trans:\s*(.*?)\s*>': 'trans_video_meta', # 是否翻译视频标题，tag和描述
            r'<sf:\s*(.*?)\s*>': 'subtitle_from', # 开发中，暂不可用
            r'<st:\s*(.*?)\s*>': 'subtitle_to',  # 开发中，暂不可用
            r'<dlo:\s*(.*?)\s*>': 'download_only', # 仅下载
```
- 示例消息：
  - `可以添加一些额外内容 <v:视频链接> <vt:1自制2转载> <tid:投稿分区tid> <trans:True(是否翻译)> <dlo:True(仅下载)> 可以添加一些额外内容'`
 
## 更新日志
- 20240526：新增消息模板功能，用户可自定义想发送消息的格式，通过发送的消息控制此次下载上传任务；任务记录现在保存在data_v2.json中了。
- 20240601：儿童节快乐！支持了windows平台。

## 致谢
> - git@github.com:biliup/biliup-rs.git
> - git@github.com:XiaoMiku01/biliup-go.git
> - git@github.com:Quandong-Zhang/Violet.git


