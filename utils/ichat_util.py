import traceback

import itchat
from itchat.content import TEXT


class IchatUtil:
    def __init__(self,callback):
        self.callback = callback
        self.start_itchat()

    def start_itchat(self):
        @itchat.msg_register([TEXT], isGroupChat=True)
        def text_reply(msg):
            if msg.isAt:
                msg.user.send(f"{msg.actualNickName}，你的消息收到了，处理中，香蕉你个芭拉！")
                try:
                    self.callback(msg)
                except:
                    msg.user.send(f"出错了！！！香蕉你个芭拉！\n{traceback.format_exc()}")


        itchat.auto_login(enableCmdQR=2, hotReload=True)  # type: ignore
        itchat.run()
