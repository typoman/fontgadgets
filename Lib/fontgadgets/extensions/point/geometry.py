from math import hypot, pi, isclose
from cmath import phase
from fontgadgets.decorators import (
    font_cached_method,
    font_cached_property,
    font_method,
    font_property,
)
from defcon import Point
from typing import Tuple


def _orientation(
    p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]
) -> int:
    """
    Determine the orientation of three points (p, q, r).

    The orientation indicates whether the points are collinear (0), form a
    clockwise turn (1), or form a counter-clockwise turn (-1). This is
    calculated using the cross product of vectors (q-p) and (r-q).

    Args:
        p (tuple[float, float]): First point as (x, y).
        q (tuple[float, float]): Second point as (x, y).
        r (tuple[float, float]): Third point as (x, y).

    Returns:
        int: 0 if collinear, 1 if clockwise, -1 if counter-clockwise.
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else -1


def _onSegment(
    p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]
) -> bool:
    """
    Check if point q lies on line segment pr.

    Args:
        p (tuple[float, float]): First endpoint of the segment.
        q (tuple[float, float]): Point to test.
        r (tuple[float, float]): Second endpoint of the segment.

    Returns:
        bool: True if q lies on segment pr, False otherwise.
    """
    return (
        q[0] <= max(p[0], r[0])
        and q[0] >= min(p[0], r[0])
        and (q[1] <= max(p[1], r[1]))
        and (q[1] >= min(p[1], r[1]))
    )


def _linesIntersect(
    p1: tuple[float, float],
    q1: tuple[float, float],
    p2: tuple[float, float],
    q2: tuple[float, float],
) -> bool:
    """
    Check if two line segments intersect.

    This function uses the orientation test to determine if the line segments
    (p1,q1) and (p2,q2) intersect. It handles collinear cases where endpoints
    lie on the other segment.

    Args:
        p1 (tuple[float, float]): First endpoint of the first segment.
        q1 (tuple[float, float]): Second endpoint of the first segment.
        p2 (tuple[float, float]): First endpoint of the second segment.
        q2 (tuple[float, float]): Second endpoint of the second segment.

    Returns:
        bool: True if the segments intersect (including at endpoints), False
        otherwise.
    """
    o1 = _orientation(p1, q1, p2)
    o2 = _orientation(p1, q1, q2)
    o3 = _orientation(p2, q2, p1)
    o4 = _orientation(p2, q2, q1)
    if o1 != 0 and o2 != 0 and (o3 != 0) and (o4 != 0) and (o1 != o2) and (o3 != o4):
        return True
    if o1 == 0 and _onSegment(p1, p2, q1):
        return True
    if o2 == 0 and _onSegment(p1, q2, q1):
        return True
    if o3 == 0 and _onSegment(p2, p1, q2):
        return True
    if o4 == 0 and _onSegment(p2, q1, q2):
        return True
    return False


def getNumberOfLineSegmentIntersections(
    line: tuple[tuple[float, float], tuple[float, float]],
    segments: list[tuple[float, float]],
) -> int:
    """
    Count how many times a line segment intersects with a closed polygon.

    The line segment is defined by two (x, y) coordinate tuples. The polygon is
    defined by a list of (x, y) coordinate tuples representing vertices in
    order (closed polygon). Returns the number of intersection points, excluding
    intersections at polygon vertices that coincide with line endpoints.

    Args:
        line (tuple[tuple[float, float], tuple[float, float]]): A tuple of two
            (x, y) coordinate tuples defining the line segment.
        segments (list[tuple[float, float]]): List of (x, y) coordinate tuples
            defining a closed polygon's vertices in order.

    Returns:
        int: Number of intersection points between the line segment and polygon
        edges.
    """
    if not segments:
        return 0
    p1, q1 = (line[0], line[1])
    num_intersections = 0
    count = len(segments)
    for i in range(count):
        p2 = segments[i]
        q2 = segments[(i + 1) % count]
        if _linesIntersect(p1, q1, p2, q2):
            is_at_q2 = (
                abs(q2[0] - p1[0]) < 1e-09
                and abs(q2[1] - p1[1]) < 1e-09
                or (abs(q2[0] - q1[0]) < 1e-09 and abs(q2[1] - q1[1]) < 1e-09)
            )
            if is_at_q2:
                continue
            num_intersections += 1
    return num_intersections


def getLinesIntersectionPoint(
    p1: complex, p2: complex, p3: complex, p4: complex
) -> complex | None:
    """
    Find the intersection point of two line segments defined by complex numbers.

    Both input lines are defined by their endpoints as complex numbers (x + yj).
    Returns the intersection point as a complex number if the line segments
    intersect within their bounds, otherwise returns None.

    Args:
        p1 (complex): First endpoint of the first line segment.
        p2 (complex): Second endpoint of the first line segment.
        p3 (complex): First endpoint of the second line segment.
        p4 (complex): Second endpoint of the second line segment.

    Returns:
        complex | None: The intersection point as complex number if segments
        intersect within bounds, otherwise None.
    """
    d1 = p2 - p1
    d2 = p4 - p3
    det = (d1.conjugate() * d2).imag
    if det == 0:
        return None
    d3 = p1 - p3
    ua = (d2.conjugate() * d3).imag / det
    ub = (d1.conjugate() * d3).imag / det
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return p1 + ua * d1
    return None


def distance(p1: Point, p2: Point):
    """
    Calculate the Euclidean distance between two `defcon.Point` objects.

    Args:
        p1 (Point): The first point.
        p2 (Point): The second point.

    Returns:
        float: The Euclidean distance between p1 and p2.
    """
    return hypot(p1.x - p2.x, p1.y - p2.y)


ON_CURVE = {"curve", "line"}


def distanceSquared(p1: Point, p2: Point) -> float:
    """
    Calculate the squared Euclidean distance between two `defcon.Point` objects.
    Useful for comparing distances without the overhead of square root.

    Args:
        p1 (Point): The first point.
        p2 (Point): The second point.

    Returns:
        float: The squared Euclidean distance.
    """
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return dx * dx + dy * dy


@font_cached_property("Contour.PointsChanged", "Contour.WindingDirectionChanged")
def _contourFlatArea(contour):
    """
    Calculate the approximate signed area of a contour using the shoelace formula to
    find its widning direction (clockwise or counter-clockwise).

    Args:
        contour (Contour): The contour object containing points to analyze.

    Returns:
        float: The signed area of the contour. Positive values indicate
        clockwise winding, negative values indicate counter-clockwise winding.
    """
    on_curve_points = [p for p in contour if p.segmentType in ON_CURVE]
    area_sum = 0
    num_on_curve = len(on_curve_points)
    for j in range(num_on_curve):
        p1 = on_curve_points[j]
        p2 = on_curve_points[(j + 1) % num_on_curve]
        area_sum += (p2.x - p1.x) * (p2.y + p1.y)
    return area_sum


def angleDirection(p1: Tuple[float, float], p2: Tuple[float, float]) -> complex:
    """
    Calculate the normalized direction vector between two points.

    Computes the unit vector pointing from p3 to p1. If the points are
    identical (distance is zero), it returns a zero complex number.

    Args:
        p1 (Tuple[float, float]): The first point as (x, y) coordinates.
        p2 (Tuple[float, float]): The second point as (x, y) coordinates.

    Returns:
        complex: A complex number representing the normalized direction
        vector from p2 to p1, or complex(0, 0) if the points coincide.
    """
    delta_x = p1[0] - p2[0]
    delta_y = p1[1] - p2[1]
    dist = hypot(delta_x, delta_y)
    if dist == 0:
        return complex(0, 0)
    return complex(delta_x, delta_y) / dist


TANGENT_TWIST_TOLLERANCE = pi * 1.2


# TODO:
# - in the first loop of init, check if sum of two non negative consecutive
# turns becomes less than pi, then add them as the the twist canidates. right
# now we're checking all the points for intersection which is too much.
class ContourVectors:
    """
    A container for precomputed geometric vectors and properties of a contour.

    This class calculates and stores various geometric properties for each
    on-curve point in a contour, including tangents, normals, turning angles,
    and segment data.

    Attributes:
        tangents (dict): Mapping from point IDs to (tangent_before, tangent_after)
            complex vectors.
        deltas (dict): Mapping from point IDs to complex products of consecutive
            tangents.
        normals (dict): Mapping from point IDs to normalized bisector vectors,
            scaled by contour diagonal.
        turns (dict): Mapping from point IDs to turning angles in radians.
        oncurves (dict): Mapping from point IDs to on-curve point objects.
        indices (dict): Mapping from point IDs to contour indices.
        segments (list): List of (x, y) coordinates for on-curve points.
        bounds (tuple): (min_x, min_y, max_x, max_y) bounding box of on-curve
            points.
        cpoints (dict): Mapping from point IDs to complex coordinates.
    """

    __slots__ = (
        "_contour",
        "_reversed",
        "tangents",
        "deltas",
        "normals",
        "turns",
        "oncurves",
        "indices",
        "segments",
        "bounds",
        "cpoints",
        "twists"
    )

    def __init__(self, contour):
        self._contour = contour
        self.tangents = {}
        self.deltas = {}
        self.normals = {}
        self.turns = {}  # stored in radians
        self.oncurves = {}
        self.indices = {}
        self.segments = []
        self.bounds = None
        self.cpoints = {}
        self._reversed = False
        self.twists = {}
        pts_list = list(self._contour)
        count = len(pts_list)
        for idx, p_curr in enumerate(pts_list):
            if p_curr.segmentType not in ON_CURVE:
                continue
            self.segments.append((p_curr.x, p_curr.y))
            p_prev = pts_list[idx - 1]
            p_next = pts_list[(idx + 1) % count]
            i = id(p_curr)
            self.cpoints[i] = complex(p_curr.x, p_curr.y)
            self.oncurves[i] = p_curr
            self.indices[i] = idx
            tangentBefore = angleDirection((p_curr.x, p_curr.y), (p_prev.x, p_prev.y))
            tangentAfter = angleDirection((p_curr.x, p_curr.y), (p_next.x, p_next.y))
            self.tangents[i] = (tangentBefore, tangentAfter)
            v_in = tangentBefore
            v_out = -tangentAfter
            bisector_vec = v_in + v_out
            if abs(bisector_vec) < 1e-06:
                bisector_vec = v_in
            self.normals[i] = bisector_vec / abs(bisector_vec) * complex(0, 1)
            self.deltas[i] = tangentBefore * tangentAfter.conjugate()
            self.turns[i] = phase(self.deltas[i])

        if self.segments:
            xs, ys = zip(*self.segments)
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            self.bounds = (min_x, min_y, max_x, max_y)
            diagonal = hypot(min_x - max_x, min_y - max_y)
            if diagonal > 0:
                for key in self.normals:
                    self.normals[key] *= diagonal
        else:
            return
        # return

        # HACK: in a case of p1, p2, p3, p4, if the segments of (p1, p2) and
        # (p3, p4) intersect, or in other words when segments are twisted, swap
        # the direction of shared tangents of p2 and p3 and recalculate the
        # turn and normals. this makes them similar to a case that they are not
        # twisted. i do this because in some cases of overlap segments, find
        # twins was failing and this hack fixed it.
        pts_list = [p for p in pts_list if p.segmentType in ON_CURVE]
        count = len(pts_list)
        j = 0
        # OPTIMIZE:
        # intgrate this inside the first loop, so the calculation
        # doesn't happen twice.
        while j < count:
            p1 = pts_list[j % count]
            p2 = pts_list[(j + 1) % count]
            p3 = pts_list[(j + 2) % count]
            p4 = pts_list[(j + 3) % count]
            c1 = complex(p1.x, p1.y)
            c2 = complex(p2.x, p2.y)
            c3 = complex(p3.x, p3.y)
            c4 = complex(p4.x, p4.y)
            # NOTE:
            # i tried to use this method instead of checking intersection
            # to optimzize but it broke some tests: instead use some of the turns
            # and if they're almost equal to pi then it's a twist. in that case
            # both turns should be positive. This broke the simple rect test.
            if getLinesIntersectionPoint(c1, c2, c3, c4) is not None:
                # BUG:
                # now we only check if segments intersect, however, on curves
                # it wokrs most of the time but not always.
                i2 = id(p2)
                i3 = id(p3)
                self.twists[i2] = i3
                self.twists[i3] = i2
                tBeforeI2, tAfterI2 = self.tangents[i2]
                tBeforeI3, tAfterI3 = self.tangents[i3]
                self.tangents[i2] = tBeforeI2, tBeforeI3
                self.tangents[i3] = tAfterI2, tAfterI3
                self.deltas[i2] = tBeforeI2 * tBeforeI3.conjugate()
                self.deltas[i3] = tAfterI2 * tAfterI3.conjugate()
                self.turns[i2] = phase(self.deltas[i2])
                self.turns[i3] = phase(self.deltas[i3])
                self.normals[i2] = -self.normals[i2] * diagonal
                self.normals[i3] = -self.normals[i3] * diagonal
                for i, (tb, ta) in [(i2, self.tangents[i2]), (i3, self.tangents[i3])]:
                    v_in = tb
                    v_out = -ta
                    bisector_vec = v_in + v_out
                    if abs(bisector_vec) < 1e-06:
                        bisector_vec = v_in
                    self.normals[i] = bisector_vec / abs(bisector_vec) * complex(0, 1)
                    if diagonal > 0:
                        self.normals[i] *= diagonal

                # jump over p1, p2, p3. the next sequence starts at p4.
                j += 3
            else:
                j += 1

    def update(self):
        if self._reversed == self._contour.cluster.reversed:
            return
        else:
            self.segments.reverse()
            for i, (t_before, t_after) in self.tangents.items():
                self.tangents[i] = (t_after, t_before)
                self.normals[i] = -self.normals[i]
                self.deltas[i] = self.deltas[i].conjugate()
            self._reversed = self._contour.cluster.reversed


@font_cached_property("Contour.PointsChanged", "Contour.WindingDirectionChanged")
def _vectors(contour):
    return ContourVectors(contour)


@font_property
def vectors(contour):
    contour._vectors.update()
    return contour._vectors


@font_property
def cluster(contour):
    """
    clusters are made of contours that contain other contours
    """
    contour.glyph._updateContoursClusters()
    return contour._cluster


class ContourCluster:
    __slots__ = ("contour", "parent", "subClusters", "root", "reversed")

    def __init__(self, contour, parent=None):
        self.contour = contour
        contour._cluster = self
        self.parent = parent
        self.subClusters = []
        if parent is not None:
            self.root = parent.root
        else:
            self.root = contour
        self.reversed = self.root._contourFlatArea > 0


def _placeContourInCluster(nodes, contour, parent=None):
    # iterate through existing nodes at this level to find a parent
    for node in nodes:
        # check if the current contour is inside this node's contour
        if node.contour.contourInside(contour):
            # found match, recurse into subclusters, passing current node as parent
            _placeContourInCluster(node.subClusters, contour, parent=node)
            return

    # if loop completes without return, contour is not inside any existing node
    # it becomes a new sibling at this level
    nodes.append(ContourCluster(contour, parent))


@font_cached_method("Contour.PointsChanged", "Contour.WindingDirectionChanged")
def _updateContoursClusters(glyph):
    contours = sorted(glyph, key=lambda c: -abs(c._contourFlatArea))
    root_clusters = []
    for contour in contours:
        _placeContourInCluster(root_clusters, contour)
    glyph._contourClusters = root_clusters


@font_property
def contourClusters(glyph):
    """
    clusters are made of contours that contain other contours
    """
    glyph._updateContoursClusters()
    return glyph._contourClusters


COLLINEAR_TOLLERANCE = 0.05 * pi
TANGENT_TOLLERANCE = 0.15 * pi
CORNER_TOLLERANCE = 0.25 * pi
PARALLEL_TOLLERANCE = 1.85 * pi

# TODO:
# From old todo list but i'm not sure to implement them yet:
# - if any line intersects with any other line (including the lines between twins),
#  discard it. also discard it if it's a extreme twin and is crossing another line.
#  this could be wrong as it discards one of the pairs on the circle.
# - keep the twins from other glyphs on the font level so we can have an
#  average twin size and then dicard the ones which are bigger/smaller than its
#  half. This can have an issue, where we could drop the ink traps.


class GlyphTwinPointsFinder:
    """
    A finder for twin points (matching points) within a glyph. A twin point is
    a point in the glyph that geometrically corresponds to another point,
    typically across filled areas and holes, based on tangent compatibility,
    turn angles, and normal. Here is the logic in summary:

    Maps points to host contours. Determines search scope via winding
    direction: filled areas target child holes or self; holes target parent.

    Inside the search, it filters candidates by tangent alignment and
    classifies them based on geometry: segments with parallel tangents,
    which usually happen on extreme points on curves, require the twin point to
    have its normal vector pointing towards the reference point; if one of the
    tangents of the two points are similar and the other tangents are pointing
    in opposite directions, then it could be a match; if normals intersect
    within the bounding box and points are close to each other, it could also
    be a match.

    Before selecting the final match, it sortes the candiates based on distance
    and checks if the line drawn between the match doesn't cross any segment 
    on the contour.

    Args:
        glyph: The glyph object to analyze for twin points.
    """

    def __init__(self, glyph) -> None:
        self._twins = {}
        self._glyph = glyph
        self._pointContours = {}
        for contour in glyph:
            for p in contour.vectors.oncurves.values():
                self._pointContours[id(p)] = contour

    def _searchTwin(self, reference_point, candidate_vectors, intersection_contours):
        p1_id = id(reference_point)
        ref_contour = self._pointContours[p1_id]
        ref_vectors = ref_contour.vectors
        twists = ref_vectors.twists
        _abs = abs
        _isclose = isclose
        _pi = pi

        # accessing local variables is faster than accessing object properties (self.x)
        p1_normal = ref_vectors.normals[p1_id]
        p1_turn = ref_vectors.turns[p1_id]
        p1_turn_abs = _abs(p1_turn)
        p1_index = ref_vectors.indices[p1_id]
        p1_complex = ref_vectors.cpoints[p1_id]
        p1_tangentBefore, p1_tangentAfter = ref_vectors.tangents[p1_id]

        # exclude the reference point itself
        c_ids = [k for k in candidate_vectors.oncurves if k != p1_id]
        c_pts = [candidate_vectors.oncurves[k] for k in c_ids]
        c_tans = [candidate_vectors.tangents[k] for k in c_ids]
        c_turns = [candidate_vectors.turns[k] for k in c_ids]
        c_norms = [candidate_vectors.normals[k] for k in c_ids]
        c_cpts = [candidate_vectors.cpoints[k] for k in c_ids]

        # root bounds logic (kept same as your code)
        root_contour = ref_contour.cluster.root
        if root_contour.vectors.bounds:
            xMin, yMin, xMax, yMax = root_contour.vectors.bounds
        else:
            xMin, yMin, xMax, yMax = ref_vectors.bounds

        collinears = []
        corners = []
        chamfers = []

        p1TangentsAreCollinear = _isclose(
            p1_turn_abs, _pi, abs_tol=COLLINEAR_TOLLERANCE
        )
        p1TurningNegative = p1_turn < 0
        isTwisted = p1_id in twists

        for pt, (p2_tBefore, p2_tAfter), p2_turn, p2_normal, cp2, p2_id in zip(
            c_pts, c_tans, c_turns, c_norms, c_cpts, c_ids
        ):
            p2_turn_abs = _abs(p2_turn)
            # fast check: tangent compatibility
            if (
                _abs(p1_tangentBefore - p2_tAfter) < TANGENT_TOLLERANCE
                or _abs(p2_tBefore - p1_tangentAfter) < TANGENT_TOLLERANCE
            ):
                turn_sum = p1_turn_abs + p2_turn_abs

                if p1TangentsAreCollinear:
                    # tangents are almost collinear and normals are pointing at each other
                    if (
                        turn_sum > PARALLEL_TOLLERANCE
                        and (p1_normal * p2_normal.conjugate()).real < 0
                    ):
                        corners.append(pt)
                elif (p1TurningNegative or p2_turn < 0) and (
                    (p1_normal * p2_normal.conjugate()).real < 0
                ):
                    # negative (concave) trun
                    # use dot product to check if normals point towards
                    # the other point within 0.9 radians.
                    delta = cp2 - p1_complex
                    dist = _abs(delta)
                    if dist > 1e-9:
                        u = delta / dist
                        # dot product of (p1_normal . direction_to_p2) and (p2_normal . direction_to_p1)
                        if (
                            (p1_normal * u.conjugate()).real > 0.6 # cos(0.9) is approximately 0.6
                            and (p2_normal * (-u).conjugate()).real > 0.6
                        ):
                            corners.append(pt)
                elif isTwisted or p2_id in twists:
                    # a sgement in-between twisted segments is not a corner
                    continue
                elif self._normalsIntersectInBounds(
                    p1_complex,
                    cp2,
                    p1_normal,
                    p2_normal,
                    xMin,
                    xMax,
                    yMin,
                    yMax,
                ):  # it's a corner or a tip of a stroke possibly
                    if (turn_sum - _pi) < CORNER_TOLLERANCE:
                        # sum of the turns adds almost to 180 degrees
                        corners.append(pt)
                    else:
                        # chamfer at a corner is skipped
                        chamfers.append(pt)

        # prioritize candidates
        # for candids in [collinears, corners, chamfers]:
        for candids in [collinears, corners, chamfers]:
            if not candids:
                continue

            # sort by distance
            candids.sort(key=lambda p2: distanceSquared(reference_point, p2))

            for pt in candids:
                # neighbor check logic
                if ref_vectors == candidate_vectors:
                    candidate_id = id(pt)
                    # we have to look up index here, but only for valid candidates
                    candidate_index = candidate_vectors.indices[candidate_id]
                    diff = _abs(candidate_index - p1_index)
                    count = len(candidate_vectors.oncurves)
                    if diff == 1 or diff == count - 1:
                        return pt

                # intersection check
                line = (reference_point.x, reference_point.y), (pt.x, pt.y)
                intersections_found = 0
                blocked = False

                for c in intersection_contours:
                    n = getNumberOfLineSegmentIntersections(line, c.vectors.segments)
                    intersections_found += n
                    if intersections_found >= 3:
                        blocked = True
                        break

                if not blocked:
                    return pt

        return None

    def getTwinPointForPoint(self, point):
        pid = id(point)
        if pid in self._twins:
            return self._twins[pid]

        referenceContour = self._pointContours.get(pid)
        if referenceContour is None:
            return []

        node = referenceContour.cluster
        root_contour = node.root

        # determine winding directions to identify if we are in a filled area or a hole
        ref_winding = referenceContour._contourFlatArea < 0
        root_winding = root_contour._contourFlatArea < 0

        # if winding matches root, it's a filled contour. otherwise, it's a hole.
        is_filled = ref_winding == root_winding

        target_contours = []

        if is_filled:
            # if filled, look for direct children (subclusters) that are holes (opposite winding)
            candidates = [
                child.contour
                for child in node.subClusters
                if (child.contour._contourFlatArea < 0) != ref_winding
            ]

            if candidates:
                target_contours = candidates
            else:
                # if no such children exist, search the contour itself
                target_contours = [referenceContour]
        else:
            # if hole, look for the immediate parent which should be filled (opposite winding)
            parent_node = node.parent
            if parent_node:
                parent_contour = parent_node.contour
                if (parent_contour._contourFlatArea < 0) != ref_winding:
                    target_contours = [parent_contour]

        # define intersection obstacles:
        # - the contour itself and its siblings (same nested level)
        # - the target contour(s)
        if node.parent:
            siblings = [n.contour for n in node.parent.subClusters]
        else:
            # if no parent, we are at the root level. siblings are other root clusters.
            siblings = [n.contour for n in self._glyph.contourClusters]

        found_candidates = []

        for target_contour in target_contours:
            # combine siblings and target for intersection checking.
            # use set to avoid duplication if target is self or a sibling.
            obstacles = list(set(siblings + [target_contour]))
            match = self._searchTwin(point, target_contour.vectors, obstacles)
            if match:
                found_candidates.append(match)

        targetPoint = None
        if found_candidates:
            # if multiple candidates (e.g. multiple holes), pick the closest one
            found_candidates.sort(key=lambda p: distanceSquared(point, p))
            targetPoint = found_candidates[0]
        elif is_filled:
            targetPoint = self._searchTwin(point, referenceContour.vectors, siblings)

        if targetPoint:
            self._twins.setdefault(pid, []).append(targetPoint)
        return self._twins.get(pid, [])

    def _normalsIntersectInBounds(
        self, cp1, cp2, p1_normal, p2_normal, xMin, xMax, yMin, yMax
    ):
        intersection = getLinesIntersectionPoint(
            cp1, cp1 + p1_normal, cp2, cp2 + p2_normal
        )
        if intersection is not None:
            if xMin <= intersection.real <= xMax and yMin <= intersection.imag <= yMax:
                return True
        return False


@font_cached_property("Contour.PointsChanged", "Contour.WindingDirectionChanged")
def _twinFinder(glyph):
    return GlyphTwinPointsFinder(glyph)


@font_method
def getTwinPointForPoint(glyph, point):
    tf = glyph._twinFinder
    return tf.getTwinPointForPoint(point)
