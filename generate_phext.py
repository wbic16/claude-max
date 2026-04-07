#!/usr/bin/env python3
"""Generate uml6d.phext — the complete 6D UML system spec for phext-lattice + uml6d."""

# Phext delimiters
SC = chr(0x17)  # scroll break
SN = chr(0x18)  # section break
CH = chr(0x19)  # chapter break
BK = chr(0x1A)  # book break
VM = chr(0x1C)  # volume break
CN = chr(0x1D)  # collection break

def scrolls(*items):   return SC.join(items)
def sections(*items):  return SN.join(items)
def chapters(*items):  return CH.join(items)
def books(*items):     return BK.join(items)

# ==========================================================================
# Module Map (Book assignments)
# Book 1: Core (coordinate_ext, index)
# Book 2: Storage (mmap)
# Book 3: Navigation (navigator, cursor)
# Book 4: Search
# Book 5: Topology (sentron, stats)
# Book 6: Editor (editor, modes)
# Book 7: UML6D
# Book 8: Undo
# Book 9: TTS
# Book 10: Web UI (phext_edit, uml6d_edit)
# ==========================================================================

# ── COLLECTION 1: META ────────────────────────────────────────────────

meta_config = """6D UML v0.1
framework: 6d-uml
phext-version: 0.3.1
generator: claude-max
system: phext-lattice + uml6d"""

meta_collection_map = """collection-map:
1: Meta
2: Requirements
3: Design
4: Source
5: Tests
6: Regressions
7: Docs
8: Whitepapers
9: Training"""

meta_dimension_map = """dimension-map:
collection: SDLC Phase
volume: Sprint/Release
book: Module
chapter: Component
section: File
scroll: Unit"""

meta_module_registry = """module-registry:
book.1: Core (coordinate_ext, index)
book.2: Storage (mmap)
book.3: Navigation (navigator, cursor)
book.4: Search
book.5: Topology (sentron, stats)
book.6: Editor (editor, modes)
book.7: UML6D (uml6d)
book.8: Undo (undo)
book.9: TTS (tts)
book.10: Web UI (phext_edit, uml6d_edit)"""

meta_deps = """dependency-map:
external:
  libphext 0.3.1: Coordinate types, delimiters, phokenize, explode/implode
  memmap2 0.9: Cross-platform memory-mapped file I/O
  rayon 1.10: Work-stealing parallelism
  serde 1 + serde_json 1: JSON serialization (web feature)
  ratatui 0.29 + crossterm 0.28: TUI rendering (tui feature)
  tempfile 3: Temporary file support
internal:
  uml6d -> index, mmap
  mmap -> index
  navigator -> coordinate_ext
  search -> index
  sentron -> index, coordinate_ext
  editor -> cursor, undo
  web_ui -> mmap, navigator, sentron, search, stats, uml6d"""

collection_1 = scrolls(meta_config, meta_collection_map, meta_dimension_map, meta_module_registry, meta_deps)

# ── COLLECTION 2: REQUIREMENTS ────────────────────────────────────────

c2_book1 = chapters(
    "R1 -- Core Engine\nThe foundation layer providing coordinate extensions and O(1) lattice indexing.\nAll other modules depend on Core for coordinate manipulation and content lookup.",
    sections(
        "R1.1 -- Coordinate Extensions\n- Hash + Eq + Ord for HashMap-based index\n- Dimension enum mapping 1-9 keys to nine phext dimensions\n- CoordinateNav trait: forward/backward in named dimension with lower-dim reset\n- Peek movement without resetting lower dims\n- Delimiter byte mapping for each dimension\n- Value get/set for any dimension with clamping",
    ),
    sections(
        "R1.2 -- Lattice Index\n- Single O(n) scan builds HashMap<Coordinate, ScrollSpan>\n- O(1) coordinate lookup thereafter\n- Sorted coordinate list for binary search navigation\n- next_populated / prev_populated jump to nearest content\n- Dimension extent queries for density analysis\n- coordinates_matching predicate filter\n- ScrollSpan stores byte offsets (start, end) for mmap integration",
    )
)

