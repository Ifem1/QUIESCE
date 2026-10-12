from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
expected=["https://studio.genlayer.com/api","61999"]
text=(ROOT/'gltest.config.yaml').read_text()+(ROOT/'.env.example').read_text()
for value in expected:
    assert value in text, f"missing Studionet value: {value}"
print("NETWORK GUARD PASS: stable Studionet 61999 configured")
