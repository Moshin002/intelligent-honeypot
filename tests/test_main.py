﻿from src.main import check_threat


def test_detection():
    assert check_threat("admin' OR 1=1--") is True  # SQLi
    assert check_threat("<script>alert(1)") is True  # XSS
    assert check_threat("normal") is False
