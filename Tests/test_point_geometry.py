import pytest
import defcon
from pathlib import Path
from fontgadgets.extensions.point.geometry import getCounterPoints

GLYPH_NAMES = [
    "rect",
    "cricle",
    "H",
    "circle-hole",
    "eight",
    "double-loop",
    "arrow",
    "arrow2",
    "broad-nib-vertical-stroke-with-chamfer",
    "angled-extremes",
    "nested-clusters",
    "nested-clusters-2",
    "nested-rect",
    "curve-overlap",
]

EXPECTED_CLUSTERS = {
    "rect": [{"contourIndex": 0, "subClusters": []}],
    "cricle": [{"contourIndex": 0, "subClusters": []}],
    "H": [{"contourIndex": 0, "subClusters": []}],
    "circle-hole": [
        {"contourIndex": 0, "subClusters": [{"contourIndex": 1, "subClusters": []}]}
    ],
    "eight": [
        {
            "contourIndex": 0,
            "subClusters": [
                {"contourIndex": 1, "subClusters": []},
                {"contourIndex": 2, "subClusters": []},
            ],
        }
    ],
    "double-loop": [
        {
            "contourIndex": 2,
            "subClusters": [
                {"contourIndex": 0, "subClusters": []},
                {"contourIndex": 1, "subClusters": []},
            ],
        }
    ],
    "arrow": [{"contourIndex": 0, "subClusters": []}],
    "arrow2": [{"contourIndex": 0, "subClusters": []}],
    "broad-nib-vertical-stroke-with-chamfer": [{"contourIndex": 0, "subClusters": []}],
    "angled-extremes": [{"contourIndex": 0, "subClusters": []}],
    "nested-clusters": [
        {
            "contourIndex": 0,
            "subClusters": [
                {
                    "contourIndex": 1,
                    "subClusters": [
                        {
                            "contourIndex": 2,
                            "subClusters": [{"contourIndex": 3, "subClusters": []}],
                        }
                    ],
                }
            ],
        }
    ],
    "nested-clusters-2": [
        {
            "contourIndex": 0,
            "subClusters": [
                {
                    "contourIndex": 1,
                    "subClusters": [{"contourIndex": 2, "subClusters": []}],
                }
            ],
        }
    ],
    "nested-rect": [
        {"contourIndex": 0, "subClusters": [{"contourIndex": 1, "subClusters": []}]}
    ],
    "curve-overlap": [ { 'contourIndex': 0, 'subClusters': [], } ],
}