c2_book2 = chapters(
    "R1.1 -- Memory-Mapped I/O\nThe editor's I/O foundation. Memory-map phext files and build LatticeIndex over raw bytes.",
    sections(
        "R1.1.1 -- MappedLattice\n- Memory-map phext files read-only via memmap2\n- Copy-on-write overlay: HashMap<Coordinate, ScrollOverlay>\n- Three states: Modified(String), Deleted, Inserted(String)\n- Byte-perfect roundtrip reconstruction on save\n- read_scroll: check overlay first, fallback to mmap span\n- write_scroll: edits go to overlay, mmap never modified\n- save: reconstruct from mmap spans + overlay deltas, re-mmap, rebuild index\n- 4MB file = 4MB virtual address space, not heap",
    )
)

c2_book3 = chapters(
    "R1.3 -- Navigator\nThe cursor model for 9D phext navigation. The 'mind' of Lattice mode.",
    sections(
        "R1.3.1 -- Navigator\n- 9D cursor tracking current coordinate\n- Active dimension selection (1-9 keys)\n- Forward/backward movement with lower dimension reset\n- Marks stack for position bookmarks\n- History with back/forward navigation\n- next_populated / prev_populated via index binary search",
    ),
    sections(
        "R1.3.2 -- Intra-Scroll Cursor\n- Position: (line, col) 0-indexed\n- Selection: start/end with direction\n- from_offset / to_offset conversion\n- Word-boundary navigation\n- Sticky column across vertical moves\n- Bridge between Lattice mode and Edit mode",
    )
)

c2_book4 = chapters(
    "R1.4 -- Search\n- Full-text search across all scrolls\n- Returns coordinates, not byte offsets\n- Parallel via rayon for files > 512KB, serial for smaller\n- Case-insensitive by default\n- Atomic early termination at max_results\n- Context extraction (40 chars around match)\n- search_lattice_auto picks parallel vs serial"
)

c2_book5 = chapters(
    "R1.5 -- Topology\nSentron neural topology and lattice statistics.",
    sections(
        "R1.5.1 -- Sentron\n- 2x4 connections per neuron (fwd + bwd x 4 axes)\n- 5x8 neurons per sentron (40 total)\n- Manhattan distance ordering from cursor\n- 8 dims: structural (Library/Shelf/Series/Collection) + sequential (Volume/Book/Chapter/Section)\n- Scroll is the neuron center\n- Sub-millisecond rebuild",
    ),
    sections(
        "R1.6 -- Statistics\n- ScrollStats: byte_size, line_count, word_count, char_count\n- DimensionDensity: distribution of scroll counts per dimension value\n- Sparkline rendering\n- Neighborhood: populated coords near cursor\n- LatticeOverview: total scrolls, total bytes, dimension extents",
    )
)

c2_book6 = chapters(
    "R1.7-R1.9 -- Editor Framework\nPluggable editing modes. Sits between navigator and mode.",
    sections(
        "R1.7 -- Editor Mode Trait\n- Pluggable EditorMode trait\n- EditKey abstraction: code, ctrl, alt, shift\n- EditResult: Nothing | CursorMoved | TextChanged | ExitEdit | Status\n- CursorStyle: Block, Line, Underline\n- Framework-independent",
    ),
    sections(
        "R1.9 -- Vim Mode\n- Sub-modes: Normal, Insert, Visual, Command\n- Count prefix for repeat\n- Motions: h/l/j/k/w/b/e/0/$\n- Operators: d/c/y\n- Multi-key: dd, dw, yy\n- Insert: i/a/o/O\n- Command: :w, :q, :wq",
    )
)

c2_book7 = chapters(
    "R-UML6D -- 6D UML Semantic Layer\n- Map collection dimension to SDLC phases (Meta through Training)\n- 5D artifact addresses (volume.book.chapter/section.scroll)\n- Phase enum with name, short code, and color\n- ArtifactAddr extraction from full coordinates\n- Trace: walk all phases at a fixed 5D address\n- UmlContext: phase + artifact for any coordinate\n- Runtime-configurable phase assignments via Meta\n- Structural traceability: same 5D address across collections"
)

c2_book8 = chapters(
    "R1.8 -- Undo/Redo\n- Per-scroll undo/redo stacks\n- EditOp: Insert, Delete, Replace\n- Phext serialization in .work.phext\n- x.chapter = edit sequence number\n- Edit history is navigable phext"
)

