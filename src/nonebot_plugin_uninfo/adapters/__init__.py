import os
import importlib
from typing import cast
from pathlib import Path
from warnings import warn

from nonebot import get_adapters

from ..loader import BaseLoader
from ..fetch import InfoFetcher

root = Path(__file__).parent
loaders: dict[str, BaseLoader] = {}
_adapters = [path.stem for path in root.iterdir() if path.is_dir() and not path.stem.startswith("_")]
for name in _adapters:
    try:
        module = importlib.import_module(f".{name}", __package__)
        loader = cast(BaseLoader, getattr(module, "Loader")())
        loaders[loader.get_adapter().value] = loader
    except Exception as e:
        warn(f"Failed to import uniseg adapter {name}: {e}", RuntimeWarning, 5)


INFO_FETCHER_MAPPING: dict[str, InfoFetcher] = {}
adapters = {}
try:
    adapters = get_adapters()
except Exception as e:
    warn(f"Failed to get nonebot adapters: {e}", RuntimeWarning, 5)

if os.environ.get("PLUGIN_UNINFO_TESTENV"):
    for adapter, loader in loaders.items():
        try:
            INFO_FETCHER_MAPPING[adapter] = loaders[adapter].get_fetcher()
        except Exception as e:
            warn(f"Failed to load uniseg adapter {adapter}: {e}", RuntimeWarning, 5)
elif not adapters:
    warn(
        "No adapters found, please make sure you have installed at least one adapter.",
        RuntimeWarning,
        5,
    )
else:
    for adapter in adapters:
        if adapter in loaders:
            try:
                INFO_FETCHER_MAPPING[adapter] = loaders[adapter].get_fetcher()
            except Exception as e:
                warn(f"Failed to load uniseg adapter {adapter}: {e}", RuntimeWarning, 5)
        else:
            warn(
                f"Adapter {adapter} is not found in the uniseg.adapters,"
                f"please go to the github repo and create an issue for it.",
                RuntimeWarning,
                5,
            )