EXPECTED_COUNTERS = {
    "rect": {(0, 0): [(0, 1)], (0, 1): [(0, 0)], (0, 2): [(0, 3)], (0, 3): [(0, 2)]},
    "curve-overlap": {
        (0, 0): [
            (
                0,
                15,
            ),
        ],
        (0, 3): [
            (
                0,
                12,
            ),
        ],
        (0, 4): [
            (
                0,
                11,
            ),
        ],
        (0, 7): [
            (
                0,
                8,
            ),
        ],
        (0, 8): [
            (
                0,
                7,
            ),
        ],
        (0, 11): [
            (
                0,
                4,
            ),
        ],
        (0, 12): [
            (
                0,
                3,
            ),
        ],
        (0, 15): [
            (
                0,
                0,
            ),
        ],
    },
    "cricle": {(0, 0): [(0, 6)], (0, 3): [(0, 9)], (0, 6): [(0, 0)], (0, 9): [(0, 3)]},
    "H": {
        (0, 0): [(0, 1)],
        (0, 1): [(0, 0)],
        (0, 2): [(0, 9)],
        (0, 3): [(0, 8)],
        (0, 4): [(0, 5)],
        (0, 5): [(0, 4)],
        (0, 6): [(0, 7)],
        (0, 7): [(0, 6)],
        (0, 8): [(0, 3)],
        (0, 9): [(0, 2)],
        (0, 10): [(0, 11)],
        (0, 11): [(0, 10)],
    },
    "circle-hole": {
        (0, 0): [(1, 0)],
        (0, 3): [(1, 9)],
        (0, 6): [(1, 6)],
        (0, 9): [(1, 3)],
        (1, 0): [(0, 0)],
        (1, 3): [(0, 9)],
        (1, 6): [(0, 6)],
        (1, 9): [(0, 3)],
    },
    "eight": {
        (0, 0): [(2, 0)],
        (0, 3): [(2, 9)],
        (0, 9): [(1, 9)],
        (0, 12): [(1, 6)],
        (0, 15): [(1, 3)],
        (0, 21): [(2, 3)],
        (1, 3): [(0, 15)],
        (1, 6): [(0, 12)],
        (1, 9): [(0, 9)],
        (2, 0): [(0, 0)],
        (2, 3): [(0, 21)],
        (2, 9): [(0, 3)],
    },
    "double-loop": {
        (0, 3): [(2, 9)],
        (0, 6): [(2, 6)],
        (0, 9): [(2, 3)],
        (1, 0): [(2, 21)],
        (1, 3): [(2, 18)],
        (1, 9): [(2, 24)],
        (2, 0): [(0, 0)],
        (2, 3): [(0, 9)],
        (2, 6): [(0, 6)],
        (2, 9): [(0, 3)],
        (2, 12): [(2, 27)],
        (2, 15): [(1, 6)],
        (2, 18): [(1, 3)],
        (2, 21): [(1, 0)],
        (2, 24): [(1, 9)],
        (2, 27): [(2, 12)],
    },
    "arrow": {
        (0, 0): [(0, 1)],
        (0, 1): [(0, 0)],
        (0, 2): [(0, 5)],
        (0, 3): [(0, 4)],
        (0, 4): [(0, 3)],
        (0, 5): [(0, 2)],
        (0, 6): [(0, 2)],
    },
    "arrow2": {
        (0, 0): [(0, 1)],
        (0, 1): [(0, 0)],
        (0, 2): [(0, 5)],
        (0, 3): [(0, 4)],
        (0, 4): [(0, 3)],
        (0, 5): [(0, 2)],
        (0, 6): [(0, 2)],
    },
    "nested-rect": {
        (0, 0): [(1, 0)],
        (0, 1): [(1, 3)],
        (0, 2): [(1, 2)],
        (0, 3): [(1, 1)],
        (1, 0): [(0, 0)],
        (1, 1): [(0, 3)],
        (1, 2): [(0, 2)],
        (1, 3): [(0, 1)],
    },
    "broad-nib-vertical-stroke-with-chamfer": {
        (0, 0): [(0, 1)],
        (0, 1): [(0, 0)],
        (0, 2): [(0, 4)],
        (0, 4): [(0, 2)],
    },
    "angled-extremes": {
        (0, 0): [(0, 9)],
        (0, 1): [(0, 8)],
        (0, 4): [(0, 5)],
        (0, 5): [(0, 4)],
        (0, 8): [(0, 1)],
        (0, 9): [(0, 0)],
    },
    "nested-clusters": {
        (0, 0): [(1, 0)],
        (0, 3): [(1, 9)],
        (0, 6): [(1, 6)],
        (0, 9): [(1, 3)],
        (1, 0): [(0, 0)],
        (1, 3): [(0, 9)],
        (1, 6): [(0, 6)],
        (1, 9): [(0, 3)],
        (2, 0): [(3, 0)],
        (2, 3): [(3, 9)],
        (2, 6): [(3, 6)],
        (2, 9): [(3, 3)],
        (3, 0): [(2, 0)],
        (3, 3): [(2, 9)],
        (3, 6): [(2, 6)],
        (3, 9): [(2, 3)],
    },
    "nested-clusters-2": {
        (0, 0): [(1, 0)],
        (0, 3): [(1, 9)],
        (0, 6): [(1, 6)],
        (0, 9): [(1, 3)],
        (1, 0): [(0, 0)],
        (1, 3): [(0, 9)],
        (1, 6): [(0, 6)],
        (1, 9): [(0, 3)],
        (2, 0): [(2, 25)],
        (2, 3): [(2, 22)],
        (2, 6): [(2, 19)],
        (2, 9): [(2, 16)],
        (2, 12): [(2, 13)],
        (2, 13): [(2, 12)],
        (2, 16): [(2, 9)],
        (2, 19): [(2, 6)],
        (2, 22): [(2, 3)],
        (2, 25): [(2, 0)],
    },
}


@pytest.fixture(scope="session")
def geometry_test_font():
    font_path = Path(__file__).parent / "data" / "geometry-test.ufo"
    if not font_path.exists():
        pytest.fail(f"Test font not found at: {font_path}")
    return defcon.Font(font_path)


def _serialize_clusters(clusters, glyph):
    result = []
    for cluster in clusters:
        try:
            contour_index = glyph.contourIndex(cluster.contour)
        except ValueError:
            contour_index = -1
        structure = {
            "contourIndex": contour_index,
            "subClusters": _serialize_clusters(cluster.subClusters, glyph),
        }
        result.append(structure)
    return result


@pytest.mark.parametrize("glyph_name", GLYPH_NAMES)
def test_contour_clusters_structure(geometry_test_font, glyph_name):
    if glyph_name not in geometry_test_font:
        pytest.fail(f"Glyph '{glyph_name}' not found in the test font.")
    glyph = geometry_test_font[glyph_name]
    clusters = glyph.contourClusters
    actual_structure = _serialize_clusters(clusters, glyph)
    expected_structure = EXPECTED_CLUSTERS[glyph_name]
    assert actual_structure == expected_structure


@pytest.mark.parametrize("glyph_name", GLYPH_NAMES)
def test_get_counter_point_for_point(geometry_test_font, glyph_name):
    if glyph_name not in geometry_test_font:
        pytest.fail(f"Glyph '{glyph_name}' not found in the test font.")
    glyph = geometry_test_font[glyph_name]
    point_map = {}
    for c_idx, contour in enumerate(glyph):
        for p_idx, point in enumerate(contour):
            point_map[id(point)] = (c_idx, p_idx)
    actual_counters = {}
    for c_idx, contour in enumerate(glyph):
        for p_idx, point in enumerate(contour):
            counterPoints = getCounterPoints(glyph, point)
            if counterPoints:
                counter_ids = []
                for counter in counterPoints:
                    if id(counter) in point_map:
                        counter_ids.append(point_map[id(counter)])
                if counter_ids:
                    actual_counters[c_idx, p_idx] = sorted(counter_ids)
    expected = EXPECTED_COUNTERS[glyph_name]
    assert actual_counters == expected
