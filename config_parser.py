"""Configuration file parser for maze generation using Pydantic."""


from pydantic import BaseModel, Field, model_validator


class MazeConfig(BaseModel):
    """Maze configuration with validated fields."""

    WIDTH: int = Field(gt=0)
    HEIGHT: int = Field(gt=0)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str = Field(min_length=1)
    PERFECT: bool

    @model_validator(mode='after')
    def validate_coordinates(self) -> 'MazeConfig':
        """Check that entry and exit are within maze bounds."""
        entry_x, entry_y = self.ENTRY
        exit_x, exit_y = self.EXIT

        if not (0 <= entry_x < self.WIDTH and 0 <= entry_y < self.HEIGHT):
            raise ValueError(f"ENTRY {self.ENTRY} is outside maze bounds")
        if not (0 <= exit_x < self.WIDTH and 0 <= exit_y < self.HEIGHT):
            raise ValueError(f"EXIT {self.EXIT} is outside maze bounds")
        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different")

        return self


def _parse_coordinate_string(value: str) -> tuple[int, int]:
    """Convert '0,0' string to tuple."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate format: {value}")
    return (int(parts[0].strip()), int(parts[1].strip()))


def parse_config(filepath: str) -> MazeConfig | None:
    """Parse a maze configuration file."""
    # Read file
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except OSError as e:
        print(f"Error: {e}")
        return None

    # Parse KEY=VALUE pairs
    raw: dict[str, str] = {}
    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            print(f"Error: Invalid syntax on line {line_num}: '{stripped}'")
            return None

        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            print(f"Error: Missing key on line {line_num}.")
            return None

        if not value:
            print(f"Error: Missing value for '{key}' on line {line_num}.")
            return None

        raw[key] = value

    # Pre-process coordinates and boolean
    try:
        if "ENTRY" in raw:
            raw["ENTRY"] = _parse_coordinate_string(raw["ENTRY"])
        if "EXIT" in raw:
            raw["EXIT"] = _parse_coordinate_string(raw["EXIT"])
        if "PERFECT" in raw:
            raw["PERFECT"] = raw["PERFECT"].lower() == "true"
    except ValueError as e:
        print(f"Error: {e}")
        return None

    # Validate with Pydantic
    try:
        return MazeConfig(**raw)
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    config = parse_config("config.txt")
    if config:
        print("Configuration parsed successfully:")
        print(f"  Size: {config.WIDTH}x{config.HEIGHT}")
        print(f"  Entry: {config.ENTRY}")
        print(f"  Exit: {config.EXIT}")
        print(f"  Perfect: {config.PERFECT}")
        print(f"  Output: {config.OUTPUT_FILE}")
    else:
        print("Configuration parsing failed.")
