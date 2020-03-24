import asyncio


class Storage:

    def __init__(self):
        self._tasks = []
        self.loop = asyncio.get_event_loop()
        self.loop.run_forever()
        self.loop.close()

    def create_task(self, action, route, data=None):
        task = None
        if 'insert' == action:
            task = asyncio.create_task(self.insert(route, data))

        if task:
            self._tasks.append(task)

    async def insert(self, route, obj):
        return obj

    async def show_tasks(self):
        return self._tasks