c2_book9 = chapters(
    "R-TTS -- Coordinate Pronunciation\n- 3x5x17+1 syllable system\n- X: Onset (open/voiced/unvoiced)\n- Y: Vowel (a/e/i/o/u)\n- Z: Coda (17 terminations)\n- Zero = 'om'\n- SSML output for TTS engines"
)

c2_book10 = chapters(
    "R3 -- Web UI\nHTTP-served phext editor. Zero-framework architecture.",
    sections(
        "R3.1 -- phext-edit\n- Raw TcpListener, no framework\n- Embedded SPA (HTML/CSS/JS)\n- REST JSON API\n- Thread-per-connection, Arc<Mutex<AppState>>\n- Sentron panel, navtree, search, edit mode\n- Coordinate hyperlinking\n- Dark theme, keyboard navigation\n- Auth token, directory mode\n- URL hash for shareable positions",
    ),
    sections(
        "R3.7 -- uml6d-edit\n- Extends phext-edit with SDLC awareness\n- Phase badge (color-coded)\n- 5D artifact address display\n- Trace panel: all 9 phases at current 5D address\n- Phase picker (p key)\n- Quick-nav: r=REQ d=DES s=SRC x=TST\n- POST /api/phase endpoint\n- Phase-colored navtree labels",
    )
)

collection_2 = books(c2_book1, c2_book2, c2_book3, c2_book4, c2_book5,
                     c2_book6, c2_book7, c2_book8, c2_book9, c2_book10)

# ── COLLECTION 3: DESIGN ──────────────────────────────────────────────

c3_book1 = chapters(
    "Core Module Design\nCoordinate extensions and lattice index form the foundation.",
    sections(
        "@startuml coordinate_ext\nenum Dimension {\n  Scroll = 1\n  Section = 2\n  Chapter = 3\n  Book = 4\n  Volume = 5\n  Collection = 6\n  Series = 7\n  Shelf = 8\n  Library = 9\n  +from_index(i: u8): Option<Dimension>\n  +name(): &str\n  +delimiter(): u8\n}\n\ntrait CoordinateNav {\n  +navigate_forward(dim): bool\n  +navigate_backward(dim): bool\n  +dimension_value(dim): usize\n  +set_dimension(dim, value)\n  +with_dimension(dim, value): Coordinate\n}\n\nCoordinate ..|> CoordinateNav\n@enduml",
    ),
    sections(
        "@startuml index\nclass ScrollSpan {\n  +start: usize\n  +end: usize\n}\n\nclass LatticeIndex {\n  -entries: HashMap<Coordinate, ScrollSpan>\n  -ordered: Vec<Coordinate>\n  +build(buffer: &[u8]): LatticeIndex\n  +get(coord): Option<&ScrollSpan>\n  +contains(coord): bool\n  +scroll_count(): usize\n  +next_populated(coord): Option<Coordinate>\n  +prev_populated(coord): Option<Coordinate>\n  +dimension_extent(dim): Vec<usize>\n}\n\nLatticeIndex --> ScrollSpan\n@enduml",
    )
)

c3_book2 = chapters(
    "Storage Module Design\nMemory-mapped I/O with copy-on-write overlay.",
    sections(
        "@startuml mmap\nenum ScrollOverlay {\n  Modified(String)\n  Deleted\n  Inserted(String)\n}\n\nclass MappedLattice {\n  -mmap: Mmap\n  -index: LatticeIndex\n  -overlay: HashMap<Coordinate, ScrollOverlay>\n  +open(path): MappedLattice\n  +read_scroll(coord): Option<String>\n  +write_scroll(coord, content)\n  +has_scroll(coord): bool\n  +save()\n  +to_phext_bytes(): Vec<u8>\n  +index(): &LatticeIndex\n}\n\nMappedLattice --> LatticeIndex\nMappedLattice --> ScrollOverlay\n@enduml",
    )
)

