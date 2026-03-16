import numpy as np

from my_vlfm import LanguageParser, SemanticMap


def test_smoke_parser_and_map() -> None:
    parser = LanguageParser()
    parsed = parser.parse("go to the chair near the door")
    assert parsed.target_object == "chair"

    semantic_map = SemanticMap.from_records(
        [
            {"category": "chair", "points": [[1.0, 2.0], [1.1, 2.0]]},
            {"category": "door", "points": [[2.0, 2.0], [2.1, 2.0]]},
        ]
    )
    results = semantic_map.query_with_relation("chair", "near", "door", near_threshold_m=2.0)
    assert len(results) == 1
    assert isinstance(np.asarray(results[0].centroid), np.ndarray)
