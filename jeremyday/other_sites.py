from dataclasses import dataclass
from pathlib import Path

import strictyaml

# This describes the file format.
other_site_schema = strictyaml.Map(
    {
        "title": strictyaml.Str(),
        "href": strictyaml.Str(),
        "icon_src": strictyaml.Str(),
        strictyaml.Optional("withdrawn"): strictyaml.Bool(),
    }
)


# This describes the in-memory representation.
@dataclass
class OtherSite:
    title: str
    href: str
    icon_src: str
    number: int


cached_sites = None
sites_mtime = None


def get_sites(in_file: Path) -> list[OtherSite]:
    global cached_sites, sites_mtime
    new_mtime = in_file.stat().st_mtime
    if cached_sites is None or new_mtime > sites_mtime:
        data_yaml = in_file.read_text()
        data = strictyaml.load(data_yaml).data
        cached_sites = [
            OtherSite(number=i, **spec)
            for i, spec in enumerate(data["sites"])
            if not spec.get("withdrawn")
        ]
        sites_mtime = new_mtime
        print("Loaded", len(cached_sites), "from", in_file)
    return cached_sites
