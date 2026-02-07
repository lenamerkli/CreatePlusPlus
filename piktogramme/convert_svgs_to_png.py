#!/usr/bin/env python3
"""
Script to convert square SVGs from grafikdateien-sbb-piktogramme-svg to PNGs.

Output resolutions: 16x16, 128x128, 512x512
Only converts SVGs that are square (width == height)
Maintains directory structure
"""

import os
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Tuple, Optional


def parse_viewbox(svg_path: str) -> Optional[Tuple[int, int]]:
    """
    Parse SVG file and extract viewBox dimensions.
    Returns (width, height) or None if parsing fails.
    """
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
        
        # Get viewBox attribute
        viewbox = root.get('viewBox')
        if viewbox:
            parts = viewbox.split()
            if len(parts) == 4:
                width = int(float(parts[2]))
                height = int(float(parts[3]))
                return width, height
        
        # Fallback: check width/height attributes
        width = root.get('width')
        height = root.get('height')
        if width and height:
            # Remove units if present (e.g., "400px" -> "400")
            width = int(float(width.replace('px', '')))
            height = int(float(height.replace('px', '')))
            return width, height
            
    except Exception as e:
        print(f"  Warning: Could not parse {svg_path}: {e}")
    
    return None


def is_square(svg_path: str) -> bool:
    """
    Check if SVG is square (width == height).
    """
    dimensions = parse_viewbox(svg_path)
    if dimensions:
        width, height = dimensions
        return width == height
    return False


def convert_svg_to_png(svg_path: str, output_path: str, size: int) -> bool:
    """
    Convert SVG to PNG at specified size using cairosvg.
    """
    try:
        import cairosvg
        cairosvg.svg2png(
            url=svg_path,
            write_to=output_path,
            output_width=size,
            output_height=size
        )
        return True
    except ImportError:
        print("  Error: cairosvg not installed. Run: pip install cairosvg")
        return False
    except Exception as e:
        print(f"  Error converting {svg_path}: {e}")
        return False


def convert_using_bash(svg_path: str, output_path: str, size: int) -> bool:
    """
    Alternative: Convert SVG to PNG using rsvg-convert (from librsvg).
    """
    try:
        import subprocess
        subprocess.run([
            'rsvg-convert',
            '-w', str(size),
            '-h', str(size),
            '-o', output_path,
            svg_path
        ], check=True)
        return True
    except FileNotFoundError:
        print("  Error: rsvg-convert not found. Install librsvg or use cairosvg.")
        return False
    except Exception as e:
        print(f"  Error converting {svg_path}: {e}")
        return False


def process_svg_file(
    svg_path: Path,
    source_root: Path,
    output_root: Path,
    sizes: list[int],
    use_bash: bool = False
) -> bool:
    """
    Process a single SVG file: check if square, convert to PNGs.
    """
    if not is_square(str(svg_path)):
        return False
    
    # Get relative path to maintain structure
    rel_path = svg_path.relative_to(source_root)
    
    for size in sizes:
        # Create output path: output_root/size/relative_path_with_new_extension
        output_dir = output_root / str(size) / rel_path.parent
        output_file = output_dir / f"{svg_path.stem}.png"
        
        # Create directories
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert
        if use_bash:
            success = convert_using_bash(str(svg_path), str(output_file), size)
        else:
            success = convert_svg_to_png(str(svg_path), str(output_file), size)
        
        if success:
            print(f"  Created {output_file}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Convert square SVGs to PNG at multiple resolutions.'
    )
    parser.add_argument(
        '--source',
        default='grafikdateien-sbb-piktogramme-svg/svg-druck',
        help='Source directory containing SVG files'
    )
    parser.add_argument(
        '--output',
        default='png-output',
        help='Output directory for PNG files'
    )
    parser.add_argument(
        '--sizes',
        default='16,128,512',
        help='Comma-separated list of output sizes (default: 16,128,512)'
    )
    parser.add_argument(
        '--bash',
        action='store_true',
        help='Use rsvg-convert instead of cairosvg'
    )
    
    args = parser.parse_args()
    
    # Parse sizes
    sizes = [int(s.strip()) for s in args.sizes.split(',')]
    
    source_root = Path(args.source).resolve()
    output_root = Path(args.output).resolve()
    
    print(f"Source: {source_root}")
    print(f"Output: {output_root}")
    print(f"Sizes: {sizes}")
    print()
    
    if not source_root.exists():
        print(f"Error: Source directory does not exist: {source_root}")
        return 1
    
    # Find all SVG files
    svg_files = list(source_root.rglob("*.svg"))
    print(f"Found {len(svg_files)} SVG files")
    
    converted_count = 0
    skipped_count = 0
    
    for svg_path in sorted(svg_files):
        print(f"Processing: {svg_path.relative_to(source_root)}")
        
        if process_svg_file(
            svg_path,
            source_root,
            output_root,
            sizes,
            use_bash=args.bash
        ):
            converted_count += 1
        else:
            skipped_count += 1
    
    print()
    print(f"Summary:")
    print(f"  Converted: {converted_count} square SVGs")
    print(f"  Skipped: {skipped_count} non-square SVGs")
    
    return 0


if __name__ == "__main__":
    exit(main())
