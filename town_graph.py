"""Town graph for NavIndlela: data model, loading and validation.

The town is a directed graph.
- Intersections are nodes (with x/y coordinates, used later for drawing and turns).
- Street segments are edges. A two-way segment can be driven in both directions,
  a one-way segment only from `start` to `end`.
- Places (buildings) sit at an intersection and have an address: street + number.
"""
from __future__ import annotations

import json
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path


class TownError(ValueError):
    """Raised when the town data is malformed or invalid."""


@dataclass(frozen=True)
class Intersection:
    id: str
    x: float
    y: float
    zone: str = ""  # neighbourhood name, e.g. "CBD"


@dataclass(frozen=True)
class Segment:
    start: str
    end: str
    street: str
    one_way: bool = False


@dataclass(frozen=True)
class Place:
    id: str
    name: str
    street: str
    number: int
    node: str  # id of the intersection the place is attached to


class Town:
    def __init__(self, name, intersections, segments, places):
        self.name = name
        self.intersection_list = list(intersections)
        self.segment_list = list(segments)
        self.place_list = list(places)

        self.intersections = {i.id: i for i in self.intersection_list}
        self.places = {p.id: p for p in self.place_list}

        # Directed adjacency: node -> [(neighbour, street)]
        self._outgoing = defaultdict(list)
        # Every street that touches a node, in either direction
        self._streets_at = defaultdict(set)
        for s in self.segment_list:
            self._outgoing[s.start].append((s.end, s.street))
            if not s.one_way:
                self._outgoing[s.end].append((s.start, s.street))
            self._streets_at[s.start].add(s.street)
            self._streets_at[s.end].add(s.street)

    # ----- queries -----

    def outgoing(self, node):
        """Where you can drive from this node: [(neighbour_id, street_name)]."""
        return list(self._outgoing.get(node, []))

    def streets(self):
        return sorted({s.street for s in self.segment_list})

    def streets_at(self, node):
        return set(self._streets_at.get(node, set()))

    def places_on_street(self, street):
        return sorted(
            (p for p in self.place_list if p.street == street),
            key=lambda p: p.number,
        )

    def reachable_from(self, node):
        """All nodes reachable from `node`, respecting one-way streets."""
        seen = {node}
        queue = deque([node])
        while queue:
            current = queue.popleft()
            for neighbour, _ in self._outgoing.get(current, []):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        return seen

    def dead_ends(self):
        """Nodes connected to exactly one other node (ignoring direction)."""
        neighbours = defaultdict(set)
        for s in self.segment_list:
            neighbours[s.start].add(s.end)
            neighbours[s.end].add(s.start)
        return sorted(n for n, nb in neighbours.items() if len(nb) == 1)

    def zones(self):
        """Neighbourhood names, sorted."""
        return sorted({i.zone for i in self.intersection_list if i.zone})

    def zone_of(self, place_id):
        """The neighbourhood a place is in."""
        return self.intersections[self.places[place_id].node].zone

    def places_in_zone(self, zone):
        return sorted(
            (p for p in self.place_list if self.intersections[p.node].zone == zone),
            key=lambda p: p.name,
        )

    def connecting_segments(self, zone_a, zone_b):
        """Segments with one end in zone_a and the other end in zone_b."""
        found = []
        for s in self.segment_list:
            ends = {self.intersections[s.start].zone, self.intersections[s.end].zone}
            if ends == {zone_a, zone_b}:
                found.append(s)
        return found

    # ----- validation -----

    def validate(self):
        """Return a list of problems. An empty list means the town is valid."""
        problems = []

        # Intersections
        ids = [i.id for i in self.intersection_list]
        if len(ids) != len(set(ids)):
            problems.append("Duplicate intersection ids")

        # Zones (neighbourhoods): if any intersection has one, all must
        zoned = [i for i in self.intersection_list if i.zone]
        if zoned and len(zoned) != len(self.intersection_list):
            problems.append("Some intersections have no zone")

        # Segments
        seen_pairs = set()
        for s in self.segment_list:
            if s.start not in self.intersections:
                problems.append(f"Segment references unknown node '{s.start}'")
            if s.end not in self.intersections:
                problems.append(f"Segment references unknown node '{s.end}'")
            if s.start == s.end:
                problems.append(f"Segment loops back to itself at '{s.start}'")
            if not s.street.strip():
                problems.append(f"Segment {s.start}->{s.end} has no street name")
            pair = frozenset((s.start, s.end))
            if pair in seen_pairs:
                problems.append(f"Duplicate segment between '{s.start}' and '{s.end}'")
            seen_pairs.add(pair)

        # Places
        place_ids = [p.id for p in self.place_list]
        if len(place_ids) != len(set(place_ids)):
            problems.append("Duplicate place ids")
        names = [p.name for p in self.place_list]
        if len(names) != len(set(names)):
            problems.append("Duplicate place names")
        addresses = [(p.street, p.number) for p in self.place_list]
        if len(addresses) != len(set(addresses)):
            problems.append("Two places share the same address")

        nodes_used = {}
        for p in self.place_list:
            if p.node not in self.intersections:
                problems.append(f"Place '{p.name}' is at unknown node '{p.node}'")
                continue
            if p.street not in self.streets_at(p.node):
                problems.append(
                    f"Place '{p.name}' is on '{p.street}', which does not pass through '{p.node}'"
                )
            if p.node in nodes_used:
                problems.append(
                    f"Places '{nodes_used[p.node]}' and '{p.name}' share node '{p.node}'"
                )
            nodes_used[p.node] = p.name

        # Every neighbourhood should contain at least one place
        if zoned:
            zones_with_places = {
                self.intersections[p.node].zone
                for p in self.place_list
                if p.node in self.intersections
            }
            for zone in self.zones():
                if zone not in zones_with_places:
                    problems.append(f"Zone '{zone}' has no places")

        # Every place must be able to reach every other place
        place_nodes = {p.node for p in self.place_list if p.node in self.intersections}
        for node in sorted(place_nodes):
            missing = place_nodes - self.reachable_from(node)
            if missing:
                problems.append(
                    f"From '{node}' you cannot reach: {', '.join(sorted(missing))}"
                )

        return problems


def load_town(path, *, validate=True):
    """Load a town from a JSON file. Raises TownError if it is malformed or invalid."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    try:
        town = Town(
            name=data["name"],
            intersections=[Intersection(**i) for i in data["intersections"]],
            segments=[Segment(**s) for s in data["segments"]],
            places=[Place(**p) for p in data["places"]],
        )
    except (KeyError, TypeError) as error:
        raise TownError(f"Malformed town file: {error}") from error

    if validate:
        problems = town.validate()
        if problems:
            raise TownError("Invalid town:\n- " + "\n- ".join(problems))
    return town