c3_book3 = chapters(
    "Navigation Module Design\n9D cursor model with history, marks, and populated-jump.",
    sections(
        "@startuml navigator\nclass Navigator {\n  -position: Coordinate\n  -active_dimension: Dimension\n  -marks: Vec<Coordinate>\n  -history: Vec<Coordinate>\n  +new(): Navigator\n  +position(): Coordinate\n  +select_dimension(index: u8)\n  +move_forward()\n  +move_backward()\n  +goto(coord)\n  +next_populated(index)\n  +prev_populated(index)\n  +push_mark()\n  +pop_mark()\n}\n\nNavigator --> Coordinate\nNavigator --> Dimension\n@enduml",
    ),
    sections(
        "@startuml cursor\nclass Position {\n  +line: usize\n  +col: usize\n  +from_offset(text, offset): Position\n  +to_offset(text): usize\n}\n\nclass ScrollCursor {\n  -position: Position\n  -selection: Option<Selection>\n  -sticky_col: usize\n  +move_left/right/up/down(text)\n  +word_forward/backward(text)\n}\n\nScrollCursor --> Position\n@enduml",
    )
)

c3_book4 = chapters(
    "@startuml search\nclass SearchHit {\n  +coordinate: Coordinate\n  +offset: usize\n  +length: usize\n  +context: String\n}\n\nclass SearchEngine <<functions>> {\n  +search_lattice(buffer, index, pattern): Vec<SearchHit>\n  +search_lattice_parallel(...): Vec<SearchHit>\n  +search_lattice_auto(...): Vec<SearchHit>\n  +search_coordinates(index, pattern): Vec<Coordinate>\n}\n\nnote: Parallel threshold 512KB, context 40 chars, rayon\n@enduml"
)

c3_book5 = chapters(
    "Topology Module Design\nSentron neural topology and lattice statistics.",
    sections(
        "@startuml sentron\nenum AxisGroup { Structural, Sequential }\n\nclass Axon {\n  +dimension: Dimension\n  +group: AxisGroup\n  +backward_count: usize\n  +forward_count: usize\n}\n\nclass Sentron {\n  +center: Coordinate\n  +structural_reach: usize\n  +sequential_reach: usize\n  +build(pos, index): Sentron\n  +size(): usize\n  +structural_axons(): &[Axon]\n  +sequential_axons(): &[Axon]\n}\n\nnote: 40 neurons max, 8 axons, Manhattan distance\nSentron --> Axon\n@enduml",
    ),
    sections(
        "@startuml stats\nclass ScrollStats {\n  +byte_size, line_count, word_count, char_count\n  +from_bytes(bytes): ScrollStats\n}\n\nclass DimensionDensity {\n  +dimension: Dimension\n  +distribution: Vec<(usize, usize)>\n  +sparkline(width): String\n}\n\nclass LatticeOverview {\n  +total_scrolls, total_bytes\n  +build(buffer, index): LatticeOverview\n}\n@enduml",
    )
)

c3_book6 = chapters(
    "Editor Module Design\nPluggable editing modes with vim as default.",
    sections(
        "@startuml editor\ntrait EditorMode {\n  +handle_key(key, ctx): EditResult\n  +cursor_style(): CursorStyle\n  +status_text(): String\n}\n\nenum EditResult { Nothing, CursorMoved, TextChanged, ExitEdit, Status(String) }\nenum CursorStyle { Block, Line, Underline }\n\nclass EditContext {\n  +text: String\n  +cursor: ScrollCursor\n  +undo: UndoEngine\n}\n\nVimMode ..|> EditorMode\n@enduml",
    ),
    sections(
        "@startuml vim\nenum VimSubMode { Normal, Insert, Visual, Command }\n\nclass VimMode {\n  -sub_mode: VimSubMode\n  -pending: String\n  -count: Option<usize>\n  +new(): VimMode\n}\n\nnote: Grammar [count] operator [count] motion\nMotions: h/l/j/k/w/b/e/0/$\nOperators: d/c/y\n@enduml",
    )
)

c3_book7 = chapters(
    "@startuml uml6d\nenum Phase {\n  Meta=1, Requirements=2, Design=3, Source=4,\n  Tests=5, Regressions=6, Docs=7, Whitepapers=8, Training=9\n  +from_collection(c): Option<Phase>\n  +name(): &str\n  +short(): &str\n  +color(): &str\n}\n\nclass ArtifactAddr {\n  +volume, book, chapter, section, scroll: usize\n  +from_coordinate(c): ArtifactAddr\n  +to_coordinate(phase): Coordinate\n  +display(): String\n}\n\nclass UmlContext {\n  +phase: Option<Phase>\n  +artifact: ArtifactAddr\n  +from_coordinate(c): UmlContext\n}\n\nnote: 5D address stable across SDLC phases\nPhase --> ArtifactAddr\nUmlContext --> Phase\nUmlContext --> ArtifactAddr\n@enduml"
)

