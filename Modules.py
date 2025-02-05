# I don't even know how it works. Is AI code and is seems working.
import importlib
import sys
import os
import re
from types import ModuleType
from typing import List, Optional

try:
    from .Logger import Logger
except ImportError:
    from Logger import Logger

class Modules:
    def __init__(self, path: Optional[str] = None, log_level: Optional[int] = None):
        self.logger = Logger('putils.Modules', log_level=(3 if log_level is None else log_level))
        self.path = os.path.abspath(path or ".")
        if not os.path.isdir(self.path):
            raise NotADirectoryError(f"Path '{self.path}' is not a directory.")
        self.loaded_modules = {}
        if self.path not in sys.path:
            sys.path.insert(0, self.path)

    def _is_valid_module_name(self, name: str) -> bool:
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

    def load(self, module_name: str) -> ModuleType:
        if not self._is_valid_module_name(module_name):
            self.logger.log(4, f"Invalid module name '{module_name}'.")
            raise ValueError("Invalid module name.")
        try:
            module = importlib.import_module(module_name)
            module_path = os.path.abspath(module.__file__)
            if not module_path.startswith(os.path.abspath(self.path)):
                self.logger.log(4, f"Module '{module_name}' not in '{self.path}'.")
                del sys.modules[module_name]
                raise ImportError(f"Module '{module_name}' not found in path.")
            self.loaded_modules[module_name] = module
            self.logger.log(1, f"Loaded '{module_name}' successfully.")
            return module
        except Exception as e:
            self.logger.log(4, f"Error loading '{module_name}': {e}")
            raise

    def reload(self, module_name: str) -> ModuleType:
        if module_name in self.loaded_modules:
            try:
                module = importlib.reload(self.loaded_modules[module_name])
                self.loaded_modules[module_name] = module
                self.logger.log(1, f"Reloaded '{module_name}' successfully.")
                return module
            except Exception as e:
                self.logger.log(4, f"Error reloading '{module_name}': {e}")
                raise
        else:
            self.logger.log(3, f"Module '{module_name}' not loaded.")
            raise ImportError("Module not loaded.")

    def unload(self, module_name: str):
        if module_name in self.loaded_modules:
            for name in list(sys.modules):
                if name == module_name or name.startswith(f"{module_name}."):
                    del sys.modules[name]
            del self.loaded_modules[module_name]
            self.logger.log(1, f"Unloaded '{module_name}'.")
        else:
            self.logger.log(3, f"Cannot unload '{module_name}': not loaded.")

    def list(self) -> List[str]:
        modules = []
        try:
            for root, dirs, files in os.walk(self.path):
                rel_path = os.path.relpath(root, self.path)
                for f in files:
                    if f.endswith(".py") and f != "__init__.py":
                        name = os.path.splitext(f)[0]
                        if self._is_valid_module_name(name):
                            if rel_path == '.':
                                modules.append(name)
                            else:
                                module_path = rel_path.replace(os.sep, '.') + '.' + name
                                modules.append(module_path)
                dirs[:] = [d for d in dirs if os.path.exists(os.path.join(root, d, '__init__.py'))]
            return modules
        except Exception as e:
            self.logger.log(4, f"Error listing modules: {e}")
            raise