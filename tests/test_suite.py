from typing import cast
from pathlib import Path
from textual.pilot import Pilot
# from textual_coloromatic import Coloromatic
from textual_coloromatic.demo import ColoromaticDemo

DEMO_DIR = Path(__file__).parent.parent / "src" / "textual_coloromatic" / "demo"
TERINAL_SIZE = (110, 36)

async def test_launch():  
    """Test launching the ColoromaticDemo app."""
    app = ColoromaticDemo()
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.exit(None) 
 

def test_snapshot_pattern_nostyle(snap_compare):

    async def run_before(pilot: Pilot[None]) -> None:
        demo_app = cast(ColoromaticDemo, pilot.app)
        demo_app.create_test_pattern()
        await pilot.pause()

    assert snap_compare(
        DEMO_DIR / "main.py",
        terminal_size=TERINAL_SIZE,
        run_before=run_before,
    )

def test_snapshot_pattern_color(snap_compare):

    async def run_before(pilot: Pilot[None]) -> None:
        demo_app = cast(ColoromaticDemo, pilot.app)
        demo_app.create_test_pattern(color=True)
        await pilot.pause()

    assert snap_compare(
        DEMO_DIR / "main.py",
        terminal_size=TERINAL_SIZE,
        run_before=run_before,
    )    