c3_book8 = chapters(
    "@startuml undo\nenum EditOp {\n  Insert { offset, text }\n  Delete { offset, deleted }\n  Replace { offset, old_text, new_text }\n}\n\nclass UndoEngine {\n  -undo_stack: Vec<UndoRecord>\n  -redo_stack: Vec<UndoRecord>\n  +push(record)\n  +undo(text): Option<Position>\n  +redo(text): Option<Position>\n}\n\nnote: Work file is navigable phext\nx.chapter = edit sequence number\n@enduml"
)

c3_book9 = chapters(
    "@startuml tts\nclass CoordPronunciation {\n  +coordinate: Coordinate\n  +syllables: Vec<String>\n  +pronounce(): String\n  +to_ssml(): String\n}\n\nnote: 3x5x17+1 syllable grid\nX: Onset (3: open/voiced/unvoiced)\nY: Vowel (5: a/e/i/o/u)\nZ: Coda (17 terminations)\nZero = om\n@enduml"
)

c3_book10 = chapters(
    "Web UI Design\nTwo binaries: phext-edit (generic) and uml6d-edit (SDLC-aware).",
    sections(
        "@startuml phext_edit\nclass AppState {\n  +lattice: MappedLattice\n  +nav: Navigator\n  +overview: LatticeOverview\n  +file_path: String\n  +dirty: bool\n}\n\nclass HttpServer <<TcpListener>> {\n  +handle_request(stream, state)\n}\n\npackage REST_API {\n  GET /api/nav, /api/status, /api/tree\n  POST /api/dim, /api/forward, /api/backward\n  POST /api/next, /api/prev, /api/goto\n  POST /api/update, /api/save, /api/search\n  GET /api/zoom/z, /api/zoom/y, /api/zoom/x\n  GET /api/scroll/{coord}\n}\n\nHttpServer --> AppState\n@enduml",
    ),
    sections(
        "@startuml uml6d_edit\nclass ApiUmlContext {\n  +phase, phase_short, phase_color: String\n  +artifact_addr: String\n  +trace: Vec<ApiTraceEntry>\n}\n\nclass ApiTraceEntry {\n  +phase, phase_short, color: String\n  +collection: usize\n  +populated: bool\n}\n\npackage UML6D_API {\n  POST /api/phase\n}\n\nnote: Extends phext-edit with phase badge,\ntrace panel, quick-nav keys, 5D display\n@enduml",
    )
)

collection_3 = books(c3_book1, c3_book2, c3_book3, c3_book4, c3_book5,
                     c3_book6, c3_book7, c3_book8, c3_book9, c3_book10)

# ── COLLECTION 4: SOURCE ──────────────────────────────────────────────

c4_book1 = chapters(
    "// Core Module -- src/coordinate_ext.rs, src/index.rs",
    sections("// src/coordinate_ext.rs\n//\n// Dimension enum: Scroll(1) through Library(9)\n// CoordinateNav trait: navigate_forward, navigate_backward,\n//   dimension_value, set_dimension, with_dimension\n// Delimiters: Scroll=0x17 Section=0x18 Chapter=0x19 Book=0x1A\n//   Volume=0x1C Collection=0x1D Series=0x1E Shelf=0x1F Library=0x01\n//\n// navigate_forward: uses built-in break methods\n// navigate_backward: set(current-1), reset lower dims\n// with_dimension: non-mutating, returns new coordinate"),
    sections("// src/index.rs\n//\n// LatticeIndex::build(buffer): walks byte-by-byte tracking\n//   coordinate via delimiter bytes. ScrollSpan{start,end} stored.\n//   Coordinates pushed to sorted Vec for binary search.\n//\n// get(): HashMap O(1) lookup\n// next_populated(): binary search forward\n// prev_populated(): binary search backward\n// dimension_extent(): unique values per dimension")
)

