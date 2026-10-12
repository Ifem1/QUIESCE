"""Live Studionet skeleton. Run only after an account is configured.

The Codex handoff instructs the agent to turn these smoke scenarios into recorded
FINALIZED evidence after deployment. This file is intentionally skipped until
QUIESCE_LIVE=1 so CI never pretends hosted consensus proof exists before it does.
"""
import os, pytest
pytestmark = pytest.mark.skipif(os.getenv("QUIESCE_LIVE") != "1", reason="live Studionet proof not requested")

def test_live_placeholder():
    assert True
