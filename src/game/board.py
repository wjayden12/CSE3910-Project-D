from src.game.tiles import build_tiles
from src.game import structures
from src.game import constants


def edge(a, b):
    return (a, b) if a < b else (b, a)


class Board:
    TILE_KEYS_BY_ROW = [
        [0, 1, 2],
        [11, 12, 13, 3],
        [10, 17, 18, 14, 4],
        [9, 16, 15, 5],
        [8, 7, 6],
    ]

    def __init__(self):
        self.rows = build_tiles()

        self.tiles = [t for row in self.rows for t in row]

        self.roads = []
        self.settlements = []
        self.cities = []

        # ----- graph -----
        self.vertex_neighbors = {v: [] for v in constants.SettlementPositions}
        for a, b in constants.roads:
            self.vertex_neighbors[a].append(b)
            self.vertex_neighbors[b].append(a)

        self.valid_edges = {edge(a, b): True for a, b in constants.roads}

        # ----- tile lookup -----
        self.tile_key_to_tile = {}
        for r, row in enumerate(self.rows):
            for c, tile in enumerate(row):
                self.tile_key_to_tile[self.TILE_KEYS_BY_ROW[r][c]] = tile

        # ----- robber starts on desert -----
        self.robber_tile_key = None
        for k, tile in self.tile_key_to_tile.items():
            if tile.resource_type == "desert":
                self.robber_tile_key = k
                break

    # structure helpers

    def get_road(self, location):
        e = edge(location[0], location[1])
        for r in self.roads:
            if r.location == e:
                return r
        return None

    def get_structure(self, vertex):
        for s in self.settlements:
            if s.location == vertex:
                return s
        for c in self.cities:
            if c.location == vertex:
                return c
        return None

    def get_settlement_vertices(self, player_id):
        verts = []
        for s in self.settlements:
            if s.owner_id == player_id:
                verts.append(s.location)
        for c in self.cities:
            if c.owner_id == player_id:
                verts.append(c.location)
        return verts

    def get_road_edges(self, player_id):
        return [r.location for r in self.roads if r.owner_id == player_id]

    # placement rules

    def can_place_settlement(self, vertex):
        if vertex not in constants.SettlementPositions:
            return False
        if self.get_structure(vertex) is not None:
            return False
        for n in self.vertex_neighbors[vertex]:
            if self.get_structure(n) is not None:
                return False
        return True

    def can_place_settlement_connected(self, vertex, player_id):
        if not self.can_place_settlement(vertex):
            return False
        for r in self.roads:
            if r.owner_id == player_id and vertex in r.location:
                return True
        return False

    def add_settlement(self, vertex, player_id):
        """
        Use this for setup phase (no road-connection requirement).
        """
        if not self.can_place_settlement(vertex):
            return False
        self.settlements.append(structures.Settlement(vertex, player_id))
        return True

    def add_settlement_connected(self, vertex, player_id):
        """
        Use this during normal play (must connect to own road).
        """
        if not self.can_place_settlement_connected(vertex, player_id):
            return False
        self.settlements.append(structures.Settlement(vertex, player_id))
        return True

    def can_place_road(self, location, player_id, must_connect_to=None):
        e = edge(location[0], location[1])
        if e not in self.valid_edges:
            return False
        if self.get_road(e) is not None:
            return False

        a, b = e

        # setup rule
        if must_connect_to is not None:
            return a == must_connect_to or b == must_connect_to

        # normal rule
        own_vertices = self.get_settlement_vertices(player_id)
        if a in own_vertices or b in own_vertices:
            return True

        for v in (a, b):
            if self.is_vertex_blocked(v, player_id):
                continue
            for ra, rb in self.get_road_edges(player_id):
                if v == ra or v == rb:
                    return True

        return False

    def add_road(self, location, player_id, must_connect_to=None):
        if not self.can_place_road(location, player_id, must_connect_to):
            return False
        self.roads.append(structures.Road(edge(location[0], location[1]), player_id))
        return True

    def is_vertex_blocked(self, vertex, player_id):
        st = self.get_structure(vertex)
        return st is not None and st.owner_id != player_id

    # city upgrades

    def can_upgrade_city(self, vertex, player_id):
        for s in self.settlements:
            if s.location == vertex:
                return s.owner_id == player_id
        return False

    def upgrade_city(self, vertex, player_id):
        if not self.can_upgrade_city(vertex, player_id):
            return False
        self.settlements = [s for s in self.settlements if s.location != vertex]
        self.cities.append(structures.City(vertex, player_id))
        return True

    # resource logic

    def vertices_adjacent_tiles(self, vertex):
        return [
            tk for tk, verts in constants.TileSettlementMap.items()
            if vertex in verts
        ]

    def resource_to_player(self, tile_res):
        return {
            "grain": "wheat",
            "lumber": "wood",
            "wool": "sheep",
        }.get(tile_res, tile_res)

    def resources_for_settlement(self, vertex):
        gained = []
        for tk in self.vertices_adjacent_tiles(vertex):
            tile = self.tile_key_to_tile.get(tk)
            if not tile or tile.resource_type == "desert":
                continue
            gained.append(self.resource_to_player(tile.resource_type))
        return gained

    def distribute_resources(self, roll_value, players):
        players_by_id = {p.player_id: p for p in players}

        # settlements
        for s in self.settlements:
            owner = players_by_id.get(s.owner_id)
            if not owner:
                continue
            for tk in self.vertices_adjacent_tiles(s.location):
                if tk == self.robber_tile_key:
                    continue
                tile = self.tile_key_to_tile[tk]
                if tile.count == roll_value and tile.resource_type != "desert":
                    r = self.resource_to_player(tile.resource_type)
                    owner.resources[r] = owner.resources.get(r, 0) + 1

        # cities (2x)
        for c in self.cities:
            owner = players_by_id.get(c.owner_id)
            if not owner:
                continue
            for tk in self.vertices_adjacent_tiles(c.location):
                if tk == self.robber_tile_key:
                    continue
                tile = self.tile_key_to_tile[tk]
                if tile.count == roll_value and tile.resource_type != "desert":
                    r = self.resource_to_player(tile.resource_type)
                    owner.resources[r] = owner.resources.get(r, 0) + 2

    # robber + longest road

    def players_adjacent_to_tile(self, tile_key):
        players = set()
        for v in constants.TileSettlementMap.get(tile_key, []):
            st = self.get_structure(v)
            if st:
                players.add(st.owner_id)
        return list(players)

    def longest_road_length(self, player_id):
        roads = [r.location for r in self.roads if r.owner_id == player_id]
        graph = {}

        for a, b in roads:
            graph.setdefault(a, []).append(b)
            graph.setdefault(b, []).append(a)

        def dfs(v, used):
            best = 0
            for nxt in graph.get(v, []):
                # break at opponent settlements
                if self.is_vertex_blocked(nxt, player_id):
                    continue
                e = edge(v, nxt)
                if e in used:
                    continue
                used.add(e)
                best = max(best, 1 + dfs(nxt, used))
                used.remove(e)
            return best

        return max((dfs(v, set()) for v in graph), default=0)

    # victory points

    def victory_points(self, player_id):
        return (
            sum(1 for s in self.settlements if s.owner_id == player_id)
            + sum(2 for c in self.cities if c.owner_id == player_id)
        )