c4_book2 = chapters(
    "// Storage Module -- src/mmap.rs",
    sections("// src/mmap.rs\n//\n// open(path): mmap read-only, build index, empty overlay\n// read_scroll: overlay first (Modified->content, Deleted->None), else mmap span\n// write_scroll: index.contains -> Modified, else Inserted\n// save: sort all coords, emit delimiters, read overlay||mmap, write temp, rename\n//   re-mmap, rebuild index, clear overlay")
)

c4_book3 = chapters(
    "// Navigation Module -- src/navigator.rs, src/cursor.rs",
    sections("// src/navigator.rs\n//\n// State: position, active_dimension, marks, history + cursor\n// select_dimension(i): set active for h/l\n// move_forward/backward: CoordinateNav on active dim\n// goto: push history, set position\n// next/prev_populated: binary search in sorted coords"),
    sections("// src/cursor.rs\n//\n// Position: (line, col) 0-indexed\n// from_offset: walk lines to convert\n// ScrollCursor: position + selection + sticky_col\n// move_left/right: line-clamped\n// move_up/down: sticky_col preserved\n// word_forward/backward: boundary scan")
)

c4_book4 = chapters("// src/search.rs\n//\n// search_scroll: hot inner loop, lowercased compare, context extraction\n// search_lattice: serial iterate all scrolls\n// search_lattice_parallel: rayon par_iter, atomic results\n// search_lattice_auto: buffer.len() vs 512KB threshold\n// search_coordinates: regex on coord strings")

c4_book5 = chapters(
    "// Topology Module -- src/sentron.rs, src/stats.rs",
    sections("// src/sentron.rs\n//\n// build(pos, index): get all coords, Manhattan distance, sort,\n//   take 40 nearest, count backward/forward per dimension\n// structural: Library/Shelf/Series/Collection\n// sequential: Volume/Book/Chapter/Section"),
    sections("// src/stats.rs\n//\n// ScrollStats::from_bytes: count lines, words, chars\n// DimensionDensity::build: bucket by dim value\n// sparkline: unicode block chars\n// LatticeOverview::build: totals + extents")
)

c4_book6 = chapters(
    "// Editor Module -- src/editor.rs, src/modes/",
    sections("// src/editor.rs\n//\n// EditorMode trait: handle_key(EditKey, &mut EditContext) -> EditResult\n// EditContext: text (String), cursor (ScrollCursor), undo (UndoEngine)\n// EditKey: code + ctrl/alt/shift modifiers"),
    sections("// src/modes/vim.rs\n//\n// VimMode: sub_mode, pending, count, command_buf\n// handle_normal: digits->count, h/l/j/k->move, d/c/y->operator\n// handle_insert: typing, Esc->normal\n// handle_command: :w/:q/:wq")
)

c4_book7 = chapters("// src/uml6d.rs\n//\n// Phase enum: Meta(1)..Training(9)\n//   from_collection, name, short, color, all\n//\n// ArtifactAddr: {volume, book, chapter, section, scroll}\n//   from_coordinate, to_coordinate(phase), to_coordinate_with_outer\n//\n// UmlContext: phase + artifact from any coordinate\n// trace_artifact: check each phase at 5D address\n// artifacts_in_phase: all addrs in a given phase")

c4_book8 = chapters("// src/undo.rs\n//\n// EditOp: Insert/Delete/Replace\n// UndoRecord: op + cursor_before + cursor_after\n// UndoEngine: undo_stack + redo_stack\n//   push: clear redo, push undo\n//   undo: pop, apply inverse, push redo\n//   redo: pop, apply forward, push undo\n// Phext serialization: x.chapter = sequence number")

c4_book9 = chapters("// src/tts.rs\n//\n// ONSETS: ['', 'b', 'p'] (3)\n// VOWELS: ['a','e','i','o','u'] (5)\n// CODAS: ['','p','t','k','b','d','g','m','n','s','f','v','l','r','ng','sh','zh'] (17)\n// byte_to_syllable: onset[v%3] + vowel[(v/3)%5] + coda[(v/15)%17]\n// Zero = 'om'")

