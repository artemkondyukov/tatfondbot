# import Skype4Py
#
# skype = Skype4Py.Skype()
#
# skype.Attach()
#
# print ('Your full name:', skype.CurrentUser.FullName)
# print ('Your contacts:')

from skpy import Skype
from skpy import SkypeEventLoop, SkypeMessageEvent, SkypeNewMessageEvent, SkypeLocationMsg


# sk = Skype("andreevich_94", "55d52d33f3a")
#
# for user in sk.contacts:
#     print('    ', user.Name)


class SkypePing(SkypeEventLoop):
    def __init__(self):
        super(SkypePing, self).__init__("andreevich_94", "55d52d33f3a")

    def onEvent(self, event):
        # print(event)
        if isinstance(event, SkypeMessageEvent):
            if isinstance(event.msg, SkypeLocationMsg):
                # print(dir(event.msg))
                print(event.msg.latitude)
                print(event.msg.longitude)
            # elif isinstance(event, SkypeLocationMsg):
            #         # and not event.userId == self.userId:
            #     print(event)
            # print(123)
            # print(event)


sp = SkypePing()
print(123)
sp.loop()
