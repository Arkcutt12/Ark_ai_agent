#!/usr/bin/env python3
"""
Create example DXF files for Ark Cutt CLI Agent
"""

import os
import sys
sys.path.append('./python')

from advanced_text_vectorizer import AdvancedTextVectorizer
from advanced_2d_shape_generator import Advanced2DShapeGenerator

def create_examples():
    print("Creating example DXF files...")
    
    # Create examples directory
    if not os.path.exists('examples'):
        os.makedirs('examples')
    
    # 1. Create text example
    print("Creating text example...")
    vectorizer = AdvancedTextVectorizer()
    text_result = vectorizer.vectorize_text(
        "ARKCUTT", 
        "examples/arkcutt_text.dxf", 
        font_size=50, 
        layer_name='ENGRAVE'
    )
    print(f"   {text_result['message']}")
    
    # 2. Create gear example
    print("Creating gear example...")
    generator = Advanced2DShapeGenerator()
    generator.create_document()
    
    # Add a simple gear simulation (basic implementation)
    import ezdxf
    from ezdxf import units
    import math
    
    doc = ezdxf.new('R2010', setup=True)
    doc.units = units.MM
    msp = doc.modelspace()
    
    # Add layers
    doc.layers.add('CUT', color=1)
    doc.layers.add('ENGRAVE', color=2)
    
    # Create gear shape (simplified)
    center = (0, 0)
    outer_radius = 50
    inner_radius = 15
    teeth = 12
    
    # Outer circle
    msp.add_circle(center, outer_radius, dxfattribs={'layer': 'CUT'})
    # Inner circle
    msp.add_circle(center, inner_radius, dxfattribs={'layer': 'CUT'})
    
    # Add gear teeth (simplified)
    tooth_angle = 360 / teeth
    for i in range(teeth):
        angle = i * tooth_angle
        rad = math.radians(angle)
        
        # Outer tooth point
        x1 = center[0] + (outer_radius + 5) * math.cos(rad)
        y1 = center[1] + (outer_radius + 5) * math.sin(rad)
        
        # Connect to outer circle
        x2 = center[0] + outer_radius * math.cos(rad)
        y2 = center[1] + outer_radius * math.sin(rad)
        
        msp.add_line((x2, y2), (x1, y1), dxfattribs={'layer': 'CUT'})
    
    doc.saveas("examples/gear_12_teeth.dxf")
    print("   Gear example created: gear_12_teeth.dxf")
    
    # 3. Create bedroom floorplan example
    print("Creating bedroom floorplan example...")
    doc = ezdxf.new('R2010', setup=True)
    doc.units = units.MM
    msp = doc.modelspace()
    
    # Add layers
    doc.layers.add('WALLS', color=1)
    doc.layers.add('FURNITURE', color=3)
    
    # Room outline (4m x 3m = 4000mm x 3000mm)
    room_points = [
        (0, 0), (4000, 0), (4000, 3000), (0, 3000), (0, 0)
    ]
    
    for i in range(len(room_points)-1):
        msp.add_line(room_points[i], room_points[i+1], dxfattribs={'layer': 'WALLS'})
    
    # Add door (800mm wide)
    door_start = (1600, 0)
    door_end = (2400, 0)
    # Remove wall segment for door
    
    # Add window (1200mm wide)
    msp.add_line((500, 3000), (1700, 3000), dxfattribs={'layer': 'WALLS'})
    
    # Add furniture (bed 2000x1500mm)
    bed_points = [
        (500, 500), (2500, 500), (2500, 2000), (500, 2000), (500, 500)
    ]
    
    for i in range(len(bed_points)-1):
        msp.add_line(bed_points[i], bed_points[i+1], dxfattribs={'layer': 'FURNITURE'})
    
    # Add wardrobe
    wardrobe_points = [
        (3200, 500), (3800, 500), (3800, 1500), (3200, 1500), (3200, 500)
    ]
    
    for i in range(len(wardrobe_points)-1):
        msp.add_line(wardrobe_points[i], wardrobe_points[i+1], dxfattribs={'layer': 'FURNITURE'})
    
    doc.saveas("examples/bedroom_floorplan.dxf")
    print("   Bedroom floorplan created: bedroom_floorplan.dxf")
    
    print("\nExample DXF files created successfully!")
    print("\nFiles created:")
    print("   - examples/arkcutt_text.dxf")
    print("   - examples/gear_12_teeth.dxf") 
    print("   - examples/bedroom_floorplan.dxf")

if __name__ == "__main__":
    create_examples()