c4_book10 = chapters(
    "// Web UI -- src/bin/phext_edit.rs, src/bin/uml6d_edit.rs",
    sections("// src/bin/phext_edit.rs\n//\n// AppState: lattice + nav + overview + file_path + dirty\n// TcpListener on port, thread::spawn per connection\n// match (method, path) to API handlers\n// INDEX_HTML: ~700 lines embedded SPA\n// API: /api/nav, /api/dim, /api/forward, /api/backward,\n//   /api/next, /api/prev, /api/goto, /api/base,\n//   /api/update, /api/save, /api/search, /api/tree,\n//   /api/zoom/*, /api/scroll/*, /api/phexts, /api/open"),
    sections("// src/bin/uml6d_edit.rs\n//\n// Extends phext-edit with:\n//   ApiUmlContext: phase, phase_short, phase_color, artifact_addr, trace\n//   POST /api/phase: change collection at fixed 5D address\n//   Frontend: phase badge, trace panel (T), phase picker (p),\n//     quick-nav r/d/s/x/R/D/w/n, UML dim labels in sentron")
)

collection_4 = books(c4_book1, c4_book2, c4_book3, c4_book4, c4_book5,
                     c4_book6, c4_book7, c4_book8, c4_book9, c4_book10)

# ── COLLECTION 5: TESTS ───────────────────────────────────────────────

c5_book1 = chapters("Core Tests", sections(
    "coordinate_ext tests:\n- coordinate_is_hashable\n- navigate_forward_and_back\n- navigate_backward_resets_lower\n- navigate_at_minimum_returns_false\n- dimension_from_index\n- with_dimension_resets_lower",
    "index tests:\n- build_empty, build_single_scroll, build_multi_scroll\n- next_populated, prev_populated\n- roundtrip byte-perfect"))
c5_book2 = chapters("mmap tests:\n- open_and_read\n- write_overlay, read_prefers_overlay\n- save_roundtrip\n- deleted_scroll, inserted_scroll")
c5_book3 = chapters("navigator tests:\n- initial_position\n- select_dimension, move_forward\n- history traversal\n- marks push/pop")
c5_book4 = chapters("search tests:\n- single_match, case_insensitive\n- max_results early termination\n- parallel matches serial\n- empty pattern")
c5_book5 = chapters("topology tests:\n- sentron build and size\n- stats from_bytes")
c5_book6 = chapters("editor tests:\n- mode trait dispatch\n- vim normal/insert/visual")
c5_book7 = chapters("uml6d tests:\n- phase_roundtrip\n- artifact_addr_from_coordinate\n- artifact_addr_to_coordinate\n- context_from_coordinate\n- artifact_display")
c5_book8 = chapters("undo tests:\n- push/undo/redo cycle\n- phext serialization")
c5_book9 = chapters("tts tests:\n- byte_to_syllable correctness\n- special coordinates")
c5_book10 = chapters("web UI tests:\n- API endpoint integration")

collection_5 = books(c5_book1, c5_book2, c5_book3, c5_book4, c5_book5,
                     c5_book6, c5_book7, c5_book8, c5_book9, c5_book10)

# ── COLLECTION 6: REGRESSIONS ─────────────────────────────────────────

collection_6 = "Regression Suite\nTrack known issues and fixes. Each entry links to the commit."

# ── COLLECTION 7: DOCS ────────────────────────────────────────────────

c7_book1 = chapters(
    scrolls(
        "Quick Start Guide\n\n1. Build: cargo build --bin uml6d-edit\n2. Run: uml6d-edit file.phext [--port 8080]\n3. Navigate: 1-9 dim, h/l move, j/k jump, p phase, e edit\n4. Phase keys: r=REQ d=DES s=SRC x=TST\n5. Trace panel: T key\n6. Save: Ctrl+S",
        "Coordinate Guide\n\nFull 9D: z.z.z/y.y.y/x.x.x\n  series.shelf.library / collection.volume.book / chapter.section.scroll\n\n6D UML inner 6:\n  collection=Phase, volume=Sprint, book=Module,\n  chapter=Component, section=File, scroll=Unit\n\n5D artifact address: volume.book.chapter/section.scroll\n\nExample: 1.1.1/4.1.2/3.1.1\n  = Source (4), Sprint 1, Module 2, Component 3, File 1, Unit 1\n  Requirement: 1.1.1/2.1.2/3.1.1  Test: 1.1.1/5.1.2/3.1.1",
        "Architecture\n\nLayer 1: Core types (coordinate_ext, index)\nLayer 2: Storage (mmap + copy-on-write)\nLayer 3: Navigation (navigator, cursor)\nLayer 4: Intelligence (search, sentron, stats)\nLayer 5: Editing (editor modes, undo)\nLayer 6: Semantics (uml6d)\nLayer 7: Presentation (web UI, TUI)\n\nDependencies flow downward. UML6D adds SDLC meaning\nwithout modifying lower layers.",
    )
)

