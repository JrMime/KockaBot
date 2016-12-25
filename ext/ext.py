import asyncio

class Extension(object):
    def __init__(self, bot, config):
        self.config = config
        self.bot = bot
        self.delete = config.get('delete', None)

    def register_commands(self, *commands):
        self.commands = commands

    def join_params(self, params):
        return ' '.join(params)

    async def reply(self, message, reply_with, mention=False, delete=True):
        if(mention):
            reply_with = '%s: %s' % (message.author.mention, reply_with)
        msg = await self.bot.send_message(message.channel, reply_with)
        if(delete and self.delete):
            async def delete_message():
                await asyncio.sleep(self.delete)
                await self.bot.delete_message(message)
                await self.bot.delete_message(msg)
            asyncio.ensure_future(delete_message())

    async def call_command(self, message, command, args):
        if(command in self.commands):
            self.bot.loop.create_task(getattr(self, 'command_%s' % command)(message, args))

    async def call_listener(self, controller, listener, args):
        try:
            method = getattr(self, 'on_%s_%s' % (controller, listener))
            l = len(args)
            if(l == 1):
                generator = method(args[0])
            elif(l == 2):
                generator = method(args[0], args[1])
            else:
                generator = method(args[0], args[1], args[2])
            # Creating handler
            self.bot.loop.create_task(generator)
        except AttributeError:
            pass
