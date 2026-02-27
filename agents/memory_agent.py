# utils/memory_agent.py
import json
import os

MEMORY_FILE = "agent_memory.json"

class MemoryAgent:

    def _read(self):
        if not os.path.exists(MEMORY_FILE):
            return {}
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    def _write(self, data):
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self, key, default=None):
        return self._read().get(key, default)

    def save(self, key, value):
        data = self._read()
        data[key] = value
        self._write(data)

    def append(self, key, value):
        data = self._read()
        data.setdefault(key, [])
        data[key].append(value)
        self._write(data)