collection_7 = books(c7_book1, "Storage docs", "Nav docs", "Search docs",
                     "Topology docs", "Editor docs", "UML6D docs", "Undo docs",
                     "TTS docs", "Web UI docs")

# ── COLLECTION 8: WHITEPAPERS ─────────────────────────────────────────

wp_phext = "Phext: Hierarchical Digital Memory\n\nPhext extends plain text to 11 dimensions via ASCII control codes.\nLine breaks (0x0A) give 2D; phext adds 7 more delimiter levels.\nEnables petabyte-scale organization in a single file.\n\nASCII defined 0x01-0x1F in the 1960s. Most fell out of use.\nPhext reclaims them as dimensional delimiters.\n\nPerformance: modern SSDs write 2 GB/sec but file abstractions\nhaven't evolved since 25 KB/sec era. Phext eliminates\nfilesystem overhead for structured data."

wp_6duml = "6D UML: Structural Traceability via Dimensional Addressing\n\nTraditional traceability matrices annotate links between\nrequirements, design, code, and tests. Annotations are fragile.\n\n6D UML makes the coordinate system the traceability matrix.\nAn artifact's 5D address is stable across all SDLC phases.\nCollection selects the phase.\n\nWalking collection 2 to 4 at same 5D address traces\nrequirement to implementation. No links to maintain.\nThe structure IS the relationship."

wp_sentron = "Sentron: Neural Topology for 9D Navigation\n\n40 neurons (nearest populated coords) form a cortical column.\n8 axons per center (4 structural + 4 sequential).\nEach measures backward/forward reachability.\n\nRebuilt sub-millisecond on every navigation event.\nProvides real-time topological awareness."

collection_8 = books("", "", "", "", chapters(wp_sentron), "",
                     chapters(wp_6duml), "", "", "")
# Put phext whitepaper at book 1 level as general
collection_8 = books(chapters(wp_phext), "", "", "", chapters(wp_sentron), "",
                     chapters(wp_6duml), "", "", "")

# ── COLLECTION 9: TRAINING ────────────────────────────────────────────

trn = """Onboarding: Your First 6D UML Session

Step 1: Look at the top bar
  - Colored badge = current SDLC phase
  - 9D coordinate = exact position
  - 5D address = artifact identity

Step 2: Navigate
  1-9 select dimension, h/l move, j/k jump populated

Step 3: Phase navigation
  p = phase picker, or quick keys: r/d/s/x

Step 4: Trace panel
  T = show all 9 phases for current artifact
  Filled = content exists, empty = not yet written

Step 5: Edit
  e = edit mode, Ctrl+S = save"""

trn_concepts = """Core Concepts

1. Phext: plain text extended to 11D via ASCII delimiters
2. Scroll: basic unit of content
3. Coordinate: 9D address (z.z.z/y.y.y/x.x.x)
4. Collection: SDLC phase dimension
5. 5D Address: artifact identity across phases
6. Trace: walking artifact across all phases
7. Sentron: local topology
8. Phase: one of 9 SDLC stages
9. Module: a book in 5D space
10. Component: a chapter within a module"""

collection_9 = books(chapters(scrolls(trn, trn_concepts)))

# ── ASSEMBLE ──────────────────────────────────────────────────────────

document = CN.join([
    collection_1, collection_2, collection_3, collection_4, collection_5,
    collection_6, collection_7, collection_8, collection_9
])

with open("uml6d.phext", 'wb') as f:
    f.write(document.encode('utf-8'))

# Verify
cols = document.split(CN)
print(f"Document size: {len(document):,} bytes")
print(f"Collections: {len(cols)}")
for i, c in enumerate(cols, 1):
    bk_list = c.split(BK)
    total = 0
    for bk in bk_list:
        for ch_text in bk.split(CH):
            for sn_text in ch_text.split(SN):
                total += 1 + sn_text.count(SC)
    print(f"  C{i}: {len(bk_list)} books, {total} scrolls")
print(f"\nWritten: uml6d.phext")
