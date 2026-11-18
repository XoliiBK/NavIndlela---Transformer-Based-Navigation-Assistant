from pathlib import Path

import pytest

from src.navigation.graph import Intersection, Place, Segment, Town, TownError, load_town

TOWN_PATH = Path(__file__).resolve().parents[1] / "data" / "town_graph" / "town.json"


@pytest.fixture(scope="module")
def town():
    return load_town(TOWN_PATH)


def tiny_town(segments=None, places=None):
    """A two-node town used to build deliberately broken examples."""
    intersections = [Intersection("a", 0, 0), Intersection("b", 100, 0)]
    if segments is None:
        segments = [Segment("a", "b", "First St")]
    if places is None:
        places = [
            Place("shop", "Shop", "First St", 1, "a"),
            Place("cafe", "Cafe", "First St", 2, "b"),
        ]
    return Town("Tiny", intersections, segments, places)


# ----- the real town -----

def test_real_town_is_valid(town):
    assert town.validate() == []


def test_real_town_size(town):
    assert len(town.intersections) == 20
    assert len(town.places) == 18


def test_one_way_street_only_goes_one_direction(town):
    # Church Rd is one-way heading east
    assert "church-market" in [n for n, _ in town.outgoing("church-main")]
    assert "church-main" not in [n for n, _ in town.outgoing("church-market")]


def test_dead_end_exists(town):
    assert town.dead_ends() == ["mill-main"]


def test_every_place_is_reachable_from_every_other(town):
    place_nodes = {p.node for p in town.places.values()}
    for node in place_nodes:
        assert place_nodes <= town.reachable_from(node)


def test_places_on_street_are_sorted_by_number(town):
    numbers = [p.number for p in town.places_on_street("Hill St")]
    assert numbers == sorted(numbers)
    assert len(numbers) > 0


# ----- deliberately broken towns -----

def test_tiny_town_is_valid():
    assert tiny_town().validate() == []


def test_unknown_node_is_reported():
    town = tiny_town(segments=[Segment("a", "zzz", "First St")])
    assert any("unknown node 'zzz'" in p for p in town.validate())


def test_place_on_wrong_street_is_reported():
    places = [
        Place("shop", "Shop", "Second St", 1, "a"),
        Place("cafe", "Cafe", "First St", 2, "b"),
    ]
    problems = tiny_town(places=places).validate()
    assert any("does not pass through" in p for p in problems)


def test_duplicate_address_is_reported():
    places = [
        Place("shop", "Shop", "First St", 1, "a"),
        Place("cafe", "Cafe", "First St", 1, "b"),
    ]
    assert any("same address" in p for p in tiny_town(places=places).validate())


def test_two_places_on_one_node_is_reported():
    places = [
        Place("shop", "Shop", "First St", 1, "a"),
        Place("cafe", "Cafe", "First St", 2, "a"),
    ]
    assert any("share node" in p for p in tiny_town(places=places).validate())


def test_one_way_trap_is_reported():
    # You can go a -> b but never back: the town is not fully connected
    town = tiny_town(segments=[Segment("a", "b", "First St", one_way=True)])
    assert any("cannot reach" in p for p in town.validate())


def test_load_town_raises_on_invalid_file(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"name": "x", "intersections": [], "segments": [], "places": [{"id": "p"}]}')
    with pytest.raises(TownError):
        load_town(bad)
