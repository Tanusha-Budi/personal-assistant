import logging

from app.core.logging import RedactingFormatter


def test_redacts_secrets():
    formatter = RedactingFormatter("%(message)s")
    record = logging.LogRecord(
        "x", logging.INFO, "", 0, "key sk-ant-abc123_DEF and Bearer abc.def", None, None
    )
    output = formatter.format(record)
    assert "sk-ant-abc123" not in output
    assert "abc.def" not in output
    assert output.count("[REDACTED]") == 2