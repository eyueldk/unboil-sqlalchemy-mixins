
# unboil-signals


Lightweight, strongly-typed event and signal library for Python.

## Installation


```bash
pip install unboil-signals
```

## Quick Start


```python
from unboil_signals import SyncSignal, AsyncSignal, SyncEvent, AsyncEvent
import asyncio

# 1. SyncSignal: listeners can return values
sig = SyncSignal[[int], str]()  # takes an int, returns str

@sig
def listener(x: int) -> str:
    return f"got {x}"

results = sig.invoke(42)  # returns ["got 42"]

# 2. AsyncSignal: async listeners with await
async_sig = AsyncSignal[[int], str]()  # takes int, returns str

@async_sig
async def async_listener(x: int) -> str:
    await asyncio.sleep(0.1)
    return f"async got {x}"

responses = await async_sig.ainvoke(7)  # sequential
all_responses = await async_sig.ginvoke(7)  # parallel with asyncio.gather

# 3. SyncEvent / AsyncEvent: no return values
evt = SyncEvent[str]()

@evt
def on_msg(msg: str) -> None:
    print(msg)

evt.invoke("Hello")

async_evt = AsyncEvent[str]()

@async_evt
async def on_async(msg: str) -> None:
    await asyncio.sleep(0.1)
    print(msg)

await async_evt.ainvoke("Hi")
```

## API

- **SyncSignal[P, T]** - register callables `Callable[P, T]`, invoke synchronously
- **AsyncSignal[P, T]** - register `Callable[P, Awaitable[T]]`, invoke with `ainvoke` or `ginvoke`
- **SyncEvent[P]** - subclass of `SyncSignal[P, None]` (ignore return)
- **AsyncEvent[P]** - subclass of `AsyncSignal[P, Awaitable[None]]`

## Contributing

Pull requests welcome. Please run tests and follow code style.

## License

MIT
